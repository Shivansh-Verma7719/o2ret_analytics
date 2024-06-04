import csv
from color import create_kml_styles

def convert_to_kml_heatmap():
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
    
    # Create KML styles
    style_string = create_kml_styles()
    kml_content = kml_content.replace('<Folder>', style_string + '\n' + '<Folder>')

    color_count = 0
    # Replace placeholders with actual values
    for pincode, values in data.items():
        kml_content = kml_content.replace('<styleUrl>#falseColor</styleUrl>',
                                        f'<styleUrl>#color{color_count+1}</styleUrl>')
        kml_content = kml_content.replace(f'<SimpleData name="PINCODE">{pincode}</SimpleData>',
                                        f'<SimpleData name="Pincode">{pincode}</SimpleData>\n'
                                        f'<SimpleData name="name">{pincode}</SimpleData>\n'
                                        f'<SimpleData name="State">Delhi</SimpleData>\n'
                                        f'<SimpleData name="Sales">{values["Sales"]}</SimpleData>\n'
        )

    # Write the updated KML content to a new file
    with open(output_kml_file, 'w') as file:
        file.write(kml_content)

if __name__ == '__main__':
    convert_to_kml_heatmap()