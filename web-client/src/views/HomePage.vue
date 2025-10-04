<template>
  <div>
    <h1>🌍 Global Bloom & Pollen Monitor</h1>
    <p>Explore near real-time vegetation conditions with NASA data.</p>

    <!-- Map -->
    <PollenMap />

    <!-- Placeholder pollen data -->
    <section class="pollen-section">
      <h2>Current Pollen Count</h2>
      <p>Loading pollen data from backend...</p>
    </section>
  </div>
</template>

<script>
import PollenMap from "../components/PollenMap.vue"

export default {
  name: "HomePage",
  components: { PollenMap }
}
</script>

<style scoped>
h1 {
  margin-bottom: 10px;
}
.pollen-section {
  margin-top: 20px;
  padding: 10px;
  border-top: 1px solid #ddd;
}
</style>
