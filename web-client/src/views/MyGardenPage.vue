<template>
  <main class="garden">
    <div class="wrap">
      <!-- LEFT COLUMN -->
      <section class="content">
        <h1 class="title">My Garden</h1>

        <!-- Current plants -->
        <section class="section">
          <h2 class="section__heading">My current plants</h2>

          <div v-if="plants.length" class="plants">
            <div v-for="(p,i) in plants" :key="p.id" class="plant-chip">
              <span class="chip__icon">{{ p.icon }}</span>
              <span class="chip__name">{{ p.name }}</span>
              <button class="chip__del" @click="remove(i)" aria-label="remove">×</button>
            </div>
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

            <form v-if="showForm" class="add-form" @submit.prevent="add">
              <input
                v-model.trim="form.name"
                class="input"
                type="text"
                placeholder="Plant name (e.g., Lavender)"
                required
              />
              <div class="row">
                <label class="check">
                  <input type="checkbox" v-model="form.beeFriendly" />
                  good for bees
                </label>
                <select v-model="form.season" class="input select">
                  <option disabled value="">bloom season…</option>
                  <option>spring</option>
                  <option>summer</option>
                  <option>autumn</option>
                </select>
              </div>
              <button class="btn">Save plant</button>
            </form>
          </div>
        </section>

        <!-- Recommendations -->
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
import { ref, watch, onMounted } from 'vue'

/* plants state (persist to localStorage) */
const plants = ref([])
const showForm = ref(false)
const form = ref({ name: '', beeFriendly: true, season: '' })

onMounted(() => {
  const saved = localStorage.getItem('hivemind.garden')
  if (saved) plants.value = JSON.parse(saved)
})
watch(plants, v => localStorage.setItem('hivemind.garden', JSON.stringify(v)), { deep: true })

function add() {
  plants.value.push({
    id: crypto.randomUUID(),
    name: form.value.name,
    beeFriendly: form.value.beeFriendly,
    season: form.value.season,
    icon: pickIcon(form.value.name)
  })
  form.value = { name: '', beeFriendly: true, season: '' }
  showForm.value = false
}
function remove(i){ plants.value.splice(i,1) }
function quickAdd(rec){
  plants.value.push({ id: crypto.randomUUID(), name: rec.name, beeFriendly: true, season: rec.season || '', icon: rec.icon })
}

function pickIcon(name){
  const n = name.toLowerCase()
  if (n.includes('lavender')) return '💜'
  if (n.includes('sunflower')) return '🌻'
  if (n.includes('mint')) return '🌿'
  return '🌱'
}

/* hard-coded recommendations (placeholder) */
const recommendations = [
  { name:'Lavender', icon:'💜', desc:'low water, high bee activity, calming scent' },
  { name:'Sunflower', icon:'🌻', desc:'thrives in your climate and helps pollinators' }
]

/* hard-coded badges for now — later make these computed from plants */
const badges = ref([
  { key:'bee-helper',   title:'bee helper',    icon:'🐝', earned:true  },
  { key:'bloom-booster',title:'bloom booster', icon:'🌸', earned:true  },
  // Example locked badge:
  // { key:'native-champ', title:'native champ', icon:'🌿', earned:false }
])
</script>

<style scoped>
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

/* plants list */
.plants{ display:flex; flex-wrap:wrap; gap:10px; }
.plant-chip{
  display:inline-flex; align-items:center; gap:8px;
  background:#fff; border:1px solid #e6e3da; border-radius:999px;
  padding:6px 10px; box-shadow:0 2px 6px rgba(0,0,0,.04);
}
.chip__icon{ font-size:18px; }
.chip__name{ font-weight:600; }
.chip__del{
  background:transparent; border:0; font-size:16px; line-height:1; cursor:pointer;
  color:#8d8b83; padding:0 4px;
}

/* add tile + form */
.adder{ display:flex; flex-direction:column; gap:12px; }
.add-tile{
  width:110px; height:86px; border-radius:14px; border:1px solid #e1ded4;
  background:#ffe6b8; color:#1b1b1b; display:flex; flex-direction:column; align-items:center; justify-content:center;
  box-shadow:0 4px 12px rgba(0,0,0,.06); cursor:pointer;
}
.plus{ font-size:28px; line-height:1; }
.add-label{ font-size:12px; margin-top:4px; font-weight:700; }
.add-form{ background:#fff; border:1px solid #e6e3da; border-radius:12px; padding:12px; width:min(520px,100%); box-shadow:0 8px 20px rgba(0,0,0,.06);}
.input{
  width:100%; padding:10px 12px; border:1px solid #d7d4cb; border-radius:10px; background:#faf9f6;
  font-size:14px;
}
.select{ width:auto; min-width:160px; }
.row{ display:flex; gap:12px; align-items:center; margin-top:10px; }
.check{ display:inline-flex; align-items:center; gap:6px; color:#48473f; }
.btn{
  margin-top:10px; background:#0f1917; color:#e8f3ef; border:0; padding:10px 14px; border-radius:12px; cursor:pointer;
}

/* recommendations */
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

/* badges board (RIGHT) */
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
