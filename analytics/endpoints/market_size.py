import pandas as pd
import xlsxwriter as xs
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

def get_market_size():
    #URLs of the Google Sheets
    url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
    url_population = 'https://docs.google.com/spreadsheets/d/1AMdrzEqqlmn_9i0bEp9zTYtm9sz-OlTtP2d-N5TSeAg'

    #Get the data from the Google Sheets
    a = get_sheet(url_pincode)
    b = get_sheet(url_population)

    #Name of File
    workbook=xs.Workbook("Excel_File.xlsx")

    #Input The Weights
    w1=int(input("Enter Weight 1: "))
    w2=int(input("Enter Weight 2: "))

    #Name The Sheet
    worksheet = workbook.add_worksheet("First_Sheet")

    #Name The Headings
    worksheet.write(0,0,"Pin-Code")
    worksheet.write(0,1,"Name")
    worksheet.write(0,2,"Relevant Market Size")
    worksheet.write(0,3,"Relevant Market Male Percentage")
    worksheet.write(0,4,"Relevant Market Women Percentage")
    worksheet.write(0,5,"Area")
    worksheet.write(0,6,"Population Density")

    index=0
    i=9
    rowToWrite=i-8
    while (i<114 and i+1<114 and i+2<114 and i+3<114):
        if(b.iloc[i][4]=='SUB-DISTRICT'):
            try:
                n, arr = allPincodes(b.iloc[i][5], a)  # Properly unpack the returned values
            except Exception as e:
                print(e)
                print(f"Error unpacking result for sub-district: {b.iloc[i][5]}")
                i += 1
                continue
            j=0
            
            while j<n:
                #PinCode
                worksheet.write(rowToWrite,0,arr[j])
                                                                                                                            
                #Sub-District Name
                worksheet.write(rowToWrite,1,str(b.iloc[i][5])) 
            
            
                #Relevant Market Size
                market_size=(w1*(b.iloc[i+1][11])+w2*(b.iloc[i+2][11]))/n
                market_size=round(market_size,2)
                worksheet.write(rowToWrite,2,str(market_size))
                                                        
                #Men Relevant Size
                men_ms=(w1*b.iloc[i+1][12] + w2*b.iloc[i+2][12])/n
                men_ms=round(men_ms,2)
                worksheet.write(rowToWrite,3,str(men_ms))
            
                #Women Relevant Size
                women_ms=(w1*b.iloc[i+1][13] + w2*b.iloc[i+2][13])/n
                women_ms=round(women_ms,2)
                worksheet.write(rowToWrite,4,str(women_ms))
            
                #Area
                area=b.iloc[i][14]/n
                area=round(area,2)
                worksheet.write(rowToWrite,5,str(area))
            
                #Population Density
                if area!=0:
                    population_density=market_size/area
                    population_density=round(population_density,2)
                else:
                    population_density=0
                worksheet.write(rowToWrite,6,str(population_density))
                j=j+1
                rowToWrite=rowToWrite+1                    
            i=i+4
            pass
        else:
            i=i+1
    workbook.close()
if __name__ == '__main__':
    get_market_size()

