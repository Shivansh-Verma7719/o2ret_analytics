import pandas as pd
from helper.sheet import get_sheet
from helper.scraper import blinkit

url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
a=get_sheet(url_pincode)

# Initialize the DataFrame with headers
# Start with base headers, extend dynamically
header = ['PinCode', 'Count']
b = pd.DataFrame(columns=header)

arr=[]
index=0
j=2
while j<36:
    if (a.iloc[j][4]=='SUB-DISTRICT'):
        arr.append(a.iloc[j][6])
        pass
    j=j+1
    pass  # example pin codes
i=0
allPinCodes=[]
while i<36:
    if a.iloc[i][4]=='SUB-DISTRICT':
        j=0
        while j<int(a.iloc[i][6]):
            allPinCodes.append(int(a.iloc[i][6+j+1]))
            j+=1
    i+=1
keyword=input("Enter The Keyword: ")

# Loop through all pin codes and scrape data
for pincode in allPinCodes:
    try:
        product_details, count_ratio = blinkit(keyword, str(pincode))
        
        # Create a dynamic header if necessary
        dynamic_header = header + [f"Product_{i+1}" for i in range(len(product_details))]
        
        # Prepare the data for the DataFrame
        ans = [pincode, count_ratio] + product_details
        
        # Create a DataFrame row with the dynamic header
        ser = pd.Series(ans, index=dynamic_header)
        
        # Concatenate the new row to the DataFrame
        b = pd.concat([b, ser.to_frame().T], ignore_index=True)
    except Exception as e:
        print(f"Error for PinCode {pincode}: {e}")
        continue