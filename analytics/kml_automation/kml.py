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

    with open(template_kml_file, 'r') as file:
        kml_content = file.read()

    # Replace placeholders with actual values
    for pincode, values in data.items():
        kml_content = kml_content.replace(f'<SimpleData name="PINCODE">{pincode}</SimpleData>',
                                        f'<SimpleData name="Pincode">{pincode}</SimpleData>\n'
                                        f'<SimpleData name="name">{pincode}</SimpleData>\n'
                                        f'<SimpleData name="State">Delhi</SimpleData>\n'
                                        f'<SimpleData name="Relevant Market Size">{values["Relevant Market Size"]}</SimpleData>\n'
                                        f'<SimpleData name="Relevant Market Male Percentage">{values["Relevant Market Male Percentage"]}</SimpleData>\n'
                                        f'<SimpleData name="Relevant Market Women Percentage">{values["Relevant Market Women Percentage"]}</SimpleData>\n'
                                        f'<SimpleData name="Area">{values["Area"]}</SimpleData>\n'
                                        f'<SimpleData name="Population Density">{values["Population Density"]}</SimpleData>\n'
                                        f'<SimpleData name="Total- Adjusted average household size">{values["Total- Adjusted average household size"]}</SimpleData>\n'
                                        f'<SimpleData name="Total- Pincode Prosperity Score">{values["Total- Pincode Prosperity Score"]}</SimpleData>\n'
                                        f'<SimpleData name="Total- Married Couples per household">{values["Total- Married Couples per household"]}</SimpleData>\n'
                                        f'<SimpleData name="Rural- Adjusted average household size">{values["Rural- Adjusted average household size"]}</SimpleData>\n'
                                        f'<SimpleData name="Rural- Pincode Prosperity Score">{values["Rural- Pincode Prosperity Score"]}</SimpleData>\n'
                                        f'<SimpleData name="Rural- Married Couples per household">{values["Rural- Married Couples per household"]}</SimpleData>\n'
                                        f'<SimpleData name="Urban- Adjusted average household size">{values["Urban- Adjusted average household size"]}</SimpleData>\n'
                                        f'<SimpleData name="Urban- Pincode Prosperity Score">{values["Urban- Pincode Prosperity Score"]}</SimpleData>\n'
                                        f'<SimpleData name="Urban- Married Couples per household">{values["Urban- Married Couples per household"]}</SimpleData>\n'
                                        f'<SimpleData name="Total Literacy">{values["Total Literacy"]}</SimpleData>\n'
                                        f'<SimpleData name="Total 12 Pass">{values["Total 12 Pass"]}</SimpleData>\n'
                                        f'<SimpleData name="Total Graduate">{values["Total Graduate"]}</SimpleData>\n'
                                        f'<SimpleData name="Male Literacy">{values["Male Literacy"]}</SimpleData>\n'
                                        f'<SimpleData name="Male - 12 Pass">{values["Male - 12 Pass"]}</SimpleData>\n'
                                        f'<SimpleData name="Male - 12 Graduate">{values["Male - 12 Graduate"]}</SimpleData>\n'
                                        f'<SimpleData name="Female Literacy">{values["Female Literacy"]}</SimpleData>\n'
                                        f'<SimpleData name="Female 12 Pass">{values["Female 12 Pass"]}</SimpleData>\n'
                                        f'<SimpleData name="Female Graduate">{values["Female Graduate"]}</SimpleData>\n'
                                        f'<SimpleData name="Literacy Index">{values["Literacy Index"]}</SimpleData>\n'
                                        f'<SimpleData name="12 Pass Index">{values["12 Pass Index"]}</SimpleData>\n'
                                        f'<SimpleData name="Graduate Index">{values["Graduate Index"]}</SimpleData>\n'
                                        f'<SimpleData name="PinCode Awareness">{values["PinCode Awareness"]}</SimpleData>\n'
                                        f'<SimpleData name="Blinkit Availability">{values["Blinkit Availability"]}</SimpleData>\n'
                                        f'<SimpleData name="Vishal Mega Mart Availability">{values["Vishal Mega Mart Availability"]}</SimpleData>\n'
                                        f'<SimpleData name="Apollo Availability">{values["Apollo Availability"]}</SimpleData>\n'
                                        f'<SimpleData name="General Popularity on Online Storefronts">{values["General Popularity on Online Storefronts"]}</SimpleData>\n'
                                        f'<SimpleData name="Sales">{values["Sales "]}</SimpleData>\n'
                                        f'<SimpleData name="Serviceability of Pincode (Discrete, Yes/No)">{values["Serviceability of Pincode (Discrete, Yes/No)"]}</SimpleData>\n'
                                        f'<SimpleData name="Online Sales">{values["Online Sales"]}</SimpleData>\n'
                                        f'<SimpleData name="Market Penetration">{values["Market Penetration"]}</SimpleData>\n'
                                        f'<SimpleData name="Expansion Score">{values["Expansion Score"]}</SimpleData>\n')

    with open(output_kml_file, 'w') as file:
        file.write(kml_content)

if __name__ == '__main__':
    convert_to_kml()