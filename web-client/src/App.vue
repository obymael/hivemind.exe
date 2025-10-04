<template>
  <SiteHeader :variant="variant" />
  <RouterView />
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import SiteHeader from '@/components/SiteHeader.vue'

const route = useRoute()
const variant = computed(() => route.meta.headerVariant === 'home' ? 'home' : 'inner')
</script>

<style>
/* optional: keep links from turning blue/purple */
a { color: inherit; }
html, body, #app { margin:0; padding:0; }
</style>
