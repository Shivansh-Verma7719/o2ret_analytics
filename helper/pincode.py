import requests
import os
from dotenv import load_dotenv

def get_pincode(address):
    url = 'https://atlas.mappls.com/api/places/geocode'

    res = get_oauth2_token()
    access_token = res['access_token']
    token_type = res['token_type']

    headers = {
                'Authorization': f'{token_type} {access_token}'
            }
    params = {
                'address': address
            }

    response = requests.get(url, headers=headers, params=params).json()
    res={
        'pincode': response['copResults']['pincode'],
        'district': response['copResults']['district']
    }

    return res

def get_oauth2_token():
    url = 'https://outpost.mappls.com/api/security/oauth/token'
    # Load environment variables from .env file
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # Body of the POST request
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        # Sending the POST request
        response = requests.post(url, data=data)

        # Checking the response status code
        if response.status_code == 200:
            return response.json()
        else:
            return None
            print("Request failed with status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# print(get_pincode('West Delhi'))