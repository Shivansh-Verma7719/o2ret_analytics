import pandas as pd
import xlsxwriter as xs
from helper.sheet import get_sheet

#URLs of the Google Sheets
url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
url_population = 'https://docs.google.com/spreadsheets/d/1AMdrzEqqlmn_9i0bEp9zTYtm9sz-OlTtP2d-N5TSeAg'

#Get the data from the Google Sheets
a = get_sheet(url_pincode)
b = get_sheet(url_population)

#Saving all the number of pincodes for each Sub-District in an array
arr=[]
index=0
j=2
while j<36:
    if (a.iloc[j][4]=='SUB-DISTRICT'):
        arr.append(a.iloc[j][6])
        pass
    j=j+1
    pass

#Name of File
workbook=xs.Workbook("ExcelFile-Final1.xlsx")

#Name The Sheet
worksheet = workbook.add_worksheet("secondSheet")

#Input The Weights
w1=int(input("Enter Weight 1: "))
w2=int(input("Enter Weight 2: "))

#Name The Headings
worksheet.write(0,0,"Sub-District Code")
worksheet.write(0,1,"Name")
worksheet.write(0,2,"Number of Pincodes")
worksheet.write(0,3,"Relevant Market Size")
worksheet.write(0,4,"Relevant Market Male Percentage")
worksheet.write(0,5,"Relevant Market Women Percentage")
worksheet.write(0,6,"Area")
worksheet.write(0,7,"Population Density")

index=0
i=9
while (i<114 and i+1<114 and i+2<114 and i+3<114):
    if(b.iloc[i][4]=='SUB-DISTRICT'):
        
        #FullCode
        worksheet.write(i-9+1,0,str(b.iloc[i][3]))
                                                                                                                           
        #Sub-District Name
        worksheet.write(i-9+1,1,str(b.iloc[i][5])) 
        
        #Number of Pincodes
        n=arr[index]
        index=index+1
        worksheet.write(i-9+1,2,str(n))
        
        #Relevant Market Size
        market_size=(w1*(b.iloc[i+1][11])+w2*(b.iloc[i+2][11]))/n
        market_size=round(market_size,2)
        worksheet.write(i-9+1,3,str(market_size))
                                                    
        #Men Relevant Size
        men_ms=(w1*b.iloc[i+1][12] + w2*b.iloc[i+2][12])/n
        men_ms=round(men_ms,2)
        worksheet.write(i-9+1,4,str(men_ms))
        
        #Women Relevant Size
        women_ms=(w1*b.iloc[i+1][13] + w2*b.iloc[i+2][13])/n
        women_ms=round(women_ms,2)
        worksheet.write(i-9+1,5,str(women_ms))
        
        #Area
        area=b.iloc[i][14]/n
        area=round(area,2)
        worksheet.write(i-9+1,6,str(area))
        
        #Population Density
        if area!=0:
            population_density=market_size/area
            population_density=round(population_density,2)
        else:
            population_density=0
        worksheet.write(i-9+1,7,str(population_density))    
        i=i+4
        pass
    else:
        i=i+1

workbook.close()     


