<template>
  <div class="pollen-map-container">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">
          <span class="icon">🌿</span>
          <h1>Global Vegetation Monitor</h1>
        </div>
        <p class="subtitle">Track NOAA VIIRS NDVI changes from 2014–2025</p>
      </div>
    </div>

    <div class="main-content">
      <!-- Map Container -->
      <div ref="mapContainer" class="map"></div>

      <!-- Controls Panel -->
      <div class="controls-panel">
        <!-- Map Layers -->
        <div class="control-section">
          <div class="section-header">
            <h3>Map Layers</h3>
          </div>
          <div class="button-group">
            <button @click="setLayer('satellite')" :class="{ active: activeLayer === 'satellite' }" class="layer-btn">Satellite View</button>
          </div>
        </div>

        <!-- NDVI Year Slider -->
        <div class="control-section">
          <div class="section-header">
            <h3>NDVI Year Selector</h3>
          </div>
          <input
            type="range"
            min="2014"
            max="2025"
            step="1"
            v-model.number="selectedYear"
            @input="updateYearLayer"
            class="year-slider"
          />
          <div class="year-display">
            <div class="year-label">Year: {{ selectedYear }}</div>
          </div>
        </div>

        <!-- Info Button -->
        <button @click="showInfo = !showInfo" class="info-btn">
          <span class="icon-small">ℹ️</span>
          <span>How to Use</span>
        </button>

        <div v-if="showInfo" class="instructions">
          <div class="instructions-header">
            <h4>Instructions</h4>
            <button @click="showInfo = false" class="close-btn">✕</button>
          </div>
          <ul>
            <li><strong>Slider:</strong> Drag to view NDVI for different years (2014-2025)</li>
            <li><strong>Click:</strong> Click anywhere to analyze vegetation at that location</li>
            <li><strong>Data:</strong> NOAA VIIRS NDVI V1 via NASA GIBS</li>
          </ul>
        </div>

        <!-- Location Analysis -->
        <div v-if="clickedLocation" class="analysis-results">
          <h3 class="results-header">
            Location Analysis
          </h3>

          <div v-if="clickedLocation.loading" class="loading">
            <div class="spinner"></div>
            <p>Analyzing location...</p>
          </div>

          <div v-else-if="!clickedLocation.error">
            <div class="result-item">
              <div class="label">Coordinates</div>
              <div class="value coords">{{ clickedLocation.lat }}, {{ clickedLocation.lng }}</div>
            </div>

            <div class="result-item">
              <div class="label">NDVI Value</div>
              <div class="value ndvi-value">{{ clickedLocation.ndvi }}</div>
            </div>

            <div class="result-item">
              <div class="label">Biome Type</div>
              <div class="value biome">{{ clickedLocation.biome }}</div>
            </div>

            <div class="result-item">
              <div class="label">Elevation</div>
              <div class="value">{{ clickedLocation.elevation }}m</div>
            </div>

            <div class="result-item">
              <div class="label">Vegetation Status</div>
              <div :class="['badge', 'veg-' + clickedLocation.category.toLowerCase().replace(/\s/g, '-')]">
                {{ clickedLocation.category }}
              </div>
            </div>

            <div class="result-item">
              <div class="label">Description</div>
              <div class="value status">{{ clickedLocation.vegetation }}</div>
            </div>

            <div v-if="clickedLocation.climate" class="climate-section">
              <h4 class="subsection-title">Climate Factors</h4>
              <div class="climate-grid">
                <div class="climate-item">
                  <span class="climate-icon">🌡️</span>
                  <span class="climate-label">Avg Temp:</span>
                  <span class="climate-value">{{ clickedLocation.climate.avgTemp.toFixed(1) }}°C</span>
                </div>
                <div class="climate-item">
                  <span class="climate-icon">🌧️</span>
                  <span class="climate-label">Precipitation:</span>
                  <span class="climate-value">{{ Math.round(clickedLocation.climate.totalPrecip) }}mm/yr</span>
                </div>
              </div>
            </div>

            <div v-if="clickedLocation.factors" class="factors-section">
              <h4 class="subsection-title">NDVI Factors</h4>
              <div class="factor-bars">
                <div class="factor-bar">
                  <div class="factor-label">Seasonal</div>
                  <div class="bar-container">
                    <div class="bar-fill" :style="{ width: (clickedLocation.factors.seasonal * 100) + '%' }"></div>
                  </div>
                  <div class="factor-value">{{ (clickedLocation.factors.seasonal * 100).toFixed(0) }}%</div>
                </div>
                <div class="factor-bar">
                  <div class="factor-label">Elevation</div>
                  <div class="bar-container">
                    <div class="bar-fill" :style="{ width: (clickedLocation.factors.elevation * 100) + '%' }"></div>
                  </div>
                  <div class="factor-value">{{ (clickedLocation.factors.elevation * 100).toFixed(0) }}%</div>
                </div>
                <div class="factor-bar">
                  <div class="factor-label">Temperature</div>
                  <div class="bar-container">
                    <div class="bar-fill" :style="{ width: (clickedLocation.factors.temperature * 100) + '%' }"></div>
                  </div>
                  <div class="factor-value">{{ (clickedLocation.factors.temperature * 100).toFixed(0) }}%</div>
                </div>
                <div class="factor-bar">
                  <div class="factor-label">Precipitation</div>
                  <div class="bar-container">
                    <div class="bar-fill" :style="{ width: (clickedLocation.factors.precipitation * 100) + '%' }"></div>
                  </div>
                  <div class="factor-value">{{ (clickedLocation.factors.precipitation * 100).toFixed(0) }}%</div>
                </div>
              </div>
            </div>

            <div v-if="clickedLocation.pollinatorPlants && clickedLocation.pollinatorPlants.length > 0" class="pollinator-section">
              <h4 class="subsection-title">🌸 Swedish Pollinator Plants (Blooming Now)</h4>
              <div class="plant-list">
                <div v-for="plant in clickedLocation.pollinatorPlants" :key="plant.id" class="plant-item">
                  <div class="plant-color" :style="{ backgroundColor: plant.color }"></div>
                  <div class="plant-info">
                    <div class="plant-name">{{ plant.commonName }}</div>
                    <div class="plant-sci">{{ plant.scientificName }}</div>
                  </div>
                </div>
              </div>
              <div class="plant-note">Data: GBIF + iNaturalist</div>
            </div>

            <div v-if="clickedLocation.trend" class="trend-info">
              <h4 class="subsection-title">Historical Trend & Projection</h4>
              <div class="trend-text">{{ clickedLocation.trend.text }}</div>
              <div class="trend-stats">
                <div class="stat-item">
                  <span class="stat-label">Total Change:</span>
                  <span :class="['stat-value', clickedLocation.trend.changePercent > 0 ? 'positive' : 'negative']">
                    {{ clickedLocation.trend.changePercent > 0 ? '+' : '' }}{{ clickedLocation.trend.changePercent.toFixed(1) }}%
                  </span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">2030 Projection:</span>
                  <span class="stat-value">{{ clickedLocation.trend.prediction2030.toFixed(3) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="error-message">
            {{ clickedLocation.error }}
          </div>
        </div>

        <!-- NDVI Legend -->
        <div class="legend">
          <h4>NDVI Legend (NOAA VIIRS)</h4>
          <div class="legend-item"><div class="legend-color dense"></div><span>Dense vegetation (0.6-1.0)</span></div>
          <div class="legend-item"><div class="legend-color moderate"></div><span>Moderate vegetation (0.4-0.6)</span></div>
          <div class="legend-item"><div class="legend-color sparse"></div><span>Sparse vegetation (0.2-0.4)</span></div>
          <div class="legend-item"><div class="legend-color minimal"></div><span>Minimal/No vegetation (0-0.2)</span></div>
        </div>
      </div>

      <div class="attribution">
        Data: NOAA CDR VIIRS NDVI V1 via NASA GIBS • Map: Leaflet
      </div>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";

export default {
  name: "VegetationMap",
  data() {
    return {
      map: null,
      activeLayer: "satellite",
      selectedYear: 2020,
      comparisonYear: 2015,
      comparisonMode: false,
      clickedLocation: null,
      showInfo: false,
      layers: {},
      marker: null,
      availableYears: Array.from({ length: 12 }, (_, i) => 2014 + i),
    };
  },
  computed: {
    displayDate() {
      return `${this.selectedYear}-06-15`;
    }
  },
  mounted() {
    this.initializeMap();
  },
  beforeUnmount() {
    if (this.map) this.map.remove();
  },
  methods: {
    initializeMap() {
      this.map = L.map(this.$refs.mapContainer, {
        center: [20, 0],
        zoom: 3,
        zoomControl: false,
      });
      L.control.zoom({ position: "topright" }).addTo(this.map);

      this.map.on("click", (e) => {
        const { lat, lng } = e.latlng;
        this.analyzeLocation(lat, lng);
      });

      this.updateLayers();
      this.fetchNDVILayer();
    },

    formatDate(year, month = 6, day = 15) {
      return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    },

    async fetchNDVILayer() {
      try {
        const bounds = this.map.getBounds();
        const bboxStr = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;
        const res = await fetch(`http://localhost:5001/api/ndvi?year=${this.selectedYear}&bbox=${bboxStr}`);
        const data = await res.json();
        if (this.layers.ndviHeat) this.map.removeLayer(this.layers.ndviHeat);

        const heatPoints = data.ndvi_points.map(p => [p.lat, p.lon, p.ndvi]);
        const heatLayer = L.heatLayer(heatPoints, { radius: 25, blur: 15, maxZoom: 10 }).addTo(this.map);
        this.layers.ndviHeat = heatLayer;
      } catch (err) {
        console.error("Failed to fetch NDVI:", err);
      }
    },

    toggleComparison() {
      this.comparisonMode = !this.comparisonMode;
      if (this.comparisonMode) {
        this.updateComparison();
      } else {
        this.updateLayers();
      }
    },

    updateComparison() {
      if (!this.comparisonMode) return;
      Object.values(this.layers).forEach(layer => { if (this.map.hasLayer(layer)) this.map.removeLayer(layer); });
      // Comparison left/right could be implemented here if needed
      this.fetchNDVILayer();
    },

    updateYearLayer() {
      if (this.comparisonMode) {
        this.updateComparison();
      } else {
        this.updateLayers();
        this.fetchNDVILayer();
      }
    },

    async analyzeLocation(lat, lng) {
      try {
        this.clickedLocation = { lat: parseFloat(lat).toFixed(4), lng: parseFloat(lng).toFixed(4), loading: true };

        const analysisRes = await fetch(`http://localhost:5001/api/analyze?lat=${lat}&lon=${lng}&year=${this.selectedYear}&month=6`);
        const analysis = await analysisRes.json();

        const trendRes = await fetch(`http://localhost:5001/api/trend?lat=${lat}&lon=${lng}`);
        const trendData = await trendRes.json();

        let pollinatorPlants = [];
        if (lat > 55 && lat < 70 && lng > 10 && lng < 25) {
          try {
            const plantsRes = await fetch(`http://localhost:5000/api/calendar`);
            const plantsData = await plantsRes.json();
            const currentMonth = new Date().getMonth() + 1;
            pollinatorPlants = plantsData.calendar[currentMonth] || [];
          } catch {
            console.warn("Failed to fetch pollinator plants");
          }
        }

        this.clickedLocation = {
          lat: parseFloat(lat).toFixed(4),
          lng: parseFloat(lng).toFixed(4),
          ndvi: analysis.ndvi.value,
          biome: analysis.ndvi.biome,
          elevation: analysis.ndvi.elevation,
          climate: analysis.ndvi.climate,
          factors: analysis.ndvi.factors,
          vegetation: analysis.vegetation.description,
          category: analysis.vegetation.category,
          pollen: analysis.pollen,
          pollinatorPlants: pollinatorPlants.map(p => ({
            id: p.scientificName,
            commonName: p.commonName,
            scientificName: p.scientificName,
            color: p.color || "#d1fae5"
          })),
          trend: {
            direction: trendData.analysis.trend,
            text: `${trendData.analysis.emoji} ${trendData.interpretation}`,
            changePercent: trendData.analysis.totalChangePercent,
            prediction2030: trendData.projection.predictedNDVI
          },
          loading: false
        };

        if (this.marker) this.map.removeLayer(this.marker);
        this.marker = L.marker([lat, lng]).addTo(this.map);
      } catch (err) {
        console.error("Error analyzing location:", err);
        this.clickedLocation = {
          lat: parseFloat(lat).toFixed(4),
          lng: parseFloat(lng).toFixed(4),
          error: "Failed to fetch analysis data",
          loading: false,
        };
      }
    },

    setLayer(layerName) {
      this.activeLayer = layerName;
      this.comparisonMode = false;
      this.updateLayers();
    },

    updateLayers() {
      Object.values(this.layers).forEach(layer => { if (this.map.hasLayer(layer)) this.map.removeLayer(layer); });

      const date = this.formatDate(this.selectedYear);

      const satellite = L.tileLayer(
        `https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_NOAA20_CorrectedReflectance_TrueColor/default/${date}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg`,
        { tileSize: 256, maxZoom: 9, attribution: "NASA GIBS - VIIRS NOAA-20", opacity: 1 }
      );

      this.layers = { satellite };
      if (this.activeLayer === "satellite") satellite.addTo(this.map);
      if (this.activeLayer === "both") satellite.addTo(this.map);
    },
  },
};
</script>

<style scoped>
.pollen-map-container { width:100%; height:100vh; display:flex; flex-direction:column; background:#f9fafb; font-family: system-ui, -apple-system, sans-serif; }
.header { background:linear-gradient(135deg, #059669 0%, #2563eb 100%); color:white; padding:1.5rem; box-shadow:0 4px 12px rgba(0,0,0,0.15);}
.header-content { max-width: 1400px; margin: 0 auto; }
.header-title { display: flex; align-items: center; gap: 0.75rem; }
.icon { font-size: 2.5rem; }
.header-title h1 { margin: 0; font-size: 1.75rem; font-weight: 700; }
.subtitle { margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 0.95rem; }
.main-content { flex:1; display:flex; position:relative;}
.map { flex:1;}
.controls-panel { position:absolute; top:1rem; left:1rem; background:white; border-radius:0.75rem; box-shadow:0 10px 25px rgba(0,0,0,0.15); padding:1.25rem; width:22rem; max-height: calc(100vh - 150px); overflow-y: auto; z-index:1000;}
.control-section { margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #e5e7eb; }
.control-section:last-of-type { border-bottom: none; }
.section-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.section-header h3 { font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0; }
.icon-small { font-size: 1.25rem; }
.button-group { display: flex; flex-direction: column; gap: 0.5rem; }
.layer-btn { width:100%; padding:0.625rem 1rem; border:2px solid transparent; border-radius:0.5rem; cursor:pointer; background:#f3f4f6; font-size: 0.875rem; font-weight: 500; transition: all 0.2s; color: #374151; }
.layer-btn:hover { background: #e5e7eb; border-color: #d1d5db; }
.layer-btn.active { background:#059669; color:white; border-color: #047857; }
.year-slider { width:100%; appearance:none; height:8px; border-radius:4px; background: linear-gradient(to right, #d1d5db 0%, #059669 50%, #2563eb 100%); outline:none; margin:0.75rem 0; cursor: pointer;}
.year-slider::-webkit-slider-thumb { appearance:none; width:20px; height:20px; border-radius:50%; background:#fff; cursor:pointer; border: 3px solid #059669; box-shadow: 0 2px 6px rgba(0,0,0,0.2);}
.year-slider::-moz-range-thumb { width:20px; height:20px; border-radius:50%; background:#fff; cursor:pointer; border: 3px solid #059669; box-shadow: 0 2px 6px rgba(0,0,0,0.2);}
.year-display { text-align: center; }
.year-label { font-weight: 600; color:#1f2937; font-size: 1.125rem; margin-bottom: 0.25rem; }
.comparison-btn { width: 100%; padding: 0.625rem 1rem; background: #eff6ff; border: 2px solid #3b82f6; color: #1e40af; border-radius: 0.5rem; cursor: pointer; font-weight: 600; transition: all 0.2s; font-size: 0.875rem; }
.comparison-btn:hover { background: #dbeafe; }
.comparison-controls { margin-top: 0.75rem; }
.comparison-label { display: block; font-size: 0.875rem; color: #374151; font-weight: 500; }
.year-select { width: 100%; margin-top: 0.5rem; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem; cursor: pointer; }
.info-btn { width: 100%; padding: 0.625rem 1rem; background: #dbeafe; border: none; border-radius: 0.5rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; font-weight: 500; transition: all 0.2s; margin-bottom: 1rem; color: #1e40af; }
.info-btn:hover { background: #bfdbfe; }
.instructions { background: #eff6ff; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; border: 1px solid #bfdbfe; }
.instructions-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.instructions-header h4 { margin: 0; font-size: 0.875rem; font-weight: 600; color: #1e40af; }
.close-btn { background: none; border: none; cursor: pointer; font-size: 1.25rem; color: #6b7280; padding: 0; line-height: 1; }
.close-btn:hover { color: #374151; }
.instructions ul { margin: 0; padding-left: 1.25rem; font-size: 0.875rem; color: #374151; line-height: 1.6; }
.instructions li { margin-bottom: 0.5rem; }
.analysis-results { background: linear-gradient(135deg, #f0fdf4 0%, #dbeafe 100%); border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; border: 1px solid #bbf7d0; }
.results-header { font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem; }
.result-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; font-size: 0.875rem; }
.result-item .label { color: #6b7280; font-weight: 500; }
.result-item .value { font-weight: 600; color: #1f2937; text-align: right; }
.result-item .coords { font-family: 'Courier New', monospace; font-size: 0.75rem; }
.result-item .status { font-size: 0.8rem; color: #059669; max-width: 60%; text-align: right; line-height: 1.4; }
.trend-info { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #cbd5e1; }
.trend-indicator { font-size: 0.875rem; font-weight: 600; margin-top: 0.5rem; padding: 0.5rem; border-radius: 0.375rem; text-align: center; }
.trend-indicator.increasing { background: #d1fae5; color: #065f46; }
.trend-indicator.decreasing { background: #fee2e2; color: #991b1b; }
.trend-indicator.stable { background: #fef3c7; color: #92400e; }
.legend { background:#f9fafb; border-radius:0.5rem; padding:1rem; border: 1px solid #e5e7eb;}
.legend h4 { font-size: 0.875rem; font-weight: 600; margin: 0 0 0.75rem 0; color: #1f2937; }
.legend-item { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.625rem; font-size: 0.8rem; color: #374151; }
.legend-color { width:2rem; height:1.25rem; border-radius:0.25rem; flex-shrink: 0;}
.legend-color.dense { background:linear-gradient(to right, #059669, #10b981);}
.legend-color.moderate { background:linear-gradient(to right, #84cc16, #a3e635);}
.legend-color.sparse { background:linear-gradient(to right, #fde047, #fef08a);}
.legend-color.minimal { background: linear-gradient(to right, #e5e7eb, #f3f4f6);}
.attribution { position:absolute; bottom:0.5rem; right:0.5rem; background:rgba(255,255,255,0.95); padding:0.375rem 0.875rem; border-radius:0.375rem; font-size:0.75rem; color:#6b7280; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
</style>