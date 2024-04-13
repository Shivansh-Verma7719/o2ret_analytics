import requests
import math
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

def get_popularity_region(prod):

    load_dotenv()
    params = {
    "engine": "google_trends",
    "q": prod,
    "data_type": "GEO_MAP_0",
    "geo": "IN-DL",
    "date": "today 1-m",
    "api_key": os.getenv("API_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    data = results["interest_by_region"]
    total_value = 0
    count = 0
    for entry in data:
        if entry['value'] == '<1':
            total_value += 1
        else:
            value = int(entry['value'])
            total_value += value
        count += 1
    average_value = total_value / count
    return average_value/100
    

def get_popularity(prod ,data):
    """
    Calculates the popularity score of a product.

    Args:
        prod: The product identifier.
        data: A dictionary containing sales and return information for the product.
            data['sales']: Total sales of the product in a given time period.
            data['returns']: Total returns of the product in the same time period.

    Returns:
        A float representing the product's popularity score (0 to 1).
    """
    gen_pop = get_popularity_region(prod)

    # Weights (adjust these based on your needs)
    if gen_pop < 0.3:
        return_penalty = 1
    else:
        return_penalty = 1 + gen_pop

    sales = data.get('sales')
    returns = data.get('returns')

    popularity = (sales / (sales + (returns * return_penalty))) * gen_pop

    return popularity

prod = 'fomo brews'
data = {'sales': 500, 'returns': 100}
popularity = get_popularity(prod, data)
print(popularity)

