<template>
  <main class="garden">
    <div class="wrap">
      <!-- LEFT COLUMN -->
      <section class="content">
        <h1 class="title">My Garden</h1>

        <!-- Current plants -->
        <section class="section">
          <h2 class="section__heading">My current plants</h2>

          <div v-if="myPlants.length" class="cards">
            <article
              v-for="(p,i) in myPlants"
              :key="p.id + '-' + i"
              class="plant-card"
              :class="{ flipped: flippedCard === p.id }"
              :style="cardStyle(p)"
              @mouseenter="hoverFlip(p.id)"
              @mouseleave="hoverFlip(null)"
              @click="toggleFlip(p.id)"
            >
                <!-- front -->
                <div class="card-face card-front">
                <div class="card-title">{{ p.commonName }}</div>
                <div class="card-sub">{{ p.scientificName }}</div>
                <button class="remove" @click.stop="remove(i)" aria-label="remove">×</button>
                </div>

                <!-- back -->
                <div class="card-face card-back">
                <div class="back-title">{{ p.commonName }}</div>
                <div class="kv"><span>Scientific</span><b>{{ p.scientificName }}</b></div>
                <div class="kv"><span>Bloom months</span><b>{{ monthsToLabels(p.bloomMonths).join(', ') }}</b></div>
                <div class="kv"><span>Pollinators</span><b>{{ (p.pollinators || []).join(', ') }}</b></div>
                <p class="desc">{{ p.description }}</p>

                <!-- NEW: remove on the back too -->
                <button class="remove" @click.stop="remove(i)" aria-label="remove">×</button>
                </div>

            </article>
          </div>
          <p v-else class="muted">No plants added yet</p>
        </section>

        <!-- Add new plant -->
        <section class="section">
          <h2 class="section__heading">Add new plant</h2>

          <div class="adder">
            <button class="add-tile" @click="showForm = !showForm" :aria-expanded="showForm">
              <span class="plus">+</span>
              <span class="add-label">Add Plant</span>
            </button>

            <!-- FILTERABLE PICKER (replaces the old free-text form) -->
            <form v-if="showForm" class="add-form" @submit.prevent="addSelected">
              <!-- Filters -->
              <div class="filters">
                <div class="fcol">
                  <label class="flabel">Pollinators</label>
                  <div class="chips">
                    <button
                      v-for="p in pollinatorOptions"
                      :key="p"
                      class="chip"
                      :class="{active: selected.pollinators.includes(p)}"
                      @click.prevent="toggle('pollinators', p)"
                    >{{ p }}</button>
                  </div>
                </div>

                <div class="fcol">
                  <label class="flabel">Bloom months</label>
                  <div class="months">
                    <button
                      v-for="m in monthOptions"
                      :key="m"
                      class="mchip"
                      :class="{active: selected.months.includes(m)}"
                      @click.prevent="toggle('months', m)"
                      :title="monthLabels[m]"
                    >{{ monthLabels[m].slice(0,3).toLowerCase() }}</button>
                  </div>
                </div>

                <div class="fcol">
                  <label class="flabel">Color</label>
                  <div class="colors">
                    <button
                      v-for="c in colorOptions"
                      :key="c"
                      class="cchip"
                      :class="{active: selected.colors.includes(c)}"
                      :style="{ '--swatch': c }"
                      @click.prevent="toggle('colors', c)"
                      :title="c"
                    />
                  </div>
                </div>

                <button class="link-clear" v-if="hasAnyFilter" @click.prevent="clearFilters">clear filters</button>
              </div>

              <!-- Plant dropdown (filtered) -->
              <div class="row select-row">
                <select v-model="selectedPlantId" class="input select">
                  <option disabled value="">choose a plant…</option>
                  <option
                    v-for="p in filteredPlants"
                    :key="p.id"
                    :value="p.id"
                  >
                    {{ p.commonName }} — {{ p.scientificName }}
                  </option>
                </select>
                <div v-if="selectedCardPreview" class="preview-swatch" :style="{ background: selectedCardPreview.color }"></div>
              </div>

              <button class="btn" :disabled="!selectedPlantId">Save plant</button>
              <p class="muted small" v-if="filtersHelp">
                Showing {{ filteredPlants.length }} of {{ allPlants.length }} plants (matches your filters).
              </p>
            </form>
          </div>
        </section>

        <!-- Recommendations (kept as before) -->
        <section class="section">
          <h2 class="section__heading">Recommended plants to add to my garden</h2>

          <div class="recs">
            <article v-for="rec in recommendations" :key="rec.name" class="rec">
              <div class="rec__icon">{{ rec.icon }}</div>
              <div class="rec__body">
                <div class="rec__title">Add <strong>{{ rec.name }}</strong></div>
                <div class="rec__desc">{{ rec.desc }}</div>
              </div>
              <button class="rec__btn" @click="quickAdd(rec)">Add</button>
            </article>
          </div>
        </section>
      </section>

      <!-- RIGHT COLUMN: BADGES -->
      <aside class="badges">
        <div class="badges__label">My badges</div>
        <div class="board">
          <div v-for="b in badges" :key="b.key" class="badge" :class="{ earned: b.earned }">
            <div class="badge__icon">{{ b.icon }}</div>
            <div class="badge__text">{{ b.title }}</div>
          </div>
        </div>
      </aside>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

