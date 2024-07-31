import folium
import json
import pandas as pd
from folium.plugins import BeautifyIcon
# Function to read the Excel file and return a dictionary with store IDs as keys
def read_excel_data(excel_path):
    df = pd.read_excel(excel_path)
    data_dict = df.set_index('Store ID').to_dict(orient='index')
    return data_dict

# Updated create_popup_content function
def create_popup_content(store_id, seller_name, sales, additional_data):
    product1 = additional_data.get('Most discounted product 1', 'N/A')
    product2 = additional_data.get('Most discounted product 2', 'N/A')
    product3 = additional_data.get('Most discounted product 3', 'N/A')
    aov = additional_data.get('Branded search AOV', 'N/A')
    search_share_pack = additional_data.get('Branded search share of pack', 'N/A')
    search_share_bar = additional_data.get('Branded search share of bar', 'N/A')
    comp_aov = additional_data.get('Generic search competitor AOV', 'N/A')
    yoga_aov = additional_data.get('Generic search AOV of Yoga Bar', 'N/A')
    comp_share = additional_data.get('Generic search competitor share', 'N/A')
    yoga_share = additional_data.get('Generic search Yoga Bar share', 'N/A')

    popup_content = f"""
        <div style="background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Store ID:</strong> {store_id}<br>
            <strong>Seller Name:</strong> {seller_name}<br>
            <strong>Sales:</strong> {round(sales, 3)}<br>
            <strong>Most Discounted Product 1:</strong> {product1}<br>
            <strong>Most Discounted Product 2:</strong> {product2}<br>
            <strong>Most Discounted Product 3:</strong> {product3}<br>
            <strong>Branded Search AOV:</strong> {aov}<br>
            <strong>Branded Search Share of Pack:</strong> {search_share_pack}<br>
            <strong>Branded Search Share of Bar:</strong> {search_share_bar}<br>
            <strong>Generic Search Competitor AOV:</strong> {comp_aov}<br>
            <strong>Generic Search AOV of Yoga Bar:</strong> {yoga_aov}<br>
            <strong>Generic Search Competitor Share:</strong> {comp_share}<br>
            <strong>Generic Search Yoga Bar Share:</strong> {yoga_share}<br>
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

# Update the add_geojson_layer function
def add_geojson_layer(m, geojson_path, layer_name, additional_data_dict, add_markers=True, show=True):
    # Load GeoJSON file
    with open(geojson_path) as f:
        data = json.load(f)

    geojson_layer = folium.FeatureGroup(name=layer_name, show=show)

    for feature in data['features']:
        # Extract properties
        properties = feature['properties']
        store_id = properties['store_id']
        seller_name = properties['seller_name']
        sales = properties['sales']
        lat = properties['lat']
        lng = properties['lng']

        # Get additional data for the store ID
        additional_data = additional_data_dict.get(store_id, {})

        if add_markers:
            # Create a marker
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(create_popup_content(store_id, seller_name, sales, additional_data), max_width=300),
                icon=folium.Icon(color='red', icon='store', prefix='fa'),
                tooltip=create_tooltip_content(store_id)
            ).add_to(m)
        
        # Add GeoJSON layer to the map
        folium.GeoJson(
            feature,
            style_function=style_function,
            highlight_function=highlight_function,
            popup=folium.Popup(create_popup_content(store_id, seller_name, sales, additional_data), max_width=300),
            zoom_on_click=True,
            tooltip=folium.GeoJsonTooltip(
                fields=['store_id'],
                aliases=['Store ID'],
                style='background-color: #003f98; color: white; border-radius: 5px; padding: 10px;'
            )
        ).add_to(geojson_layer)

    m.add_child(geojson_layer)

def create_map_with_data(geojson_paths, excel_path):
    # Read additional data from Excel file
    additional_data_dict = read_excel_data(excel_path)

    # Create a folium map object
    m = folium.Map(location=[23.03157589546863, 72.47071340245118], zoom_start=7)

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

    # Add markers and GeoJSON layer for 9 AM data
    add_geojson_layer(m, geojson_paths[0][0], geojson_paths[0][1], additional_data_dict, add_markers=True, show=False)

    # Add GeoJSON layers without markers for other times, default to hidden
    for geojson_path, layer_name in geojson_paths[1:]:
        add_geojson_layer(m, geojson_path, layer_name, additional_data_dict, add_markers=False, show=False)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Inject custom CSS
    css = '<link rel="stylesheet" type="text/css" href="custom_layer_control.css"/>'
    m.get_root().html.add_child(folium.Element(css))

    # Save map as HTML
    map_path = 'store_map.html'
    m.save(map_path)

# Specify the paths of the GeoJSON files and the Excel file
geojson_paths = [
    ('9am.geojson', '9 AM Data'),
    ('1pm.geojson', '1 PM Data'),
    ('6pm.geojson', '6 PM Data')
]
excel_path = 'blinkit.xlsx'

# Create map and save GeoJSON
create_map_with_data(geojson_paths, excel_path)
