<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Tourist Guide Map</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script src="Municipalities.js"></script>
    <script src="province.js"></script>
    <script src="District.js"></script>
    
    <style>
        #map {
            height: 500px;
            width: 100%;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center my-4">Interactive Tourist Guide Map</h1>
        <div id="map"></div>
    </div>
    <script>
        // Initialize the map
        var map = L.map('map').setView([27.7172, 85.3240], 13); // Kathmandu
    
        // Define base layers
        var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        });
    
        var satelliteLayer = L.tileLayer('https://{s}.sat.ortho.tiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: '© Esri Imagery'
        });
    
        var terrainLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
            attribution: '© OpenTopoMap contributors'
        });
    
        // Add a default base layer
        osmLayer.addTo(map);
    
        // Define overlay for weather
        var weatherStations = L.layerGroup().addTo(map);
    
        // Weather toggle control
        let weatherEnabled = false;
    
        // Add layer to control weather
        map.on('overlayadd', function (eventLayer) {
            if (eventLayer.name === 'Weather Stations') {
                weatherEnabled = true;
                alert('Weather data enabled. Click the map to fetch weather data.');
            }
        });
    
        map.on('overlayremove', function (eventLayer) {
            if (eventLayer.name === 'Weather Stations') {
                weatherEnabled = false;
            }
        });
    
        // Fetch weather data
        async function fetchWeatherData(lat, lon) {
            const apiKey = 'e569c26e83e607eb7de26e5f88115100';
            const apiUrl = `https://api.openweathermap.org/data/2.5/weather`;
    
            try {
                const response = await axios.get(apiUrl, { params: { lat, lon, appid: apiKey, units: 'metric' } });
                const { description } = response.data.weather[0];
                const { temp, humidity } = response.data.main;
                return { description, temp, humidity };
            } catch (error) {
                console.error('Error fetching weather data:', error);
                return null;
            }
        }
    
        // Map click event for weather data
        map.on('click', async (e) => {
            if (!weatherEnabled) return; // Exit if weather is disabled
    
            const { lat, lng } = e.latlng;
            const weather = await fetchWeatherData(lat, lng);
    
            if (weather) {
                const popup = L.popup()
                    .setLatLng([lat, lng])
                    .setContent(`
                        <strong>Weather:</strong> ${weather.description}<br>
                        <strong>Temperature:</strong> ${weather.temp}°C<br>
                        <strong>Humidity:</strong> ${weather.humidity}%
                    `)
                    .openOn(map);
    
                // Add the popup to weatherStations layer group for visibility toggle
                weatherStations.addLayer(L.marker([lat, lng]).bindPopup(popup));
            } else {
                alert('Failed to fetch weather data. Please try again.');
            }
        });
       
        const municipalitiesLayer = L.geoJSON(Municipalities, {
            style: () => ({ color: "yellow", weight: 2, fillOpacity: 0.1 }),
            onEachFeature: (feature, layer) => {
                const { LOCAL } = feature.properties;
                layer.bindPopup(`Local Municipality: ${LOCAL}`);
            }
        });

        const provinceLayer = L.geoJSON(Province, {
            style: () => ({ color: "green", weight: 2, fillOpacity: 0.1 }),
            onEachFeature: (feature, layer) => {
                const { PROVINCE_NAME } = feature.properties;
                layer.bindPopup(`Province Name: ${PROVINCE_NAME}`);
            }
        });

        const districtLayer = L.geoJSON(District, {
            style: () => ({ color: "grey", weight: 2, fillOpacity: 0.1 }),
            onEachFeature: (feature, layer) => {
                const { DISTRICT } = feature.properties;
                layer.bindPopup(`District Name: ${DISTRICT}`);
            }
        });
    
        // Combine base layers and overlays in a single control
        var baseMaps = {
            "OpenStreetMap": osmLayer,
            "Satellite": satelliteLayer,
            "Terrain": terrainLayer
        };
    
        var overlays = {
            "Weather Stations": weatherStations,
            "Municipalities": municipalitiesLayer,
            "Provinces": provinceLayer,
            "Districts": districtLayer
        };
        
    
        // Add layer control to the map
        L.control.layers(baseMaps, overlays).addTo(map);
    </script>
    
    
</body>
</html>
