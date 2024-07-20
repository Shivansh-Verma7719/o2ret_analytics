import folium

# Data for the placemark
placemark_data = {
    'coordinates': [28.63290701515694, 77.22152955820528],
    'placemark_color': 'orange',
    'popup': 'Dark Store 1'
}

# Create a map centered at the specified location
m = folium.Map(location=placemark_data['coordinates'],
    zoom_start=12,
    tiles="https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}",
    attr="Google maps",
)

# Add the placemark
folium.Marker(
    location=placemark_data['coordinates'],
    icon=folium.Icon(color='red', icon='tv', prefix='fa'),
    popup=placemark_data['popup']
).add_to(m)

# Save the map
map_path = 'dark_store_map.html'
m.save(map_path)

map_path
