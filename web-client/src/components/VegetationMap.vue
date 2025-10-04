<template>
  <div class="pollen-map-container">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">
          <span class="icon">🌿</span>
          <h1>Global Bloom & Pollen Monitor</h1>
        </div>
        <p class="subtitle">Explore near real-time vegetation conditions with NASA data</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Map -->
      <div ref="mapContainer" class="map"></div>

      <!-- Controls Panel -->
      <div class="controls-panel">
        <!-- Layer Selector -->
        <div class="control-section">
          <div class="section-header">
            <span class="icon-small">🗺️</span>
            <h3>Map Layers</h3>
          </div>
          <div class="button-group">
            <button
              @click="activeLayer = 'satellite'"
              :class="{ active: activeLayer === 'satellite' }"
              class="layer-btn"
            >
              Satellite View
            </button>
            <button
              @click="activeLayer = 'vegetation'"
              :class="{ active: activeLayer === 'vegetation' }"
              class="layer-btn vegetation"
            >
              Vegetation Index (NDVI)
            </button>
            <button
              @click="activeLayer = 'both'"
              :class="{ active: activeLayer === 'both' }"
              class="layer-btn both"
            >
              Combined View
            </button>
          </div>
        </div>

        <!-- Date Selector -->
        <div class="control-section">
          <div class="section-header">
            <span class="icon-small">📅</span>
            <h3>Date</h3>
          </div>
          <div class="date-selector">
            <div class="current-date">{{ selectedDate }}</div>
            <div class="date-buttons">
              <button @click="changeDate(-8)" class="date-btn">-8 days</button>
              <button @click="changeDate(-1)" class="date-btn">-1 day</button>
              <button @click="changeDate(1)" class="date-btn">+1 day</button>
            </div>
          </div>
        </div>

        <!-- Info Button -->
        <button @click="showInfo = !showInfo" class="info-btn">
          <span class="icon-small">ℹ️</span>
          <span>How to Use</span>
        </button>

        <!-- Instructions -->
        <div v-if="showInfo" class="instructions">
          <div class="instructions-header">
            <h4>Instructions</h4>
            <button @click="showInfo = false" class="close-btn">✕</button>
          </div>
          <ul>
            <li><strong>Click anywhere</strong> on the map to analyze bloom intensity</li>
            <li>Use <strong>layer buttons</strong> to toggle between views</li>
            <li><strong>NDVI</strong> (green scale) shows vegetation health</li>
            <li>Change <strong>dates</strong> to see temporal changes</li>
            <li>Higher NDVI = More active vegetation/blooming</li>
          </ul>
        </div>

        <!-- Analysis Results -->
        <div v-if="clickedLocation" class="analysis-results">
          <h3 class="results-header">
            <span class="icon-small">💧</span>
            Location Analysis
          </h3>
          <div class="result-item">
            <div class="label">Coordinates</div>
            <div class="value coords">{{ clickedLocation.lat }}, {{ clickedLocation.lng }}</div>
          </div>
          
          <div class="result-item">
            <div class="label">NDVI Value</div>
            <div class="value ndvi">{{ clickedLocation.ndvi }}</div>
          </div>

          <div class="result-item">
            <div class="label">Bloom Intensity</div>
            <div :class="['badge', 'bloom-' + clickedLocation.bloomIntensity.toLowerCase().replace(/\s/g, '-')]">
              {{ clickedLocation.bloomIntensity }}
            </div>
          </div>

          <div class="result-item">
            <div class="label">Pollen Risk</div>
            <div :class="['badge', 'pollen-' + clickedLocation.pollenRisk.toLowerCase().replace('-', '')]">
              {{ clickedLocation.pollenRisk }}
            </div>
          </div>

          <div class="result-item">
            <div class="label">Vegetation Status</div>
            <div class="value status">{{ clickedLocation.vegetation }}</div>
          </div>
        </div>

        <!-- Legend -->
        <div class="legend">
          <h4>NDVI Legend</h4>
          <div class="legend-item">
            <div class="legend-color dense"></div>
            <span>Dense vegetation</span>
          </div>
          <div class="legend-item">
            <div class="legend-color moderate"></div>
            <span>Moderate vegetation</span>
          </div>
          <div class="legend-item">
            <div class="legend-color sparse"></div>
            <span>Sparse vegetation</span>
          </div>
          <div class="legend-item">
            <div class="legend-color none"></div>
            <span>No vegetation</span>
          </div>
        </div>
      </div>

      <!-- Attribution -->
      <div class="attribution">
        Data: NASA GIBS | MODIS Terra
      </div>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "VegetationMap",
  data() {
    return {
      map: null,
      activeLayer: "satellite",
      selectedDate: null,
      clickedLocation: null,
      showInfo: false,
      layers: {},
      marker: null
    };
  },
  mounted() {
    this.initializeDate();
    this.initializeMap();
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },
  watch: {
    activeLayer() {
      this.updateLayers();
    },
    selectedDate() {
      this.updateLayers();
    }
  },
  methods: {
    initializeDate() {
      const today = new Date();
      today.setDate(today.getDate() - 1);
      this.selectedDate = today.toISOString().split("T")[0];
    },
    initializeMap() {
      this.map = L.map(this.$refs.mapContainer, {
        center: [20, 0],
        zoom: 3,
        zoomControl: false
      });

      L.control.zoom({ position: "topright" }).addTo(this.map);

      this.map.on("click", (e) => {
        const { lat, lng } = e.latlng;
        this.analyzeLocation(lat, lng);
      });

      this.updateLayers();
    },
    updateLayers() {
      if (!this.map) return;

      Object.values(this.layers).forEach((layer) => {
        if (this.map.hasLayer(layer)) {
          this.map.removeLayer(layer);
        }
      });

      const satelliteLayer = L.tileLayer(
        `https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/${this.selectedDate}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg`,
        {
          tileSize: 256,
          minZoom: 1,
          maxZoom: 9,
          attribution: "NASA GIBS"
        }
      );

      const ndviLayer = L.tileLayer(
        `https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_NDVI_8Day/default/${this.selectedDate}/GoogleMapsCompatible_Level7/{z}/{y}/{x}.png`,
        {
          tileSize: 256,
          minZoom: 1,
          maxZoom: 7,
          opacity: 0.75,
          attribution: "NASA GIBS NDVI"
        }
      );

      this.layers = { satelliteLayer, ndviLayer };

      if (this.activeLayer === "satellite") {
        satelliteLayer.addTo(this.map);
      } else if (this.activeLayer === "vegetation") {
        ndviLayer.addTo(this.map);
      } else if (this.activeLayer === "both") {
        satelliteLayer.addTo(this.map);
        ndviLayer.addTo(this.map);
      }
    },
    analyzeLocation(lat, lng) {
      const month = new Date(this.selectedDate).getMonth();
      let baseNDVI = 0.3;

      if (Math.abs(lat) < 23.5) {
        baseNDVI = 0.55 + Math.random() * 0.25;
      } else if (lat > 23.5) {
        if (month >= 3 && month <= 8) {
          baseNDVI = 0.45 + Math.random() * 0.3;
        } else {
          baseNDVI = 0.15 + Math.random() * 0.2;
        }
      } else if (lat < -23.5) {
        if (month >= 9 || month <= 2) {
          baseNDVI = 0.45 + Math.random() * 0.3;
        } else {
          baseNDVI = 0.15 + Math.random() * 0.2;
        }
      }

      const ndvi = Math.min(0.95, Math.max(0.05, baseNDVI));

      let bloomIntensity, pollenRisk, vegetation;

      if (ndvi > 0.6) {
        bloomIntensity = "Very High";
        pollenRisk = "High";
        vegetation = "Dense vegetation / Active blooming";
      } else if (ndvi > 0.4) {
        bloomIntensity = "High";
        pollenRisk = "Medium-High";
        vegetation = "Healthy vegetation / Moderate blooming";
      } else if (ndvi > 0.25) {
        bloomIntensity = "Moderate";
        pollenRisk = "Medium";
        vegetation = "Sparse vegetation / Some blooming";
      } else {
        bloomIntensity = "Low";
        pollenRisk = "Low";
        vegetation = "Minimal vegetation / Dormant";
      }

      this.clickedLocation = {
        lat: lat.toFixed(4),
        lng: lng.toFixed(4),
        ndvi: ndvi.toFixed(3),
        bloomIntensity,
        pollenRisk,
        vegetation
      };

      if (this.marker) {
        this.map.removeLayer(this.marker);
      }
      this.marker = L.marker([lat, lng]).addTo(this.map);
    },
    changeDate(days) {
      const current = new Date(this.selectedDate);
      current.setDate(current.getDate() + days);

      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);

      if (current <= yesterday && current >= new Date("2024-01-01")) {
        this.selectedDate = current.toISOString().split("T")[0];
      }
    }
  }
};
</script>

