<template>
  <!-- variant: 'home' (no logo) | 'inner' (logo left + centered links) -->
  <header class="hdr" :class="variant">
    <div class="row">
      <RouterLink
        v-if="variant==='inner'"
        to="/"
        class="brand"
        aria-label="hivemind.exe"
      >
        <img :src="logoMark" alt="" />
        <span class="sr-only">hivemind.exe</span>
      </RouterLink>

      <nav class="links" aria-label="Primary">
        <RouterLink to="/" exact-active-class="active">home</RouterLink>
        <RouterLink to="/about" active-class="active">about</RouterLink>
        <RouterLink to="/monitor" active-class="active">monitor</RouterLink>
        <RouterLink to="/contact" active-class="active">contact</RouterLink>
      </nav>

      <!-- spacer to balance grid when brand is shown -->
      <div v-if="variant==='inner'" class="spacer" />
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

/* 3-col grid so links stay perfectly CENTERED even with a brand on the left */
.row{
  max-width:1100px; margin:0 auto;
  padding:14px 20px;
  display:grid; grid-template-columns: 1fr auto 1fr; align-items:center;
}

/* brand only rendered for inner pages */
.brand{ display:inline-flex; align-items:center; }
.brand img{ width:24px; height:24px; object-fit:contain; }

/* center nav */
.links{
  display:flex; gap:44px; justify-content:center; align-items:center;
  text-transform:lowercase;
  letter-spacing:.02em;
  font-weight:700;
  /* Roundish feel like the mock: use system stack unless you add a webfont */
  font-family: "Trebuchet MS", "Avenir", "Century Gothic", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}
.links a{
  color:#f2fbf8; text-decoration:none;
}
.links a:hover{ text-decoration:underline; text-underline-offset:6px; }
.active{ text-decoration:underline; text-underline-offset:6px; }

/* when variant=home: hide brand column and bump spacing a touch */
.hdr.home .row{ grid-template-columns: 1fr auto 1fr; padding:22px 20px 18px; }
.hdr.home .links{ gap:56px; font-size:28px; }       /* big, like your sketch */
.hdr.inner .links{ gap:36px; font-size:18px; }      /* slightly smaller inside */

.sr-only{
  position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden;
  clip:rect(0,0,0,0); white-space:nowrap; border:0;
}
.spacer{ justify-self:end; }
</style>
