<template>
  <main>
    <!-- hero bar (dark) -->
    <section class="hero">
      <img :src="logo" alt="hivemind.exe bee logo" class="hero__logo" />
      <h1 class="hero__title">hivemind<span class="dot">.</span>exe</h1>
    </section>

    <!-- big visual -->
    <section class="visual">
      <img class="visual__img" :src="heroBg" alt="seedling with biometrics overlay" />

      <!-- gradient pairs nicely with frosted glass -->
      <div class="visual__grad"></div>

      <div class="visual__panel">
        <div class="panel__inner">
          <!-- FROSTED GLASS (centered overlay) -->
          <div class="panel__copy copy--glass copy--frosted">
            <section class="intro">
              <h2>What if your backyard could help the planet?</h2>
              <p>
                <strong>hivemind.exe</strong> turns NASA Earth data into everyday actions you can take
                to support vegetation and pollinators—right where you live.
              </p>
            </section>

            <section class="feature">
              <h3>My Garden Planner</h3>
              <p>
                Tell us where you are and what’s growing in your garden. We’ll build a bloom calendar
                from trusted flowering datasets and run a <strong>gap analysis</strong> to find months
                with little nectar or pollen in your area. Then we recommend <strong>region-appropriate plants</strong>
                to fill those gaps—so you can feed pollinators across the whole season and see your impact over time.
              </p>
              <ul>
                <li>A personal bloom timeline for your garden</li>
                <li>Recommendations based on your location and local flowering data</li>
                <li>Tips to sustain pollinators and increase biodiversity</li>
              </ul>
            </section>

            <section class="feature">
              <h3>Vegetation Time-Machine (NDVI)</h3>
              <p>
                Explore how vegetation has changed from <strong>2014–2025</strong> with an interactive
                <strong> NDVI</strong> overlay. Use the year slider to watch coverage expand or shrink.
              </p>
              <p class="muted"><em>If coverage trends down, we’ll guide you to actionable steps—planting choices and local actions—so you can help turn the curve.</em></p>
            </section>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import logo from '@/assets/hivemind.exe_logo_white_bzz.png'
import heroBg from '@/assets/nature_biometrics.png'
</script>

<style scoped>
/* dark top area like the mockup */
.hero{
  background:#0f1917;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:56px 20px 44px;
}
.hero__logo{ width:180px; height:auto; margin-bottom:10px; filter:drop-shadow(0 2px 0 rgba(0,0,0,.2)); }
.hero__title{
  color:#e9f6f1; font-size:56px; line-height:1; letter-spacing:.04em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  font-weight:700;
}
.dot{ opacity:.7 }

/* image */
.visual{ position:relative; overflow:hidden; }
.visual__img{ display:block; width:100%; height:auto; }

/* gradient (softer because we have a glass panel) */
.visual__grad{
  position:absolute; inset:0;
  background: linear-gradient(to bottom,
    rgba(15,25,23,.55) 0%,
    rgba(15,25,23,.28) 34%,
    transparent 70%);
  pointer-events:none;
}

/* centered overlay */
.visual__panel{
  position:absolute; inset:0;
  display:flex; justify-content:center; align-items:center;
  padding: clamp(24px, 7vw, 120px) 20px;
}
.panel__inner{ width:min(1100px, 100%); display:flex; justify-content:center; }

/* shared text styles — same font as the navbar */
.panel__copy{
  position: relative;                 /* needed for frosted highlight */
  width:min(900px, 100%);
  text-align:center;
  color:#f2fbf8;
  font-family:"Trebuchet MS","Avenir","Century Gothic",system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
}

/* base glass */
.copy--glass{
  background: rgba(10,14,13,.20);
  backdrop-filter: blur(8px) saturate(115%);
  -webkit-backdrop-filter: blur(8px) saturate(115%);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 18px;
  box-shadow: 0 14px 36px rgba(0,0,0,.22);
  padding: clamp(18px, 2.8vw, 30px);
}

/* FROSTED variant — darker emerald + stronger blur */
.copy--frosted{
  /* darker tint (lower lightness) + a bit more opacity */
  background: hsla(160, 36%, 12%, 0.46);
  /* more blur for stronger frost */
  backdrop-filter: blur(18px) saturate(120%) contrast(108%);
  -webkit-backdrop-filter: blur(18px) saturate(120%) contrast(108%);
  border: 1px solid hsla(160, 45%, 55%, 0.26);
  box-shadow: 0 18px 40px rgba(0,0,0,.28);
}

/* keep the subtle emerald highlight */
.copy--frosted::before{
  content:"";
  position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background: linear-gradient(135deg,
    hsla(160, 55%, 70%, 0.12) 0%,
    hsla(160, 45%, 60%, 0.05) 28%,
    transparent 60%);
}


/* graceful fallback if blur unsupported */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))){
  .copy--glass,
  .copy--frosted{
    background: rgba(10,14,13,.34);
    border-color: rgba(255,255,255,.12);
  }
}

/* typography */
.intro h2{ font-size:clamp(26px,3.2vw,40px); line-height:1.2; margin:0 0 10px; }
.intro p{ margin:0 0 6px; line-height:1.7; }
.feature{ margin-top:18px; }
.feature h3{ font-size:clamp(18px,2.2vw,22px); margin:8px 0 6px; }
.feature p{ margin:0 0 8px; line-height:1.75; }
.feature ul{ margin:8px auto 0; text-align:left; width:min(760px,100%); }
.feature li{ margin:4px 0; }
.muted{ opacity:.92; }

/* mobile */
@media (max-width: 800px){
  .feature ul{ width:100%; }
}
</style>
