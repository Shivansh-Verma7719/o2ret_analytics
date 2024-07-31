import pandas as pd
import re

# Read the Excel file
df = pd.read_excel('yoga-bar.xlsx')

# Helper function to parse product information
def parse_product_info(product_str):
    parts = product_str.split(', ')
    if len(parts) >= 3:
        name, time, price_info = parts[0], parts[1], parts[2]
        price_match = re.search(r'₹(\d+)', price_info)
        if price_match:
            price = float(price_match.group(1))
        else:
            price = 0.0  # Default to 0 if no price found
        discount_match = re.search(r'(\d+)% OFF', price_info)
        discount = float(discount_match.group(1)) if discount_match else 0.0
        return name, time, price, discount
    return None, None, 0, 0

# Initialize list to store output rows
output_rows = []

# Iterate through the dataframe two rows at a time
for i in range(0, len(df), 2):
    pincode = df.iloc[i, 0]
    
    # Branded search term row
    branded_row = df.iloc[i, 2:].dropna()
    branded_products = [parse_product_info(item) for item in branded_row if item and "N/A" not in item]

    # Generic search term row
    generic_row = df.iloc[i+1, 2:].dropna()
    generic_products = [parse_product_info(item) for item in generic_row if item and "N/A" not in item]

    if not branded_products or not generic_products or 'N/A' in df.iloc[i, 2] or 'N/A' in df.iloc[i+1, 2]:
        # If the row is empty or product1 has N/A, mark as not serviceable
        output_row = [
            pincode,
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable",
            "not serviceable"
        ]
    else:
        # Analysis for branded search term
        branded_products_sorted = sorted(branded_products, key=lambda x: x[3], reverse=True)  # Sort by discount
        most_discounted_branded = branded_products_sorted[:3]  # 3 most discounted products
        branded_aov = sum([p[2] for p in branded_products]) / len(branded_products) if branded_products else 0
        branded_pack_share = sum(['Pack' in p[0] for p in branded_products]) / len(branded_products) if branded_products else 0
        branded_bar_share = 1 - branded_pack_share
        
        # Analysis for generic search term
        generic_yoga_bar = [p for p in generic_products if 'Yoga Bar' in p[0]]
        generic_competitors = [p for p in generic_products if 'Yoga Bar' not in p[0]]
        generic_yoga_bar_aov = sum([p[2] for p in generic_yoga_bar]) / len(generic_yoga_bar) if generic_yoga_bar else 0
        generic_competitor_aov = sum([p[2] for p in generic_competitors]) / len(generic_competitors) if generic_competitors else 0
        generic_yoga_bar_share = len(generic_yoga_bar) / len(generic_products) if generic_products else 0
        generic_competitor_share = 1 - generic_yoga_bar_share

        # Combine results
        output_row = [
            pincode,
            most_discounted_branded[0][0] if len(most_discounted_branded) > 0 else '',
            most_discounted_branded[1][0] if len(most_discounted_branded) > 1 else '',
            most_discounted_branded[2][0] if len(most_discounted_branded) > 2 else '',
            branded_aov,
            branded_pack_share,
            branded_bar_share,
            generic_competitor_aov,
            generic_yoga_bar_aov,
            len(generic_competitors),
            len(generic_yoga_bar)
        ]
    
    output_rows.append(output_row)

# Create output dataframe
output_df = pd.DataFrame(output_rows, columns=[
    'pincode', 'most discounted product1', 'most discounted product2', 'most discounted product3',
    'branded search AOV', 'branded search share of pack', 'branded search share of bar',
    'generic search competitor AOV', 'generic search AOV of Yoga Bar',
    'generic search competitor share', 'generic search Yoga Bar share'
])

# Save to Excel
output_df.to_excel('blinkit_analysis_output.xlsx', index=False)
