# hivemind.exe
hivemind.exe repo for NASA Space Apps Challenge 2025

---
## BloomWatch: An Earth Observation Application for Global Flowering Phenology

Witness the pulse of life across our planet! From season to season and year to year, Earth’s vegetation is constantly changing, providing critical information on plant species, crops, seasonal effects, pollen sources, and changes in plant phenology (the relationship between seasonal changes and climate and biological phenomena in plants). Your challenge is to harness the power of NASA Earth observations to create a dynamic visual tool that displays and/or detects plant blooming events around the globe—just like pollinators do–and that advances solutions for monitoring, predicting, or managing vegetation. (Earth Science Division)

---
## Challenge Considerations
The temporal capability of NASA’s Earth observing satellites and the spatial resolution of the datasets used may impact the type of blooms that can be detected.
Your tool could:
    Be interactive, and zoom into specific locations.
    Show trends across time.
    Explain ecological and conservation implications.
    What decisions could your tool inform?


# 🌸 hivemind.exe

**An Earth Observation Application for Global Flowering Phenology**

[![NASA Space Apps Challenge 2025](https://img.shields.io/badge/NASA%20Space%20Apps-2025-blue)](https://www.spaceappschallenge.org/)
[![Earth Science](https://img.shields.io/badge/Category-Earth%20Science-green)](https://github.com/obymael/hivemind.exe)

> Witness the pulse of life across our planet! Track blooming events globally using NASA Earth observation data.

---

## 📖 About

hivemind.exe is a dynamic visual tool that harnesses NASA Earth observation data to monitor, detect, and visualize plant blooming events across the globe. From season to season and year to year, Earth's vegetation is constantly changing, providing critical information on plant species, crops, seasonal effects, pollen sources, and changes in plant phenology.

### The Challenge

This project was created for the **2025 NASA Space Apps Challenge** to address the hivemind.exe challenge: creating an application that displays and detects plant blooming events around the globe—just like pollinators do—and advances solutions for monitoring, predicting, or managing vegetation.

### Why It Matters

Tracking when, where, and how extensively plants bloom opens exciting possibilities:
- 🐝 Understanding relationships between plants, pollinators, and animals
- 🌾 Supporting beneficial crop management practices
- 🏥 Informing public health initiatives (pollen tracking)
- 🌍 Monitoring ecosystem productivity and nutrient cycles
- 🚜 Predicting agricultural pest spread
- 🌺 Detecting invasive species
- 📊 Tracking phenology changes due to climate

---

## 🛰️ Data Sources

hivemind.exe leverages NASA's powerful suite of satellites and airborne sensors:

- **Landsat** - Multispectral satellite imagery with extensive temporal archive
- **MODIS** - Moderate Resolution Imaging Spectroradiometer

---

## ✨ Features

- 🗺️ **Interactive Global Map** - Zoom into specific locations to explore bloom events
- 📈 **Temporal Trends** - Visualize blooming patterns across multiple years
- 🎯 **Bloom Detection** - Identify flowering events using spectral analysis
- 🌐 **Multi-Scale Analysis** - From local regions to global coverage
- 📊 **Ecological Insights** - Understand conservation implications
- 🔍 **Species Identification** - Potential inference of plant species from bloom characteristics
- ⏱️ **Real-time Monitoring** - Track current bloom events as they happen

---

## 🚀 Installation

### Prerequisites

Before installing hivemind.exe, ensure you have the following installed:

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **Python** (v3.8 or higher) - for data processing
- **Git**

### Step 1: Clone the Repository

```bash
git clone https://github.com/obymael/hivemind.exe.git
cd hivemind.exe
```

### Step 2: Install Dependencies

#### Frontend Dependencies
```bash
npm install
# or
yarn install
```

#### Backend Dependencies (if applicable)
```bash
cd backend
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### Step 3: Environment Configuration

Create a `.env` file in the root directory and add your API keys:

```env
# NASA Earthdata credentials (register at https://urs.earthdata.nasa.gov/)
NASA_EARTHDATA_USERNAME=your_username
NASA_EARTHDATA_PASSWORD=your_password

# Optional: Additional API keys for enhanced features
MAPBOX_ACCESS_TOKEN=your_mapbox_token
```

### Step 4: Data Setup

Download initial datasets (optional - application can fetch data on-demand):

```bash
npm run setup-data
```

---

## 💻 Usage

### Starting the Application Locally

#### Option 1: Development Mode

```bash
# Start the frontend development server
npm run dev

# In a separate terminal, start the backend (if applicable) 
cd backend
python app.py
```

The frontend will be available at `http://localhost:8080`
The backend will be available at `http://localhost:5000`

#### Option 2: Production Build

```bash
# Build the application
npm run build

# Start the production server
npm start
```

### Using the Application

1. **Select a Region**
   - Use the interactive map to navigate to your area of interest
   - Zoom in/out to adjust the scale of analysis

2. **Choose a Time Period**
   - Select date ranges to view bloom events
   - Compare multiple years to see trends

3. **Analyze Blooms**
   - Click on detected bloom areas to see detailed information
   - View spectral signatures and bloom characteristics
   - Export data for further analysis

4. **Explore Insights**
   - Read ecological implications for your selected region
   - View predictions and management recommendations
   - Access historical bloom data

### Example Workflows

#### Track Cherry Blossom Season
```
1. Navigate to Japan or Washington DC
2. Select March-April timeframe
3. Enable bloom detection layer
4. Compare across multiple years
```

#### Monitor Agricultural Crops
```
1. Select your farming region
2. Set current growing season dates
3. Track bloom progression for timing harvest
4. Access pest management insights
```

#### Study Climate Change Impact
```
1. Select a specific ecosystem
2. Compare bloom timing across 10+ years
3. Analyze phenology shift trends
4. Generate climate impact report
```

---

### Data & APIs
- NASA GIBS Earthdata API: Map satellite visualization
- NOAA NDVI datasets: Map vegetation index data
- iNaturalist API: Community of naturalists, scientists, and members of the public sharing over a million wildlife sightings
- Global Biodiversity Information Facility API: plant and pollinator data

---

## Use Cases

hivemind.exe serves multiple stakeholder groups:

- **Farmers & Agricultural Managers** - Optimize planting and harvest timing
- **Conservation Organizations** - Monitor ecosystem health and invasive species
- **Researchers** - Study phenology and climate change impacts
- **Public Health Officials** - Forecast pollen seasons for allergy alerts
- **Beekeepers** - Track nectar flow for hive management
- **Citizens and Educators** - Learn about local ecosystems and phenology

---

## License

This project is developed for the NASA Space Apps Challenge 2025. For contribution, the project uses the MIT License.

---

## Team

**hivemind.exe Team**

- Elin Forssell - Developer
- Julia McCall - Developer
- Karl Byland - Developer
- Lada

---
