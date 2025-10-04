<template>
  <div id="map" class="map-container"></div>
</template>

<script>
import L from "leaflet"
import "leaflet/dist/leaflet.css"

export default {
  name: "PollenMap",
  mounted() {
    const map = L.map("map").setView([20, 0], 2)
    
    // Use OpenStreetMap for testing
    const osmLayer = L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }
    )
    osmLayer.addTo(map)
  }
}
</script>

<style>
.map-container {
  height: 600px;
  width: 100%;
  border: 2px solid #ddd;
  border-radius: 8px;
}
</style>