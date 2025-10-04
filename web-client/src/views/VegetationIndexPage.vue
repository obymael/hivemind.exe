<template>
  <div>
    <h1>🌍 Global Vegetation Monitor</h1>
    <p>Explore near real-time vegetation conditions with NASA data.</p>

    <!-- Map -->
    <VegetationMap />

    <!-- Placeholder pollen data -->
    <section class="pollen-section">
      <h2>Current Pollen Count</h2>
      <p>Loading pollen data from backend...</p>
    </section>
  </div>
</template>

<script>
import VegetationMap from "../components/VegetationMap.vue"

export default {
  name: "MonitorPage",
  components: { VegetationMap }
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
