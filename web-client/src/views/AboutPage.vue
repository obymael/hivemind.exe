<template>
  <div class="page">
    <NavBar />

    <main class="container">
      <section class="about">
        <div class="copy">
          <h1>About Us</h1>
          <p>
            We are <strong>Flower Power Tower Girls</strong> — a tiny team of three software
            engineers behind <em>hivemind.exe</em>. Bees inspired us: they follow the pulse of
            flowers, guiding life across ecosystems. Our project aims to do the same using NASA
            Earth observations: help everyone witness the pulse of life on Earth.
          </p>
          <ul>
            <li><strong>Global Bloom &amp; Pollen monitor</strong> powered by near real-time data.</li>
            <li>Animated globe &amp; seasonal “bloom wave” transitions across continents.</li>
            <li>Simple insights for planners, gardeners, allergy sufferers, and curious minds.</li>
          </ul>
          <p>
            At the heart of it, our project is about curiosity, collaboration, and a little bit of
            flower power. 🌼🐝
          </p>
        </div>

        <figure class="art" aria-label="three girls with flowers and bees"></figure>
      </section>
    </main>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
.page{ background:#f2f1eb; min-height:100vh; }
.container{ max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
.about{
  display:grid; grid-template-columns: 1.2fr 1fr; gap:26px; align-items:start;
}
.copy h1{
  font-family: "Helvetica Neue", Helvetica, Arial, ui-sans-serif, system-ui;
  font-size:38px; margin:12px 0 14px; color:#2c2c2c;
}
.copy p{ color:#3b3b3b; line-height:1.7; }
.copy ul{ margin:10px 0 0 18px; color:#3b3b3b; }
.copy li{ margin:6px 0; }
.art{
  width:100%; height:360px; border-radius:10px;
  background:
    radial-gradient(ellipse at top right, rgba(255,200,0,.18), transparent 60%),
    #fff url('https://images.unsplash.com/photo-1606800052052-a08af714886d?q=80&w=1200&auto=format&fit=crop') center/cover no-repeat;
  box-shadow:0 8px 24px rgba(0,0,0,.08);
}
@media (max-width:900px){
  .about{ grid-template-columns:1fr; }
  .art{ order:-1; height:220px; }
}
</style>
