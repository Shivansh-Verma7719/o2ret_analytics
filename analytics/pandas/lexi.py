import pandas as pd
from collections import Counter
import re

# Load the Excel file
file_path = 'lexi-res.xlsx'  # Replace with your file path
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert 'flavor' column to strings to handle any non-string entries
df['flavor'] = df['cuisine'].astype(str)

# Tokenize and clean the flavor descriptions
def tokenize_and_clean(flavor):
    flavor = flavor.lower()
    flavor = re.sub(r'[^a-z\s]', '', flavor)
    tokens = flavor.split()
    return tokens

# Combine all flavor descriptions into a single list of tokens
all_tokens = []
for flavor in df['flavor']:
    tokens = tokenize_and_clean(flavor)
    all_tokens.extend(tokens)

# Count the frequency of each token
token_counts = Counter(all_tokens)

# Display the most common tokens
most_common_tokens = token_counts.most_common(30)
print("Most common flavor keywords:")
for token, count in most_common_tokens:
    print(f"{token}: {count}")

# Save the results to a CSV file
result_df = pd.DataFrame(most_common_tokens, columns=['Keyword', 'Frequency'])
result_df.to_csv('restaurants_cuisine_frequency.csv', index=False)
