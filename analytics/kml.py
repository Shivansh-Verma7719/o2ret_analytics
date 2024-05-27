import csv

# Read the data from a CSV file or any other data source
data_file = 'data.csv'

# Template KML file with placeholders
template_kml_file = 'template.kml'

# Output KML file with actual values
output_kml_file = 'output.kml'

# Read data from CSV file
data = {}
with open(data_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pincode = row['PINCODE']
        data[pincode] = row

# Read the template KML file
with open(template_kml_file, 'r') as file:
    kml_content = file.read()

# Replace placeholders with actual values
for pincode, values in data.items():
    kml_content = kml_content.replace(f'<SimpleData name="PINCODE">{pincode}</SimpleData>', 
                                      f'<SimpleData name="PINCODE">{pincode}</SimpleData>'
                                      f'<SimpleData name="Total - Adjusted average household size">{values["Total - Adjusted average household size"]}</SimpleData>'
                                      f'<SimpleData name="Pincode Prosperity Score">{values["Pincode Prosperity Score"]}</SimpleData>'
                                      f'<SimpleData name="Married Couples per household">{values["Married Couples per household"]}</SimpleData>'
                                      f'<SimpleData name="Rural - Adjusted average household size">{values["Rural - Adjusted average household size"]}</SimpleData>'
                                      f'<SimpleData name="Rural - Pincode Prosperity Score">{values["Rural - Pincode Prosperity Score"]}</SimpleData>'
                                      f'<SimpleData name="Rural - Married Couples per household">{values["Rural - Married Couples per household"]}</SimpleData>'
                                      f'<SimpleData name="Urban - Adjusted average household size">{values["Urban - Adjusted average household size"]}</SimpleData>'
                                      f'<SimpleData name="Urban - Pincode Prosperity Score">{values["Urban - Pincode Prosperity Score"]}</SimpleData>'
                                      f'<SimpleData name="Urban - Married Couples per household">{values["Urban - Married Couples per household"]}</SimpleData>'
                                      f'<SimpleData name="Final Relevant Market Size (Total)">{values["Final Relevant Market Size (Total)"]}</SimpleData>'
                                      f'<SimpleData name="Final Relevant Market Size (Male)">{values["Final Relevant Market Size (Male)"]}</SimpleData>'
                                      f'<SimpleData name="Final Relevant Market Size (Female)">{values["Final Relevant Market Size (Female)"]}</SimpleData>'
                                      f'<SimpleData name="Unweighted Pincode Relevant Population Density">{values["Unweighted Pincode Relevant Population Density"]}</SimpleData>'
                                      f'<SimpleData name="Product Awareness Based on Education (Total)">{values["Product Awareness Based on Education (Total)"]}</SimpleData>'
                                      f'<SimpleData name="Product Awareness Based on Education (Male)">{values["Product Awareness Based on Education (Male)"]}</SimpleData>'
                                      f'<SimpleData name="Product Awareness Based on Education (Female)">{values["Product Awareness Based on Education (Female)"]}</SimpleData>'
                                      f'<SimpleData name="Blinkit Availability">{values["Blinkit Availability"]}</SimpleData>'
                                      f'<SimpleData name="Vishal Mega Mart Availability">{values["Vishal Mega Mart Availability"]}</SimpleData>'
                                      f'<SimpleData name="Apollo Availability">{values["Apollo Availability"]}</SimpleData>'
                                      f'<SimpleData name="General Popularity on Online Storefronts">{values["General Popularity on Online Storefronts"]}</SimpleData>'
                                      f'<SimpleData name="Sales">{values["Sales"]}</SimpleData>'
                                      f'<SimpleData name="Serviceability of Pincode (Discrete, Yes/No)">{values["Serviceability of Pincode (Discrete, Yes/No)"]}</SimpleData>'
                                      f'<SimpleData name="Online Sales">{values["Online Sales"]}</SimpleData>'
                                      f'<SimpleData name="Market Penetration">{values["Market Penetration"]}</SimpleData>'
                                      f'<SimpleData name="Expansion Score">{values["Expansion Score"]}</SimpleData>')

# Write the updated KML content to a new file
with open(output_kml_file, 'w') as file:
    file.write(kml_content)
