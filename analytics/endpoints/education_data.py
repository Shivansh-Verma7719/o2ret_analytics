import pandas as pd
from helper.sheet import get_sheet

def searchSubDistrict(name, a):
    i=0
    while i<36:
        if str(a.iloc[i][5]).strip()==str(name).strip():
            return i
            pass
        i=i+1
        pass
    return -1

def allPincodes(name, a):
    arr=[]
    row=searchSubDistrict(name, a)
    if(row==-1):
        return
    numberOfPincodes=a.iloc[row][6]
    i=1
    while i<(numberOfPincodes+1):
        arr.append(int(a.iloc[row][6+i]))
        i=i+1
    return numberOfPincodes,arr
def education_data(w1, w2, w3):
    headers = [
        "PinCodes", "Total Literacy", "Total 12 Pass", "Total Graduate",
        "Male Literacy", "Male - 12 Pass", "Male - 12 Graduate", "Female Literacy", 
        "Female 12 Pass", "Female Graduate", "Literacy Index", "12 Pass Index", 
        "Graduate Index", "PinCode Awareness"
    ]
    url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
    url_education = 'https://docs.google.com/spreadsheets/d/1mK1ZfanLodzNXSbLoZACyftnzdHiOsEcEB9GJ6DRnuY'
    a = get_sheet(url_pincode)
    d = get_sheet(url_education)
    
    result_data = []
    i = 4
    while i < 13:
        try:
            n, arr = allPincodes(d.iloc[i, 4], a)  # Properly unpack the returned values
        except Exception as e:
            print(f"Error unpacking result for sub-district: {d.iloc[i][4]}")
            i += 1
            continue
        
        total_population = int(d.iloc[i, 17])
        total_male_population = int(d.iloc[i, 18])
        total_female_population = int(d.iloc[i, 19])
        
        for j in range(n):
            ans = [
                str(arr[j]),  # PinCodes
                str(d.iloc[i, 23]),  # Total Literacy
                str(d.iloc[i, 38]),  # Total 12 Pass
                str(d.iloc[i, 47]),  # Total Graduate
                str(d.iloc[i, 24]),  # Male Literacy
                str(d.iloc[i, 39]),  # Male - 12 Pass
                str(d.iloc[i, 48]),  # Male - 12 Graduate
                str(d.iloc[i, 25]),  # Female Literacy
                str(d.iloc[i, 40]),  # Female 12 Pass
                str(d.iloc[i, 49]),  # Female Graduate
                str((int(d.iloc[i, 23]) * w1 / total_population)*100),  # Literacy Index
                str((int(d.iloc[i, 24]) * w2 / total_male_population)*100),  # 12 Pass Index
                str((int(d.iloc[i, 25]) * w3 / total_female_population)*100),  # Graduate Index
            ]
            
            # PinCode Awareness
            pinaware_total = int(d.iloc[i, 23]) * w1 / total_population
            pinaware_male = int(d.iloc[i, 24]) * w2 / total_male_population
            pinaware_female = int(d.iloc[i, 25]) * w3 / total_female_population
            pinaware = ((pinaware_total + pinaware_male + pinaware_female) / 3)*100
            ans.append(str(pinaware))
            
            result_data.append(ans)
        
        i += 1
    
    result = pd.DataFrame(result_data, columns=headers)
    return result

# Example usage
if __name__ == "__main__":
    w1 = 0.5
    w2 = 0.3
    w3 = 0.2
    result = education_data(w1, w2, w3)
    print(result)
