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
def population_Data(w1,w2):
    w1=w1
    w2=w2
    url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
    url_population = 'https://docs.google.com/spreadsheets/d/1AMdrzEqqlmn_9i0bEp9zTYtm9sz-OlTtP2d-N5TSeAg'

    #Get the data from the Google Sheets
    a = get_sheet(url_pincode)
    b = get_sheet(url_population)
    headers=["PinCodes","Name","Relevant Market Size","Relevant Market Male Percentage","Relevant Market Women Percentage","Area","Population Density"]
    result=pd.DataFrame(columns=headers)
    index=0
    i=9
    while (i<114 and i+1<=114 and i+2<=114 and i+3<=114):
        if(b.iloc[i][4]=='SUB-DISTRICT'):
            try:
                n, arr = allPincodes(b.iloc[i][5], a)  # Properly unpack the returned values
            except Exception as e:
                print(f"Error unpacking result for sub-district: {b.iloc[i][5]}")
                i += 1
                continue
            j=0
        
            while j<n:
                ans=[]
                #PinCode
                ans.append(str(arr[j]))
                                                                                                                           
                #Sub-District Name
                ans.append(b.iloc[i][5]) 
        
        
                #Relevant Market Size
                market_size=(w1*(b.iloc[i+1][11])+w2*(b.iloc[i+2][11]))/n
                market_size=round(market_size,2)
                ans.append(market_size)
                                                    
                #Men Relevant Size
                men_ms=(w1*b.iloc[i+1][12] + w2*b.iloc[i+2][12])/n
                men_ms=round(men_ms,2)
                ans.append(men_ms)
        
                #Women Relevant Size
                women_ms=(w1*b.iloc[i+1][13] + w2*b.iloc[i+2][13])/n
                women_ms=round(women_ms,2)
                ans.append(women_ms)
        
                #Area
                area=b.iloc[i][14]/n
                area=round(area,2)
                ans.append(area)
        
                #Population Density
                if area!=0:
                    population_density=market_size/area
                    population_density=round(population_density,2)
                else:
                    population_density=0
                ans.append(population_density)
                ser=pd.Series(ans,index=headers)
                result=pd.concat([result,ser.to_frame().T], ignore_index=True)
                j=j+1                   
            i=i+3
            pass
        else:
            i=i+1
    return result
