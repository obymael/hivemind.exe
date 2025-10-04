<template>
  <main>
    <!-- hero bar (dark) -->
    <section class="hero">
      <img :src="logo" alt="hivemind.exe bee logo" class="hero__logo" />
      <h1 class="hero__title">hivemind<span class="dot">.</span>exe</h1>
    </section>

    <!-- big visual (mockup shows a photo below hero) -->
    <section class="visual">
      <img class="visual__img" :src="heroBg" alt="seedling with biometrics overlay" />
      <div class="visual__shade"></div>
      <!--
      <div class="visual__overlay">
        <h2>hivemind.exe — global flowering & pollen insights</h2>
        <p>
          Explore near real-time vegetation conditions using NASA Earth observations.
          Start with the <RouterLink to="/monitor">monitor</RouterLink> or learn
          more <RouterLink to="/about">about us</RouterLink>.
        </p>
      </div>
      -->
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

/* image section under hero */
.visual{ position:relative; overflow:hidden; }
.visual__img{ display:block; width:100%; height:auto; }   /* full image, no crop */
.visual__shade{ position:absolute; inset:0; background:rgba(0,0,0,.28); }
/* keep your constrained text width */
.visual__overlay{
  position:absolute; inset:0; z-index:1;
  display:block;
}
.visual__overlay h2,
.visual__overlay p{
  max-width:1100px; margin:0 auto; padding:36px 20px; color:#f6fbf9;
}
.visual__overlay h2{ font-size:28px; margin-bottom:8px; font-weight:600; }
.visual__overlay p{ max-width:720px; opacity:.95; }
.visual__overlay a{ color:#b3ffea; text-decoration:underline; text-underline-offset:3px; }

</style>
