from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
from functools import lru_cache
import ee
import numpy as np
from sklearn.linear_model import LinearRegression

# Initialize Earth Engine
ee.Initialize()

app = Flask(__name__)
CORS(app)  # Enable CORS for Vue.js frontend


# =========================
# BloomData API
# =========================

class BloomDataAPI:
    """Real-time API for Swedish pollinator plant bloom data"""
    
    def __init__(self):
        self.gbif_base = "https://api.gbif.org/v1"
        self.inaturalist_base = "https://api.inaturalist.org/v1"
        
        # Swedish pollinator plants with phenology data
        self.plants_db = {
            "hepatica_nobilis": {
                "commonName": "Blåsippa",
                "scientificName": "Hepatica nobilis",
                "bloomMonths": [3, 4, 5],
                "pollinators": ["bees", "flies"],
                "description": "Early spring flower, critical for pollinators emerging from winter",
                "color": "#9370DB"
            },
            "ranunculus_acris": {
                "commonName": "Smörblomma", 
                "scientificName": "Ranunculus acris",
                "bloomMonths": [5, 6, 7],
                "pollinators": ["bees", "flies", "beetles"],
                "description": "Common meadow flower, provides abundant nectar throughout summer",
                "color": "#FFD700"
            },
            "achillea_millefolium": {
                "commonName": "Rölleka",
                "scientificName": "Achillea millefolium",
                "bloomMonths": [6, 7, 8],
                "pollinators": ["bees", "butterflies", "flies"],
                "description": "Hardy perennial, excellent for continuous summer blooming",
                "color": "#FFFFFF"
            },
            "calluna_vulgaris": {
                "commonName": "Ljung",
                "scientificName": "Calluna vulgaris",
                "bloomMonths": [7, 8, 9],
                "pollinators": ["bees", "bumblebees"],
                "description": "Late summer bloomer, vital for autumn pollinators",
                "color": "#DDA0DD"
            },
            "taraxacum_officinale": {
                "commonName": "Maskros",
                "scientificName": "Taraxacum officinale",
                "bloomMonths": [4, 5, 6],
                "pollinators": ["bees", "butterflies", "flies"],
                "description": "Often overlooked but crucial early season food source",
                "color": "#FFFF00"
            },
            "salix_caprea": {
                "commonName": "Videört (Sälg)",
                "scientificName": "Salix caprea",
                "bloomMonths": [3, 4],
                "pollinators": ["bees", "bumblebees"],
                "description": "Willow catkins - one of the first pollen sources in spring",
                "color": "#F0E68C"
            },
            "leucanthemum_vulgare": {
                "commonName": "Prästkrage",
                "scientificName": "Leucanthemum vulgare",
                "bloomMonths": [6, 7],
                "pollinators": ["bees", "flies", "butterflies"],
                "description": "Classic Swedish meadow flower with long bloom period",
                "color": "#FFFFFF"
            },
            "vicia_cracca": {
                "commonName": "Åkervicker",
                "scientificName": "Vicia cracca",
                "bloomMonths": [6, 7, 8],
                "pollinators": ["bees", "bumblebees"],
                "description": "Native vetch providing protein-rich pollen",
                "color": "#8B7BC8"
            },
            "trifolium_pratense": {
                "commonName": "Rödklöver",
                "scientificName": "Trifolium pratense",
                "bloomMonths": [5, 6, 7, 8],
                "pollinators": ["bees", "bumblebees"],
                "description": "Red clover - excellent for long-tongued bumblebees",
                "color": "#DC143C"
            },
            "trifolium_repens": {
                "commonName": "Vitklöver",
                "scientificName": "Trifolium repens",
                "bloomMonths": [5, 6, 7, 8, 9],
                "pollinators": ["bees", "honeybees"],
                "description": "White clover - ground cover supporting many pollinator species",
                "color": "#F5F5F5"
            }
        }
    
    @lru_cache(maxsize=100)
    def get_gbif_data(self, scientific_name):
        """Fetch real-time occurrence data from GBIF"""
        try:
            url = f"{self.gbif_base}/occurrence/search"
            params = {
                "scientificName": scientific_name,
                "country": "SE",
                "limit": 50,
                "hasCoordinate": True,
                "year": "2020,2025"  # Recent observations
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                # Extract coordinates
                locations = []
                for occ in results[:20]:
                    lat = occ.get("decimalLatitude")
                    lon = occ.get("decimalLongitude")
                    if lat and lon:
                        locations.append({
                            "lat": lat,
                            "lon": lon,
                            "date": occ.get("eventDate"),
                            "locality": occ.get("locality", "Unknown")
                        })
                
                return {
                    "count": data.get("count", 0),
                    "locations": locations
                }
            return {"count": 0, "locations": []}
            
        except Exception as e:
            print(f"GBIF API error for {scientific_name}: {e}")
            return {"count": 0, "locations": []}
    
    @lru_cache(maxsize=100)
    def get_inaturalist_observations(self, scientific_name):
        """Fetch observations from iNaturalist for additional validation"""
        try:
            url = f"{self.inaturalist_base}/observations"
            params = {
                "taxon_name": scientific_name,
                "place_id": 7706,  # Sweden place ID
                "quality_grade": "research",
                "per_page": 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "count": data.get("total_results", 0),
                    "recent_observations": len(data.get("results", []))
                }
            return {"count": 0, "recent_observations": 0}
            
        except Exception as e:
            print(f"iNaturalist API error for {scientific_name}: {e}")
            return {"count": 0, "recent_observations": 0}

# Initialize API handler
bloom_api = BloomDataAPI()

# =========================
# NDVI API Integration
# =========================
def fetch_ndvi_for_year(year, region):
    ndvi_collection = ee.ImageCollection("NOAA/CDR/VIIRS/NDVI/V1") \
                        .filterDate(f'{year}-01-01', f'{year}-12-31') \
                        .select("NDVI")
    ndvi_image = ndvi_collection.mean().clip(region)
    ndvi_array = ndvi_image.sample(region, scale=10000).getInfo()
    
    points = []
    for feat in ndvi_array['features']:
        coords = feat['geometry']['coordinates']
        points.append({"lon": coords[0], "lat": coords[1], "ndvi": feat['properties']['NDVI']})
    return points

def predict_ndvi_trend(region, target_year):
    historical_years = list(range(2014, 2026))
    mean_ndvi_years = []
    for y in historical_years:
        img = ee.ImageCollection("NOAA/CDR/VIIRS/NDVI/V1") \
                .filterDate(f'{y}-01-01', f'{y}-12-31').select("NDVI").mean().clip(region)
        val = img.reduceRegion(ee.Reducer.mean(), region).getInfo()['NDVI']
        mean_ndvi_years.append(val if val is not None else np.nan)
    
    X = np.array([y for y, v in zip(historical_years, mean_ndvi_years) if v is not None]).reshape(-1, 1)
    y_vals = np.array([v for v in mean_ndvi_years if v is not None])
    model = LinearRegression().fit(X, y_vals)
    predicted = float(model.predict(np.array([[target_year]]))[0])
    return predicted, np.nanmean(mean_ndvi_years)

# =========================
# Flask Routes
# =========================
@app.route('/')
def home():
    return jsonify({
        "service": "PolliBloom + NDVI API",
        "version": "1.1",
        "description": "Real-time Swedish pollinator bloom data and NDVI maps",
        "endpoints": {
            "/api/plants": "Get all plants with live data",
            "/api/plant/<name>": "Get specific plant data",
            "/api/calendar": "Get bloom calendar view",
            "/api/gaps": "Analyze bloom gaps for pollinator support",
            "/api/ndvi?year=&bbox=": "Get NDVI points and predicted trend"
        }
    })

@app.route('/api/ndvi')
def get_ndvi():
    year = int(request.args.get("year", 2025))
    bbox = request.args.get("bbox")
    if bbox:
        minLon, minLat, maxLon, maxLat = map(float, bbox.split(","))
        region = ee.Geometry.Rectangle([minLon, minLat, maxLon, maxLat])
    else:
        region = ee.Geometry.Rectangle([11.0, 55.0, 24.0, 69.0])  # Sweden approx

    points = fetch_ndvi_for_year(year, region)
    predicted_ndvi, mean_ndvi = predict_ndvi_trend(region, year)
    
    return jsonify({
        "year": year,
        "bbox": bbox or "Sweden approx",
        "ndvi_points": points[:500],
        "mean_ndvi": mean_ndvi,
        "predicted_ndvi": predicted_ndvi,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/plants')
def get_all_plants():
    """Get all plants with real-time GBIF data"""
    plants_with_data = []
    
    for plant_id, plant_info in bloom_api.plants_db.items():
        scientific_name = plant_info["scientificName"]
        
        # Fetch real-time data
        gbif_data = bloom_api.get_gbif_data(scientific_name)
        inat_data = bloom_api.get_inaturalist_observations(scientific_name)
        
        plant_entry = {
            **plant_info,
            "id": plant_id,
            "bloomStart": plant_info["bloomMonths"][0],
            "bloomEnd": plant_info["bloomMonths"][-1],
            "gbifOccurrences": gbif_data["count"],
            "iNaturalistObs": inat_data["count"],
            "sampleLocations": gbif_data["locations"][:10],
            "dataFreshness": datetime.now().isoformat()
        }
        
        plants_with_data.append(plant_entry)
    
    return jsonify({
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "region": "Sweden",
            "plantCount": len(plants_with_data),
            "dataSource": "GBIF + iNaturalist APIs (real-time)"
        },
        "plants": plants_with_data
    })

@app.route('/api/plant/<plant_id>')
def get_plant_detail(plant_id):
    """Get detailed data for a specific plant"""
    if plant_id not in bloom_api.plants_db:
        return jsonify({"error": "Plant not found"}), 404
    
    plant_info = bloom_api.plants_db[plant_id]
    scientific_name = plant_info["scientificName"]
    
    # Fetch real-time data
    gbif_data = bloom_api.get_gbif_data(scientific_name)
    inat_data = bloom_api.get_inaturalist_observations(scientific_name)
    
    return jsonify({
        **plant_info,
        "id": plant_id,
        "gbifOccurrences": gbif_data["count"],
        "iNaturalistObs": inat_data["count"],
        "locations": gbif_data["locations"],
        "dataFreshness": datetime.now().isoformat()
    })

@app.route('/api/calendar')
def get_bloom_calendar():
    """Get bloom calendar organized by month"""
    calendar = {month: [] for month in range(1, 13)}
    
    for plant_id, plant_info in bloom_api.plants_db.items():
        for month in plant_info["bloomMonths"]:
            calendar[month].append({
                "id": plant_id,
                "commonName": plant_info["commonName"],
                "scientificName": plant_info["scientificName"],
                "color": plant_info["color"],
                "pollinators": plant_info["pollinators"]
            })
    
    return jsonify({
        "calendar": calendar,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/gaps')
def analyze_gaps():
    """Analyze bloom gaps and suggest plants to fill them"""
    monthly_coverage = {month: 0 for month in range(1, 13)}
    
    for plant_info in bloom_api.plants_db.values():
        for month in plant_info["bloomMonths"]:
            monthly_coverage[month] += 1
    
    # Find gaps (months with fewer than 3 blooming plants)
    gaps = [month for month, count in monthly_coverage.items() if count < 3]
    
    # Find best months (most diversity)
    best_months = sorted(monthly_coverage.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return jsonify({
        "monthlyCoverage": monthly_coverage,
        "gaps": gaps,
        "bestMonths": [{"month": m, "plantCount": c} for m, c in best_months],
        "recommendations": "Consider adding early spring or late autumn plants" if gaps else "Good coverage!",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🌸 Bloom Data API + NDVI API Server Starting...")
    print("📡 Fetching real-time data from GBIF, iNaturalist, and Earth Engine...")
    app.run(debug=True, port=5000)