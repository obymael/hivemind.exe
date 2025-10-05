/**
Parts of this code were enhanced with the help of generative AI
*/
<template>
  <div class="pollen-map-container">
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
            min="2020"
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
            <li><strong>Slider:</strong> Drag to view NDVI for different years (2020-2025)</li>
            <li><strong>Data:</strong> NOAA VIIRS NDVI V1 via NASA GIBS</li>
          </ul>
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
      selectedYear: 2025,
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
    // Remove existing NDVI layer
    if (this.layers.ndviLayer) {
      this.map.removeLayer(this.layers.ndviLayer);
      this.layers.ndviLayer = null;
    }

    // Map your NDVI GeoTIFFs by year
    const tifMap = {
      2020: "http://localhost:8000/cog/tiles/{z}/{x}/{y}.png?url=file://server/NDVI_2020_global.tif",
      2021: "http://localhost:8000/cog/tiles/{z}/{x}/{y}.png?url=file://server/NDVI_2021_global.tif",
      2022: "http://localhost:8000/cog/tiles/{z}/{x}/{y}.png?url=file://server/NDVI_2022_global.tif",
      2023: "http://localhost:8000/cog/tiles/{z}/{x}/{y}.png?url=file://server/NDVI_2023_global.tif",
      2024: "http://localhost:8000/cog/tiles/{z}/{x}/{y}.png?url=file://server/NDVI_2024_global.tif",
      2025: "http://localhost:8000/cog/tiles/{z}/{x}/{y}.png?url=file:///home/julia/Desktop/nasa-2025/hivemind.exe/server/NDVI_2025_global.tif",
    };

    const ndviUrl = tifMap[this.selectedYear];
    if (!ndviUrl) return;

    const ndviLayer = L.tileLayer(ndviUrl, {
      opacity: 0.7,
      attribution: "NOAA VIIRS NDVI",
      tileSize: 256,
      tms: false,
    });

    ndviLayer.addTo(this.map);
    this.layers.ndviLayer = ndviLayer;

  } catch (err) {
    console.error("Error adding NDVI layer:", err);
  }
},

    updateYearLayer() {
        this.updateLayers();
        this.fetchNDVILayer();
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