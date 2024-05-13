import requests
import json
from dotenv import load_dotenv



def get_cell_value(spreadsheet_id, key, cells):
    uri = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{cells}?key={key}"
    response = requests.get(uri)
    data = response.json()
    return data['values'][0][0]

load_dotenv()
pincode_lookup_sid = "1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE"
education_sid = "1mK1ZfanLodzNXSbLoZACyftnzdHiOsEcEB9GJ6DRnuY"
population_sid = "1AMdrzEqqlmn_9i0bEp9zTYtm9sz-OlTtP2d-N5TSeAg"
prosperity_sid = "1JtNQkuw-ba9thvHpdj44n2AaLmelP-k3mgInSzjcJeE"

key = "AIzaSyBMiBffpXNl06sN4nvXy_9skYyPk_DZi7I"
cells = "G2"

print(data['values'][0][0])