<template>
  <main>
    <!-- hero bar (dark) -->
    <section class="hero">
      <img :src="logo" alt="hivemind.exe bee logo" class="hero__logo" />
      <h1 class="hero__title">hivemind<span class="dot">.</span>exe</h1>
    </section>

    <!-- big visual (mockup shows a photo below hero) -->
    <section class="visual">
      <div class="visual__bg" role="img" aria-label="seedling and science overlay"></div>
      <div class="visual__overlay">
        <h2>BloomWatch — global flowering & pollen insights</h2>
        <p>
          Explore near real-time vegetation conditions using NASA Earth observations.  
          Start with the <RouterLink to="/monitor">monitor</RouterLink> or learn
          more <RouterLink to="/about">about us</RouterLink>.
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import logo from '@/assets/hivemind.exe_logo_white_bzz.png'
</script>

<style scoped>
/* dark top area like the mockup */
.hero{
  background:#0f1917;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:56px 20px 44px;
}
.hero__logo{ width:74px; height:auto; margin-bottom:10px; filter:drop-shadow(0 2px 0 rgba(0,0,0,.2)); }
.hero__title{
  color:#e9f6f1; font-size:56px; line-height:1; letter-spacing:.04em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  font-weight:700;
}
.dot{ opacity:.7 }

/* image section under hero */
.visual{
  position:relative; min-height:420px; overflow:hidden; background:#0a0a0a;
}
.visual__bg{
  position:absolute; inset:0;
  background-image: url('https://images.unsplash.com/photo-1501004318641-b39e6451bec6?q=80&w=2070&auto=format&fit=crop'); /* placeholder */
  background-size:cover; background-position:center;
  filter:brightness(.72) contrast(1.05);
}
.visual__overlay{
  position:relative; z-index:1; max-width:1100px; margin:0 auto; padding:36px 20px;
  color:#f6fbf9;
}
.visual__overlay h2{ font-size:28px; margin-bottom:8px; font-weight:600; }
.visual__overlay p{ max-width:720px; opacity:.95; }
.visual__overlay a{ color:#b3ffea; text-decoration:underline; text-underline-offset:3px; }
</style>
