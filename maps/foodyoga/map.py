import pandas as pd
import folium

# Read the Excel file
data = pd.read_excel('yoga.xlsx')

# Create a map object
map = folium.Map(location=[data['lat'].mean(), data['lng'].mean()], zoom_start=10)

def create_popup_content(row):
    popup_content = f"""
        <div id="popup">
        <div style="background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Name:</strong> {row['name']}<br>
            <strong>Address:</strong> {row['address']}<br>
            <strong>Phone:</strong> {row['phone']}<br>
            <strong>Email:</strong> {row['email']}<br>
            <strong>URL:</strong> <a href="{row['url']}">{row['url']}</a><br>
            <strong>Facebook Profile:</strong> <a href="{row['Facebook Profile']}">{row['Facebook Profile']}</a><br>
            <strong>Instagram Handle:</strong><a href="{row['Instagram Handle']}">{row['Instagram Handle']}</a><br>
            <strong>LinkedIn:</strong> <a href="{row['LinkedIn']}">{row['LinkedIn']}</a><br>
            <strong>Twitter:</strong> <a href="{row['Twitter']}">{row['Twitter']}</a><br>
            <strong>YouTube:</strong> <a href="{row['YouTube']}">{row['YouTube']}</a><br>
            <br/>
            <strong>Primary Category:</strong> {row['primary_category_name']}<br>
            <strong>Category:</strong> {row['category_name']}<br>
            <strong>GTM Score:</strong> {int(row['Grading score'])}<br>
            <strong>Radius:</strong> {int(row['Radius'])} km<br>
            <strong>What to Sell:</strong> {row['What to sell']}<br>
            <strong>Insight:</strong> {row['Insight']}<br>
            <strong>Summary:</strong> {row['Summary']}<br>
            <button onclick="showSecondaryPopup('{row['zip']}')" id="why-btn">Why?</button>
        </div>
        <div id="{row['zip']}-secondary-popup" style="display:none; background-color: #003f98; padding: 10px; border-radius: 5px; color: white;">
            <strong>Total Population:</strong> {row['Total population']}<br>
            <strong>Male Population:</strong> {row['Male population']}<br>
            <strong>Female Population:</strong> {row['Female Population']}<br>
            <strong>Median Income:</strong> {row['Median Income']}<br>
            <strong>Mean Income:</strong> {row['Mean Income']}<br>
            <strong>Star Count:</strong> {row['star_count']}<br>
            <strong>Rating Count:</strong> {row['rating_count']}<br>
        </div>
        </div>
    """
    return popup_content

# Function to convert kilometers to pixels
def km_to_pixels(radius_km, zoom_level):
    # Approximate pixel conversion factor for map zoom levels
    scale = 2 ** (15 - zoom_level)
    return radius_km * 1000 / scale  # Conversion factor to convert km to pixels

# Add circle markers for each location
for index, row in data.iterrows():
    radius_km = row['Radius']
    folium.Circle(
        location=[row['lat'], row['lng']],
        radius=radius_km*1000,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(folium.Html(create_popup_content(row), script=True), max_width=700)
    ).add_to(map)

    folium.Marker(
    location=[row['lat'], row['lng']],
    icon=folium.Icon(color='red', icon='store', prefix='fa'),
    popup=folium.Popup(folium.Html(create_popup_content(row), script=True), max_width=700)
    ).add_to(map)


css = f'''
    <link rel="stylesheet" type="text/css" href="styles.css"/>
    <script>
            function showSecondaryPopup(storeId) {{
                var popup = document.getElementById(storeId + '-secondary-popup');
                popup.style.display = popup.style.display === 'none' ? 'block' : 'none';
            }}
        </script>
    '''
folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", 
        attr="Google", 
        name="Google Maps"
    ).add_to(map)
map.get_root().header.add_child(folium.Element(css))
# Save the map as an HTML file
map.save('map.html')
