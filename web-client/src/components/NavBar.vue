<template>
  <header class="nav">
    <div class="nav__inner">
      <RouterLink class="brand" to="/">
        <img :src="logo" alt="hivemind.exe logo" class="brand__logo" />
        <span class="brand__name">hivemind.exe</span>
      </RouterLink>

      <nav class="links">
        <RouterLink to="/" exact-active-class="active">home</RouterLink>
        <RouterLink to="/about" active-class="active">about</RouterLink>
        <RouterLink to="/monitor" active-class="active">monitor</RouterLink>
        <RouterLink to="/contact" active-class="active">contact</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import logo from '@/assets/hivemind.exe_logo_white_bzz.png'
</script>

<style scoped>
.nav {
  background:#0f1917; /* deep green/black from mockups */
  border-bottom:1px solid rgba(255,255,255,.06);
}
.nav__inner{
  max-width:1100px; margin:0 auto; padding:14px 20px;
  display:flex; align-items:center; justify-content:space-between;
}
.brand{ display:flex; align-items:center; gap:10px; text-decoration:none; }
.brand__logo{ width:24px; height:24px; object-fit:contain; }
.brand__name{ color:#e8f3ef; font-weight:600; letter-spacing:.04em; }
.links{ display:flex; gap:26px; }
.links a{
  color:#e8f3ef; text-decoration:none; opacity:.9; font-weight:500;
}
.links a:hover{ opacity:1; text-decoration:underline; text-underline-offset:4px; }
.active{ text-decoration:underline; text-underline-offset:6px; }
</style>