/* ---------- API: load the 10-plant collection ---------- */
/* If you proxy /api to the Flask server, keep API_BASE = '' (relative). */
const API_BASE = 'http://localhost:5000'   // change to 'http://localhost:5000' if you are NOT proxying

const allPlants = ref([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/plants`)
    if (!res.ok) throw new Error(`${res.status}`)
    const data = await res.json()
    allPlants.value = data.plants || []
  } catch (e) {
    error.value = 'Could not reach /api/plants; showing a tiny fallback.'
    // Fallback so the page still works if the server isn’t running:
    allPlants.value = [
      { id:'trifolium_pratense', commonName:'Rödklöver', scientificName:'Trifolium pratense', bloomMonths:[5,6,7,8], pollinators:['bees','bumblebees'], description:'Red clover - excellent for long-tongued bumblebees', color:'#DC143C' },
      { id:'calluna_vulgaris', commonName:'Ljung',      scientificName:'Calluna vulgaris',     bloomMonths:[7,8,9],     pollinators:['bees','bumblebees'], description:'Late summer bloomer, vital for autumn pollinators', color:'#DDA0DD' },
    ]
  } finally {
    loading.value = false
  }
})

/* ---------- Month labels helper ---------- */
const monthLabels = {
  1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
  7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'
}
const monthOptions = Object.keys(monthLabels).map(n => Number(n))
const monthsToLabels = (arr=[]) => arr.map(m => monthLabels[m] ?? m)

/* ---------- Filters inside Add Plant form ---------- */
const selected = ref({ pollinators: [], months: [], colors: [] })
const hasAnyFilter = computed(() =>
  selected.value.pollinators.length || selected.value.months.length || selected.value.colors.length
)
const pollinatorOptions = computed(() => {
  const set = new Set()
  allPlants.value.forEach(p => p.pollinators?.forEach(x => set.add(x)))
  return Array.from(set).sort()
})
const colorOptions = computed(() => {
  const set = new Set(allPlants.value.map(p => p.color).filter(Boolean))
  return Array.from(set)
})
function toggle(type, value){
  const arr = selected.value[type]
  const i = arr.indexOf(value)
  i === -1 ? arr.push(value) : arr.splice(i, 1)
}
function clearFilters(){ selected.value = { pollinators: [], months: [], colors: [] } }

const filteredPlants = computed(() => {
  return allPlants.value.filter(p => {
    const okPoll = !selected.value.pollinators.length ||
      selected.value.pollinators.every(pol => (p.pollinators || []).includes(pol))
    const okMonths = !selected.value.months.length ||
      selected.value.months.some(m => (p.bloomMonths || []).includes(m))
    const okColor = !selected.value.colors.length ||
      selected.value.colors.includes(p.color)
    return okPoll && okMonths && okColor
  })
})
const filtersHelp = computed(() => hasAnyFilter.value && allPlants.value.length)

/* ---------- My garden state (persist) ---------- */
const myPlants = ref([])
const showForm = ref(false)
const selectedPlantId = ref('')
const flippedCard = ref(null)

onMounted(() => {
  const saved = localStorage.getItem('hivemind.garden.v3')
  if (saved) myPlants.value = JSON.parse(saved)
})
watch(myPlants, v => localStorage.setItem('hivemind.garden.v3', JSON.stringify(v)), { deep: true })

const selectedCardPreview = computed(() => allPlants.value.find(x => x.id === selectedPlantId.value))

function addSelected(){
  const p = allPlants.value.find(x => x.id === selectedPlantId.value)
  if (!p) return
  myPlants.value.push(JSON.parse(JSON.stringify(p)))
  selectedPlantId.value = ''
  showForm.value = false
}
function quickAdd(rec){
  // Optional helper from the static list
  myPlants.value.push({
    id: rec.name.toLowerCase().replace(/\s+/g,'_'),
    commonName: rec.name, scientificName: rec.name, bloomMonths: [], pollinators: [], description: rec.desc, color:'#FFF6DD'
  })
}
function remove(i){ myPlants.value.splice(i,1) }

function hoverFlip(id){ flippedCard.value = id }
function toggleFlip(id){ flippedCard.value = flippedCard.value === id ? null : id }

/* ---------- Badges (as before) ---------- */
const badges = ref([
  { key:'bee-helper',   title:'bee helper',    icon:'🐝', earned:true  },
  { key:'bloom-booster',title:'bloom booster', icon:'🌸', earned:true  },
])

/* ---------- Card colors / contrast ---------- */
function cardStyle(p){
  const bg = p.color || '#e0e0e0'
  const txt = contrastColor(bg)
  const border = isVeryLight(bg) ? '1px solid rgba(0,0,0,.2)' : '1px solid rgba(255,255,255,.18)'
  return { '--bg': bg, '--txt': txt, '--border': border }
}
function hexToRgb(hex){
  const h = hex.replace('#','')
  const b = parseInt(h.length===3 ? h.split('').map(x=>x+x).join('') : h, 16)
  return { r:(b>>16)&255, g:(b>>8)&255, b:b&255 }
}
function luminance(hex){
  const {r,g,b} = hexToRgb(hex)
  const toLin = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4) }
  return 0.2126*toLin(r) + 0.7152*toLin(g) + 0.0722*toLin(b)
}
function contrastColor(hex){ return luminance(hex) > 0.58 ? '#1b1b1b' : '#f7f7f7' }
function isVeryLight(hex){ return luminance(hex) > 0.9 }

/* ---------- Recommendations (unchanged) ---------- */
const recommendations = [
  { name:'Lavender', icon:'💜', desc:'low water, high bee activity, calming scent' },
  { name:'Sunflower', icon:'🌻', desc:'thrives in your climate and helps pollinators' }
]
</script>

<style scoped>
/* add a little space under the color chips before the select row */
.select-row { 
  margin-top: 12px;       /* tweak 10–16px to taste */
}

/* optional: a touch more space under the color chip group itself */
.colors { 
  gap: 8px; 
  margin-bottom: 2px;     /* or 4–6px if you want more */
}


.garden{ background:#f2f1eb; min-height:100vh; }
.wrap{
  max-width:1100px; margin:0 auto; padding:28px 20px 80px;
  display:grid; grid-template-columns: 1.2fr .8fr; gap:28px;
}
.title{
  font-family: "Helvetica Neue", Arial, ui-sans-serif, system-ui;
  font-size:38px; margin:10px 0 18px; color:#2c2c2c;
}

/* sections & dividers */
.section{ padding:16px 0 4px; }
.section + .section{ border-top:1px solid #d8d5cc; }
.section__heading{
  font-size:24px; font-weight:600; margin:0 0 12px; color:#2c2c2c;
  border-bottom:1px solid #d8d5cc; padding-bottom:8px;
}
.muted{ color:#6c6a63; }
.small{ font-size:12px; }

/* --- CARDS UNDER "MY CURRENT PLANTS" --- */
.cards{ display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:14px; }
.plant-card{
  position:relative; height:160px; perspective:1000px; border-radius:16px; cursor:pointer;
  color:var(--txt); background:var(--bg); border:var(--border);
  box-shadow:0 8px 18px rgba(0,0,0,.08);
}
.card-face{
  position:absolute; inset:0; border-radius:inherit; padding:14px;
  backface-visibility:hidden; transform-style:preserve-3d;
  transition: transform .5s ease;
}
.card-front{ display:flex; flex-direction:column; gap:4px; }
.card-title{ font-weight:800; font-size:18px; }
.card-sub{ opacity:.9; font-size:12px; }

.remove{
  position:absolute; top:6px; right:8px;
  background:rgba(0,0,0,.22); color:#fff;
  border:0; width:22px; height:22px; border-radius:999px;
  cursor:pointer; font-weight:700; line-height:22px;
}


.card-back{
  transform: rotateY(180deg);
  background: color-mix(in oklab, var(--bg), white 8%);
  color: var(--txt);
  display:flex; flex-direction:column; gap:6px; font-size:13px;
}
.back-title{ font-weight:800; }
.kv{ display:flex; justify-content:space-between; gap:10px; border-bottom:1px dashed rgba(0,0,0,.15); padding-bottom:4px; }
.kv span{ opacity:.8; }
.desc{ margin:4px 0 0; font-size:12px; line-height:1.4; }

/* flip interaction */
.plant-card:hover .card-front{ transform: rotateY(180deg); }
.plant-card:hover .card-back{ transform: rotateY(360deg); }
.plant-card.flipped .card-front{ transform: rotateY(180deg); }
.plant-card.flipped .card-back{ transform: rotateY(360deg); }

/* --- ADD TILE + FILTERABLE PICKER --- */
.adder{ display:flex; flex-direction:column; gap:12px; }
.add-tile{
  width:110px; height:86px; border-radius:14px; border:1px solid #e1ded4;
  background:#ffe6b8; color:#1b1b1b; display:flex; flex-direction:column; align-items:center; justify-content:center;
  box-shadow:0 4px 12px rgba(0,0,0,.06); cursor:pointer;
}
.plus{ font-size:28px; line-height:1; }
.add-label{ font-size:12px; margin-top:4px; font-weight:700; }

.add-form{ background:#fff; border:1px solid #e6e3da; border-radius:12px; padding:12px; width:min(680px,100%); box-shadow:0 8px 20px rgba(0,0,0,.06);}

.filters{ display:grid; gap:14px; }
.fcol{ display:flex; flex-direction:column; gap:8px; }
.flabel{ font-weight:700; color:#30302a; }
.chips, .months, .colors{ display:flex; flex-wrap:wrap; gap:8px; }

.chip{
  padding:6px 10px; border-radius:999px; border:1px solid #d9d6cd;
  background:#fff; cursor:pointer;
}
.chip.active{ background:#0f1917; color:#e8f3ef; border-color:#0f1917; }

.mchip{
  width:40px; height:28px; border-radius:8px; border:1px solid #d9d6cd; background:#fff; cursor:pointer;
  display:flex; align-items:center; justify-content:center; font-size:12px;
}
.mchip.active{ background:#0f1917; color:#e8f3ef; border-color:#0f1917; }

.cchip{
  width:28px; height:28px; border-radius:999px; border:1px solid #c9c6bd;
  background: var(--swatch);
  cursor:pointer;
  box-shadow: inset 0 0 0 2px rgba(255,255,255,.5);
}
.cchip.active{ outline:2px solid #0f1917; }

.link-clear{
  margin-top:6px; align-self:start; background:none; border:0; color:#0f1917; text-decoration:underline; cursor:pointer;
}

.row{ display:flex; gap:12px; align-items:center; }
.input{
  width:100%; padding:10px 12px; border:1px solid #d7d4cb; border-radius:10px; background:#faf9f6;
  font-size:14px;
}
.select{ min-width:320px; }
.preview-swatch{
  width:26px; height:26px; border-radius:999px; border:1px solid rgba(0,0,0,.12);
  box-shadow: inset 0 0 0 2px rgba(255,255,255,.55);
}

.btn{
  margin-top:10px; background:#0f1917; color:#e8f3ef; border:0; padding:10px 14px; border-radius:12px; cursor:pointer;
}
.btn:disabled{ opacity:.5; cursor:default; }

/* --- Recommendations (unchanged visuals) --- */
.recs{ display:flex; flex-direction:column; gap:10px; }
.rec{
  display:grid; grid-template-columns: 42px 1fr auto; align-items:center; gap:12px;
  background:#fff; border:1px solid #e6e3da; border-radius:12px; padding:10px 12px;
  box-shadow:0 6px 14px rgba(0,0,0,.05);
}
.rec__icon{ font-size:24px; filter: drop-shadow(0 1px 0 rgba(0,0,0,.1)); }
.rec__title{ font-size:16px; }
.rec__desc{ color:#5e5c54; font-size:14px; }
.rec__btn{
  background:#ffe6b8; border:1px solid #e8c986; color:#1b1b1b; padding:8px 12px; border-radius:10px; cursor:pointer; font-weight:700;
}

/* --- Badges board (RIGHT) --- */
.badges{ position:relative; }
.badges__label{
  position:absolute; left:24px; top:-14px; background:#f2b544; color:#171a19;
  font-weight:700; padding:6px 14px; border-radius:14px; box-shadow:0 4px 10px rgba(0,0,0,.08);
}
.board{
  background:#0f1917; border-radius:28px; padding:28px 20px; color:#e8f3ef;
  box-shadow:0 18px 36px rgba(0,0,0,.18);
  min-height:240px; display:flex; gap:16px; align-items:flex-start; flex-wrap:wrap;
}
.badge{
  background:#1a2522; border:1px solid rgba(255,255,255,.08); border-radius:18px;
  padding:10px 12px; width:110px; text-align:center; opacity:.65;
}
.badge.earned{ opacity:1; background:#1e2d28; }
.badge__icon{ font-size:28px; }
.badge__text{ font-size:12px; margin-top:4px; font-weight:700; }

/* layout */
.content{ min-width:0; }
@media (max-width: 900px){
  .wrap{ grid-template-columns:1fr; }
  .badges__label{ position:static; display:inline-block; margin:0 0 8px 0; }
}
</style>
