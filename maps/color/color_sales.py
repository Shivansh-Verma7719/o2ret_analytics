import pandas as pd

# Define the function to generate hex colors
def sales_to_hex_color(sales, min_sales, max_sales):
    # Ensure sales is within the provided range
    sales = max(min(sales, max_sales), min_sales)

    # Normalize the sales value to a 0-1 range
    normalized_sales = (sales - min_sales) / (max_sales - min_sales)

    # Calculate the red and green components
    red = int((1 - normalized_sales) * 255)
    green = int(normalized_sales * 255)

    # Convert the red and green components to a hex string
    hex_color = f"#{red:02x}{green:02x}00"

    return hex_color

# Load the sales data from the Excel file
file_path = 'Sales-Pincode.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Find the minimum and maximum sales values
min_sales = data['Sales'].min()
max_sales = data['Sales'].max()

# Generate hex colors for each pincode based on sales value
data['Color'] = data['Sales'].apply(lambda x: sales_to_hex_color(x, min_sales, max_sales))

# Save the pincode, sales, and color mapping to a new Excel file
output_file_path = 'pincode_sales_color_mapping.xlsx'
data.to_excel(output_file_path, index=False)

print(f"Output file saved as {output_file_path}")
