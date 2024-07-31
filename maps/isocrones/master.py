import folium
import json
import pandas as pd
from folium.plugins import BeautifyIcon
from folium.plugins import MarkerCluster
from folium.plugins import Search

# Load the Excel file
excel_path = 'geo.xlsx'
store_data = pd.read_excel(excel_path)

def get_store_data(store_id):
    # Find the row in the DataFrame with the given store_id
    store_row = store_data[store_data['Store ID'] == store_id].iloc[0]
    return store_row

def create_popup_content(store_id):
    # Extract the store data
    store_row = get_store_data(store_id)
    
    popup_content = f"""
        <div id="popup">
        <div style="background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Store ID:</strong> {store_row['Store ID']}<br>
            <strong>Seller Name:</strong> {store_row['Seller Name']}<br>
            <strong>Sales:</strong> {round(store_row['Sales'], 3)}<br>
            <strong>Expansion Score:</strong> {store_row['Expansion Score']}<br>
            <strong>What to Sell:</strong> {store_row['What to Sell']}<br>
            <strong>WWH:</strong> {store_row['WWH']}<br>
            <strong>Summary:</strong> {store_row['Summary']}<br>
            <strong>Outliers:</strong> {store_row['Outliers']}<br>
            <strong>Segment:</strong> {store_row['Segment']}<br>
            <button onclick="showSecondaryPopup('{store_id}')" id="why-btn">Why?</button>
        </div>
        <div id="{store_id}-secondary-popup" style="display:none; background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Area of Pincode:</strong> {store_row['Area of pincode']}<br>
            <strong>Total Population:</strong> {store_row['Total Population']}<br>
            <strong>Male Population:</strong> {store_row['Male Population']}<br>
            <strong>Female Population:</strong> {store_row['Female Population']}<br>
            <strong>Population Density:</strong> {store_row['Population Density']}<br>
            <strong>Prosperity Index:</strong> {store_row['Prosperity Index']}<br>
            <strong>Market Penetration:</strong> {round(store_row['Market Penetration'],3)}<br>
        </div>
        </div>
    """
    return popup_content

def create_tooltip_content(store_id):
    tooltip_content = f"""
        <div style="background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Store ID:</strong> {store_id}<br>
        </div>
    """
    return tooltip_content

def style_function(feature):
    return {
        'fillColor': feature['properties']['color'],
        'color': feature['properties']['color'],
        'weight': 1,
        'fillOpacity': 0.5,
    }

def highlight_function(feature):
    return {
        'color': 'black',
        'weight': 3,
        'fillOpacity': 0.5,
        'line_opacity': 1,
    }

def add_geojson_layer(m, geojson_path, layer_name, show=True):
    # Load GeoJSON file
    with open(geojson_path) as f:
        data = json.load(f)
    if layer_name == '9 AM Data':
        show = True

    geojson_layer = folium.FeatureGroup(name=layer_name, show=show)

    for feature in data['features']:
        # Extract properties
        properties = feature['properties']
        store_id = properties['store_id']
        seller_name = properties['seller_name']
        sales = properties['sales']
        lat = properties['lat']
        lng = properties['lng']
        
        # Add GeoJSON layer to the map
        folium.GeoJson(
            feature,
            style_function=style_function,
            highlight_function=highlight_function,
            popup=folium.Popup(create_popup_content(store_id)),
            zoom_on_click=True,
            tooltip=folium.GeoJsonTooltip(
                fields=['store_id'],
                aliases=['Store ID'],
                style='background-color: #003f98; color: white; border-radius: 5px; padding: 10px;'
            )
        ).add_to(geojson_layer)

    m.add_child(geojson_layer)

def create_map_with_data(geojson_paths):
    # Create a folium map object
    m = folium.Map(location=[23.03157589546863, 72.47071340245118], zoom_start=12)

    # Add base layers
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", 
        attr="Google", 
        name="Google Satellite"
    ).add_to(m)
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", 
        attr="Google", 
        name="Google Maps"
    ).add_to(m)

    # Traverse all features in 9am geojson and create a lat long list
    lat_lng_list = []
    with open('9am.geojson') as f:
        data = json.load(f)

    lat_lng_list = []
    for feature in data['features']:
        properties = feature['properties']
        lat = properties['lat']
        lng = properties['lng']
        store_id = properties['store_id']
        seller_name = properties['seller_name']
        sales = properties['sales']
        lat_lng_list.append([lat, lng, store_id, seller_name, sales])

    # Create a marker cluster
    marker_cluster = MarkerCluster(name='Markers').add_to(m)

    # Add markers to the marker cluster
    for lat, lng, store_id, seller_name, sales in lat_lng_list:
        folium.Marker(
            location=[lat, lng],
            popup=folium.Popup(create_popup_content(store_id)),
            icon=folium.Icon(color='blue', icon='store', prefix='fa'),
            tooltip=create_tooltip_content(store_id),
            title=store_id,
        ).add_to(marker_cluster)

    # Add GeoJSON layers without markers for other times, default to hidden
    for geojson_path, layer_name in geojson_paths:
        add_geojson_layer(m, geojson_path, layer_name, show=False)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Inject custom CSS
    css = f'''
    <link rel="stylesheet" type="text/css" href="custom_layer_control.css"/>
    <script>
            function showSecondaryPopup(storeId) {{
                var popup = document.getElementById(storeId + '-secondary-popup');
                popup.style.display = popup.style.display === 'none' ? 'block' : 'none';
            }}
        </script>
    '''
    m.get_root().header.add_child(folium.Element(css))

    search = Search(
        layer=marker_cluster,
        search_label='title',
        placeholder='Search for Store ID',
        collapsed=False
    ).add_to(m)

    # Save map as HTML
    map_path = 'store_map.html'
    m.save(map_path)

# Specify the paths of the GeoJSON files
geojson_paths = [
    ('9am.geojson', '9 AM Data'),
    ('1pm.geojson', '1 PM Data'),
    ('6pm.geojson', '6 PM Data')
]

# Create map and save GeoJSON
create_map_with_data(geojson_paths)
