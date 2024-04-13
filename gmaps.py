import csv
import re
from helper.pincode import get_pincode
from helper.popularity import get_popularity

# Define a function to read and parse the CSV file
def parse_csv(filename):
    data = []  # List to store parsed data
    
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        
        for row in reader:
            brand_name = row[0]
            product_name = row[1]
            price = row[2]
            distributor_name = row[3]
            serviceable_areas_str = row[4]
            serviceable_areas_str = serviceable_areas_str.replace('-', ',')
            serviceable_areas = re.findall(r'\w+\s*\w*', serviceable_areas_str)            
            past_sales = int(row[5])
            past_returns = int(row[6])
            
            # Create a dictionary to represent each product
            product = {
                "Brand Name": brand_name,
                "Product Name": product_name,
                "Price": price,
                "Distributor Name": distributor_name,
                "Serviceable Areas": serviceable_areas,
                "Past Sales": past_sales,
                "Past Returns": past_returns
            }
            
            data.append(product)  # Append the product dictionary to the data list
    
    return data

def get_pincode_for_serviceable_areas(data):

    pincode_data = []
    for area in data:
        pincode = get_pincode(area)
        
        # Create a dictionary to represent each pincode
        pincode_entry = {
            "Area": area,
            "Pincode": pincode['pincode'],
            "District": pincode['district']
        }
        
        pincode_data.append(pincode_entry)  # Append the pincode dictionary to the pincode_data list
    
    return pincode_data

def get_popularity_score(data):
    for product in data:
        popularity_score = get_popularity(product['Product Name'], {'sales': product['Past Sales'], 'returns': product['Past Returns']})
        product['Popularity Score'] = popularity_score

    return data

filename = 'data.csv' 
parsed_data = parse_csv(filename)

pincode_data = get_pincode_for_serviceable_areas(parsed_data[0]['Serviceable Areas'])

data={
    
    'sales': parsed_data[0]['Past Sales'],
    'returns': parsed_data[0]['Past Returns']
}
popularity_scored_data = get_popularity_score(parsed_data)


