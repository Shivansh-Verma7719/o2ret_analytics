import requests
import openpyxl
import folium
import json

# Load pincode to color mapping from Excel file
color_mapping_file = 'pincode_market_penetration_color_mapping.xlsx'
color_wb = openpyxl.load_workbook(color_mapping_file)
color_sheet = color_wb.active

# Create a dictionary to map pincode to hex color
pincode_color_mapping = {}
for row in color_sheet.iter_rows(min_row=2, values_only=True):
    pincode, mp, hex_color = row
    pincode_color_mapping[str(pincode).replace(",", "")] = hex_color

# Define coordinates of where we want to center our map
boulder_coords = [28.6815, 77.2228]

# Create the map
my_map = folium.Map(location=boulder_coords, zoom_start=10)

# Load GeoJSON data
with open('style.json') as f:
    geo_json_data = json.load(f)

# Create a function to style the features
def style_function(feature):
    pincode = feature['properties']['Pincode']
    fill_color = pincode_color_mapping.get(pincode)
    return {
        'fillColor': fill_color,
        'color': fill_color,
        'weight': 1,
        'fillOpacity': 0.8,
        'line_opacity': 0.9,
    }

# Create a function to highlight the features on click
def highlight_function(feature):
    return {
        'color': 'black',
        'weight': 5,
        'fillOpacity': 0.8,
        'line_opacity': 1,
    }

# Function to create popup content
def create_popup(feature):
    props = feature['properties']
    popup_content = f"""
    <div style="font-size: 10px;">
        <b>PT_ID:</b> {props['PT_ID']}<br>
        <b>Pincode:</b> {props['Pincode']}<br>
        <b>Name:</b> {props['name']}<br>
        <b>State:</b> {props['State']}<br>
        <b>Relevant Market Size:</b> {props['Relevant Market Size']}<br>
        <b>Male Percentage:</b> {props['Relevant Market Male Percentage']}<br>
        <b>Female Percentage:</b> {props['Relevant Market Women Percentage']}<br>
        <b>Area:</b> {props['Area']}<br>
        <b>Population Density:</b> {props['Population Density']}<br>
        <b>Total Literacy:</b> {props['Total Literacy']}<br>
        <b>Total 12 Pass:</b> {props['Total 12 Pass']}<br>
        <b>Total Graduate:</b> {props['Total Graduate']}<br>
        <b>Male Literacy:</b> {props['Male Literacy']}<br>
        <b>Male 12 Pass:</b> {props['Male - 12 Pass']}<br>
        <b>Male Graduate:</b> {props['Male - 12 Graduate']}<br>
        <b>Female Literacy:</b> {props['Female Literacy']}<br>
        <b>Female 12 Pass:</b> {props['Female 12 Pass']}<br>
        <b>Female Graduate:</b> {props['Female Graduate']}<br>
        <b>Literacy Index:</b> {props['Literacy Index']}<br>
        <b>12 Pass Index:</b> {props['12 Pass Index']}<br>
        <b>Graduate Index:</b> {props['Graduate Index']}<br>
        <b>PinCode Awareness:</b> {props['PinCode Awareness']}<br>
        <b>Blinkit Availability:</b> {props['Blinkit Availability']}<br>
        <b>Vishal Mega Mart Availability:</b> {props['Vishal Mega Mart Availability']}<br>
        <b>Apollo Availability:</b> {props['Apollo Availability']}<br>
        <b>General Popularity on Online Storefronts:</b> {props['General Popularity on Online Storefronts']}<br>
        <b>Sales:</b> {props['Sales']}<br>
        <b>Serviceability of Pincode:</b> {props['Serviceability of Pincode (Discrete, Yes/No)']}<br>
        <b>Online Sales:</b> {props['Online Sales']}<br>
        <b>Market Penetration:</b> {props['Market Penetration']}<br>
        <b>Expansion Score:</b> {props['Expansion Score']}<br>
    </div>
    """
    return folium.Popup(popup_content, max_width=300)

# Add GeoJSON layer with popups and highlight function
for feature in geo_json_data['features']:
    popup = create_popup(feature)
    folium.GeoJson(
        feature,
        style_function=style_function,
        highlight_function=highlight_function,
        popup=popup,
        tooltip=folium.GeoJsonTooltip(
            fields=['Pincode', 'State', 'Sales'],
            aliases=['Pincode:', 'State:', 'Sales'],
            localize=True
        )
    ).add_to(my_map)

# Save the map as an HTML string
map_html = my_map.get_root().render()

# Write the HTML string to a file
with open('sales_heatmap.html', 'w') as f:
    f.write(map_html)

print("Map with heatmap saved to 'sales_heatmap.html'")
