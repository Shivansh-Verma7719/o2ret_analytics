import csv

def convert_to_kml():
    # Read the data from a CSV file or any other data source
    data_file = 'data.csv'

    # Template KML file with placeholders
    template_kml_file = 'kml/delhi-pincode.kml'

    # Output KML file with actual values
    output_kml_file = 'output.kml'

    # Read data from CSV file
    data = {}
    with open(data_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pincode = row['Pincode']
            data[pincode] = row

    # for pincode, values in data.items():
    #     print(pincode, values)

    # Read the template KML file
    with open(template_kml_file, 'r') as file:
        kml_content = file.read()

    # Replace placeholders with actual values
    for pincode, values in data.items():
        kml_content = kml_content.replace(f'<SimpleData name="PINCODE">{pincode}</SimpleData>',
                                        f'<SimpleData name="Pincode">{pincode}</SimpleData>\n'
                                        f'<SimpleData name="name">{pincode}</SimpleData>\n'
                                        f'<SimpleData name="State">Delhi</SimpleData>\n'
                                        f'<SimpleData name="Total - Adjusted average household size">{values["Total- Adjusted average household size"]}</SimpleData>\n'
                                        f'<SimpleData name="Pincode Prosperity Score">{values["Total- Prosperity Score"]}</SimpleData>\n'
                                        f'<SimpleData name="Married Couples per household">{values["Total- Married Couples per household"]}</SimpleData>\n'
                                        f'<SimpleData name="Rural - Adjusted average household size">{values["Rural- Adjusted average household size"]}</SimpleData>\n'
                                        f'<SimpleData name="Rural - Pincode Prosperity Score">{values["Rural- Prosperity Score"]}</SimpleData>\n'
                                        f'<SimpleData name="Rural - Married Couples per household">{values["Rural- Married Couples per household"]}</SimpleData>\n'
                                        f'<SimpleData name="Urban - Adjusted average household size">{values["Urban- Adjusted average household size"]}</SimpleData>\n'
                                        f'<SimpleData name="Urban - Pincode Prosperity Score">{values["Urban- Prosperity Score"]}</SimpleData>\n'
                                        f'<SimpleData name="Urban - Married Couples per household">{values["Urban- Married Couples per household"]}</SimpleData>\n'
                                        f'<SimpleData name="Final Relevant Market Size (Total)">{values["Final Relevant Market Size (Total)"]}</SimpleData>\n'
                                        f'<SimpleData name="Final Relevant Market Size (Male)">{values["Final Relevant Market Size (Male)"]}</SimpleData>\n'
                                        f'<SimpleData name="Final Relevant Market Size (Female)">{values["Final Relevant Market Size (Female)"]}</SimpleData>\n'
                                        f'<SimpleData name="Unweighted Pincode Relevant Population Density">{values["Unweighted Pincode Relevant Population Density"]}</SimpleData>\n'
                                        f'<SimpleData name="Product Awareness Based on Education (Total)">{values["Product Awareness Based on Education (Total)"]}</SimpleData>\n'
                                        f'<SimpleData name="Product Awareness Based on Education (Male)">{values["Product Awareness Based on Education (Male)"]}</SimpleData>\n'
                                        f'<SimpleData name="Product Awareness Based on Education (Female)">{values["Product Awareness Based on Education (Female)"]}</SimpleData>\n'
                                        f'<SimpleData name="Blinkit Availability">{values["Blinkit Availability"]}</SimpleData>\n'
                                        f'<SimpleData name="Vishal Mega Mart Availability">{values["Vishal Mega Mart Availability"]}</SimpleData>\n'
                                        f'<SimpleData name="Apollo Availability">{values["Apollo Availability"]}</SimpleData>\n'
                                        f'<SimpleData name="General Popularity on Online Storefronts">{values["General Popularity on Online Storefronts"]}</SimpleData>\n'
                                        f'<SimpleData name="Sales">{values["Sales"]}</SimpleData>\n'
                                        f'<SimpleData name="Serviceability of Pincode (Discrete, Yes/No)">{values["Serviceability of Pincode (Discrete, Yes/No)"]}</SimpleData>\n'
                                        f'<SimpleData name="Online Sales">{values["Online Sales"]}</SimpleData>\n'
                                        f'<SimpleData name="Market Penetration">{values["Market Penetration"]}</SimpleData>\n'
                                        f'<SimpleData name="Expansion Score">{values["Expansion Score"]}</SimpleData>\n')

    # Write the updated KML content to a new file
    with open(output_kml_file, 'w') as file:
        file.write(kml_content)
