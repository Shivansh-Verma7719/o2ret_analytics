import matplotlib.pyplot as plt
import textwrap
from matplotlib.ticker import MaxNLocator

# Configuration Section
CONFIG = {
    "label_wrap_width": 15,  # Width for wrapping labels
    "figure_size": (22, 12),  # Size of the figure (WIDTH, HEIGHT)
    "xlabel": "Products",  # Label for the x-axis
    "ylabel": "Price (Rs.)",  # Label for the y-axis
    "title": "Prices of Reliance Digital",  # TITLE of the graph
    "xlabel_fontsize": 14,  # Font size for the x-axis label
    "ylabel_fontsize": 14,  # Font size for the y-axis label
    "title_fontsize": 16,  # Font size for the title
    "xtick_fontsize": 12.5,  # Font size for the x-ticks (PRODUCTS)
    "ytick_fontsize": 14,  # Font size for the y-ticks (PRICE)
    "tight_layout_pad": 3.0,  # Padding for tight layout
    "tight_layout_w_pad": 2.0,  # Width padding for tight layout
    "tight_layout_h_pad": 2.0,  # Height padding for tight layout
    "nbins": 10,  # Number of bins for x-ticks
    "dpi": 300,  # DPI for saving the figure
    "output_file": "./product_graph.png"  # Output file path for saving the plot
}

# Function to wrap text
def wrap_labels(labels, width):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

# Product data
products_data = [
    ("Reconnect RALCE1002 USB-C to Lightning Cable", 899),
    ("Reconnect DNC UL-F 1 m USB to Lightning Cable", 899),
    ("Reconnect DNC UL-D 2-in-1 USB to Micro-USB & Lightning Cable", 799),
    ("Reconnect DNC UL-D 1 m 2-in-1 USB to Micro-USB & Lightning Cable", 799),
    ("Reconnect DNC UL-B 1 m PVC & Nylon Mesh Coated USB to Lightning Cable", 999),
    ("Reconnect Marvel Thanos Lighting cable, Apple compliant MFI certified cable", 529),
    ("Anker A8612H21 USB Type-C to Lightning MFi certified Cable", 1499),
    ("boAt LTG 500 Indestructible Lightning Cable 1 Mtr", 999),
    ("boAt LTG 650 Type C Lightning Cable 1.5 Mtr", 1049),
    ("Belkin F8J207BT04-GLD MFi Certified Kevlar USB to Lightning Cable", 1794),
    ("Belkin F8J023BT04-BLK 1.2 m MFI-Certified USB 2.0 to Lightning Cable", 1144),
    ("Apple 1m USB-C to Lightning Cable", 1900)
]

# Separate products and prices
products = [item[0] for item in products_data]
prices = [item[1] for item in products_data]

# Wrap the product names to the specified width from the config
wrapped_products = wrap_labels(products, CONFIG["label_wrap_width"])

# Create the line plot
plt.figure(figsize=CONFIG["figure_size"])
plt.plot(wrapped_products, prices, marker='o', linestyle='-', color='b')

# Add labels, title, and grid
plt.xlabel(CONFIG["xlabel"], fontsize=CONFIG["xlabel_fontsize"])
plt.ylabel(CONFIG["ylabel"], fontsize=CONFIG["ylabel_fontsize"])
plt.title(CONFIG["title"], fontsize=CONFIG["title_fontsize"])
plt.grid(True)

# Use MaxNLocator to limit the number of x-ticks
ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(nbins=CONFIG["nbins"], prune='both'))

# Set xticks with wrapped labels
plt.xticks(ticks=range(len(wrapped_products)), labels=wrapped_products, fontsize=CONFIG["xtick_fontsize"])

# Set y-tick font size
plt.yticks(fontsize=CONFIG["ytick_fontsize"])

# Adjust the layout to accommodate wrapped labels
plt.tight_layout(pad=CONFIG["tight_layout_pad"], w_pad=CONFIG["tight_layout_w_pad"], h_pad=CONFIG["tight_layout_h_pad"])

# Save the plot figure
plt.savefig(CONFIG["output_file"], dpi=CONFIG["dpi"])

# Show the plot
plt.show()
