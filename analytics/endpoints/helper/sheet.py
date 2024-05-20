import pandas as pd
import re

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=xlsx'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url

def get_sheet(url):
    new_url = convert_google_sheet_url(url)
    df = pd.read_excel(new_url)
    return df

if __name__ == "__main__":
    url = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
    df = get_sheet(url)
    print(df)
