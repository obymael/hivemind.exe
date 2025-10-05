<template>
  <!-- variant: 'home' (no logo) | 'inner' (logo + centered links) -->
  <header class="hdr" :class="variant">
    <div class="bar">
      <RouterLink
        v-if="variant==='inner'"
        to="/"
        class="brand"
        aria-label="hivemind.exe"
      >
        <img :src="logoMark" alt="" class="brand__logo" />
        <span class="brand__name">hivemind.exe</span>
      </RouterLink>

      <nav class="links" aria-label="Primary">
        <RouterLink to="/" exact-active-class="active">home</RouterLink>
        <RouterLink to="/about" active-class="active">about</RouterLink>
        <RouterLink to="/monitor" active-class="active">monitor</RouterLink>
        <RouterLink to="/mygarden" active-class="active">my garden</RouterLink>
        <RouterLink to="/contact" active-class="active">contact</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
defineProps({ variant: { type: String, default: 'inner' } })
import logoMark from '@/assets/hivemind.exe_logo_white_bzz.png'
</script>

<style scoped>
.hdr{
  background:#0f1917;
  border-bottom:1px solid rgba(255,255,255,.06);
  color:#e8f3ef;
  width:100%;
}

/* center the links; position brand on the left so it doesn't push the nav */
.bar{
  max-width:1100px;
  margin:0 auto;
  padding:14px 20px;
  position:relative;
  display:flex;
  align-items:center;
  justify-content:center;
}

/* brand (logo + name) */
.brand{
  position:absolute;
  left:20px;
  display:inline-flex;
  align-items:center;
  gap:10px;
  text-decoration:none;
}
.brand__logo{ width:24px; height:24px; object-fit:contain; }
.brand__name{
  color:#e8f3ef;          /* white text next to logo */
  font-weight:700;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  letter-spacing:.03em;
  /* if you want black text instead: color:#0f1917; */
}

/* centered links */
.links{
  display:flex;
  gap:56px;
  justify-content:center;
  align-items:center;
  text-transform:lowercase;
  letter-spacing:.02em;
  font-weight:700;
  font-size:22px;
  font-family: "Trebuchet MS","Avenir","Century Gothic",system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
}
.links a{ color:#f2fbf8; text-decoration:none; }
.links a:hover{ text-decoration:underline; text-underline-offset:6px; }
.active{ text-decoration:underline; text-underline-offset:6px; }

/* home variant: no brand (already handled by v-if), slightly taller top padding */
.hdr.home .bar{ padding:22px 20px 18px; }
</style>
