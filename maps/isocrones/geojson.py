import asyncio
import pandas as pd
import json
import geojson
import requests

async def rate_limiter(requests_per_minute):
    interval = 60 / requests_per_minute
    await asyncio.sleep(interval)

async def fetch_geojson(lat, lng):
    print(f"Fetching GeoJSON for coordinates: {lat}, {lng}")
    url = "https://api.traveltimeapp.com/v4/time-map"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Application-Id': app_id,
        'X-Api-Key': api_key
    }
    payload = {
        "departure_searches": [
            {
                "id": f"store_{lat}_{lng}",
                "coords": {
                    "lat": lat,
                    "lng": lng
                },
                "departure_time": "2024-07-24T18:30:00",
                "travel_time": 600,
                "transportation": {
                    "type": "driving"
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

async def create_geojson_file(data_frame):
    features = []
    count = 0
    for index, row in data_frame.iterrows():
        # if count == 5:
        #     break
        store_id = row['Store ID']
        lat = row['Latitude']
        lng = row['Longitude']
        color = row['Color']

        # Fetch GeoJSON
        geojson_data = await fetch_geojson(lat, lng)

        # Rate limiting
        await rate_limiter(50)

        # Add GeoJSON to features list
        for result in geojson_data['results']:
            for shape in result['shapes']:
                shell = shape['shell']
                coordinates = [[point['lng'], point['lat']] for point in shell]  # Note the swap for GeoJSON format
                # print(coordinates)
                feature = {
                    "type": "Feature",
                    "properties": {
                        "store_id": store_id,
                        "lat": lat,
                        "lng": lng,
                        "color": color,
                        "seller_name": row['Seller Name'],
                        "seller_address": row['Address'],
                        "sales": row['Sales']
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coordinates]
                    }
                }
                features.append(feature)
                print(f"Added isochrone for store: {store_id}")
                break
        # count += 1

    # Create GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Save GeoJSON to file
    geojson_file_path = 'store_polygons.geojson'
    with open(geojson_file_path, 'w') as f:
        json.dump(geojson_data, f)

async def main():
    global app_id, api_key
    app_id = "99485a68"
    api_key = "454aa5730ac1e85d608fbaf98cf3344e"

    # Load Excel file
    file_path = 'geo.xlsx'
    df = pd.read_excel(file_path)

    # Create GeoJSON file
    await create_geojson_file(df)

if __name__ == "__main__":
    asyncio.run(main())
