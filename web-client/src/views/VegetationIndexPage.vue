/**
Parts of this code were enhanced with the help of generative AI
*/
<template>
  <div class="page">
    <main class="container">
      <section class="content">
        <h1>Global Vegetation Monitor</h1>
        <p>Track vegetation level changes from 2020–2025 — powered by NOAA VIIRS.</p>

        <!-- Map (now full width) -->
        <div class="map-wrapper">
          <VegetationMap />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import VegetationMap from "../components/VegetationMap.vue"
</script>

<style scoped>
/* Match contact page aesthetic */
.page {
  background: #f2f1eb;
  min-height: 100vh;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 28px 20px 60px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

h1 {
  font-size: 34px;
  margin: 10px 0 4px;
  color: #2c2c2c;
}

p {
  color: #4a4a4a;
  line-height: 1.6;
}

/* Full-width map inside container */
.map-wrapper {
  margin-top: 10px;
  width: 100%;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

/* Pollen info section */
.pollen-section {
  background: #fff;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
}

.pollen-section h2 {
  font-size: 20px;
  margin-bottom: 8px;
  color: #2c2c2c;
}

@media (max-width: 900px) {
  .map-wrapper {
    margin-top: 20px;
  }
}
</style>
