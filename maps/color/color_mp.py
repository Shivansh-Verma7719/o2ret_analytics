import pandas as pd

# Define the function to generate hex colors
def sales_to_hex_color(market_penetration, min_penetration, max_penetration):
    # Ensure market_penetration is within the provided range
    market_penetration = max(min(market_penetration, max_penetration), min_penetration)

    # Normalize the market_penetration value to a 0-1 range
    normalized_penetration = (market_penetration - min_penetration) / (max_penetration - min_penetration)

    # Calculate the red and green components
    red = int((1 - normalized_penetration) * 255)
    green = int(normalized_penetration * 255)

    # Convert the red and green components to a hex string
    hex_color = f"#{red:02x}{green:02x}00"

    return hex_color

# Load the data from the CSV file
file_path = 'geo.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Find the minimum and maximum market penetration values
min_penetration = data['Market Penetration'].min()
max_penetration = data['Market Penetration'].max()
print(min_penetration)
print(max_penetration)

# Generate hex colors for each pincode based on market penetration value
data['Color'] = data['Market Penetration'].apply(lambda x: sales_to_hex_color(x, min_penetration, max_penetration))

# Save the pincode, market penetration, and color mapping to a new Excel file
output_file_path = 'pincode_market_penetration_color_mapping.xlsx'
data.to_excel(output_file_path, index=False)
print(f"Output file saved as {output_file_path}")