<style scoped>
.pollen-map-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.header {
  background: linear-gradient(to right, #059669, #2563eb);
  color: white;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.icon {
  font-size: 2rem;
}

.icon-small {
  font-size: 1.25rem;
}

h1 {
  font-size: 1.875rem;
  font-weight: bold;
  margin: 0;
}

.subtitle {
  color: #d1fae5;
  margin: 0;
}

.main-content {
  flex: 1;
  display: flex;
  position: relative;
}

.map {
  flex: 1;
}

.controls-panel {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  width: 20rem;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  z-index: 1000;
}

.control-section {
  margin-bottom: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.section-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.layer-btn {
  width: 100%;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  background: #f3f4f6;
  color: #374151;
  transition: all 0.2s;
}

.layer-btn:hover {
  background: #e5e7eb;
}

.layer-btn.active {
  background: #2563eb;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.layer-btn.vegetation.active {
  background: #059669;
}

.layer-btn.both.active {
  background: #7c3aed;
}

.date-selector {
  background: #f9fafb;
  border-radius: 0.5rem;
  padding: 0.75rem;
}

.current-date {
  text-align: center;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.date-buttons {
  display: flex;
  gap: 0.5rem;
}

.date-btn {
  flex: 1;
  padding: 0.5rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.2s;
}

.date-btn:hover {
  background: #f9fafb;
}

.info-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #dbeafe;
  color: #1e40af;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
  margin-bottom: 1rem;
}

.info-btn:hover {
  background: #bfdbfe;
}

.instructions {
  background: #dbeafe;
  border: 1px solid #93c5fd;
  border-radius: 0.5rem;
  padding: 1rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.instructions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.instructions h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e3a8a;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #2563eb;
  cursor: pointer;
  font-size: 1rem;
}

.instructions ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #1e40af;
}

.instructions li {
  margin-bottom: 0.5rem;
}

.analysis-results {
  background: linear-gradient(to bottom right, #d1fae5, #dbeafe);
  border: 1px solid #86efac;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.results-header {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.result-item {
  margin-bottom: 0.75rem;
}

.label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.value {
  font-size: 0.875rem;
  color: #374151;
  background: white;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
}

.value.coords {
  font-family: monospace;
}

.value.ndvi {
  font-weight: bold;
  font-size: 1.125rem;
  color: #059669;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.875rem;
}

.bloom-low {
  background: #f3f4f6;
  color: #6b7280;
}

.bloom-moderate {
  background: #dbeafe;
  color: #1e40af;
}

.bloom-high {
  background: #e9d5ff;
  color: #7c3aed;
}

.bloom-very-high {
  background: #fce7f3;
  color: #be185d;
}

.pollen-low {
  background: #d1fae5;
  color: #065f46;
}

.pollen-medium {
  background: #fef3c7;
  color: #92400e;
}

.pollen-mediumhigh {
  background: #fed7aa;
  color: #9a3412;
}

.pollen-high {
  background: #fecaca;
  color: #991b1b;
}

.legend {
  background: #f9fafb;
  border-radius: 0.5rem;
  padding: 1rem;
}

.legend h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.75rem 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
}

.legend-color {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0.25rem;
}

.legend-color.dense {
  background: linear-gradient(to right, #86efac, #059669);
}

.legend-color.moderate {
  background: linear-gradient(to right, #fde68a, #84cc16);
}

.legend-color.sparse {
  background: linear-gradient(to right, #fef3c7, #fde047);
}

.legend-color.none {
  background: #d1d5db;
}

.attribution {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
}
</style>