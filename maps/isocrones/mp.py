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
    market_penetration = additional_data.get('Market Penetration', 'N/A')
    market_size = additional_data.get('Total Population', 'N/A')
    pop_density = additional_data.get('Population Density', 'N/A')

    popup_content = f"""
        <div style="background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Store ID:</strong> {store_id}<br>
            <strong>Seller Name:</strong> {seller_name}<br>
            <strong>Sales:</strong> {round(sales, 3)}<br>
            <strong>Market Penetration:</strong> {round(market_penetration, 3)}<br>
            <strong>Market Size:</strong> {market_size}<br>
            <strong>Population Density:</strong> {pop_density}
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

    # Define the style function within this scope
    def style_function(feature):
        store_id = feature['properties']['store_id']
        color = additional_data_dict.get(store_id, {}).get('Color', 'blue')
        return {
            'fillColor': color,
            'color': color,
            'weight': 1,
            'fillOpacity': 0.5,
        }

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
    add_geojson_layer(m, geojson_paths[0][0], geojson_paths[0][1], additional_data_dict, add_markers=True, show=True)

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
excel_path = 'mp.xlsx'

# Create map and save GeoJSON
create_map_with_data(geojson_paths, excel_path)
