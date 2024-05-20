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

def prosperity_index():
    #URLs of the Google Sheets
    url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
    url_prosperity = 'https://docs.google.com/spreadsheets/d/13rebDqDJG0eqxq8bnBP08WZ0iX2Yg9XGngwbymw8zr8'
    a = get_sheet(url_pincode)
    b = get_sheet(url_prosperity)

    #Naming The Output File
    workbook=xs.Workbook("Excel-Prosperity_Index_1.xlsx")
    #Naming The Excel Sheet
    worksheet=workbook.add_worksheet("First_Sheet")

    #Writing The Headings
    worksheet.write(0,0,"Pincodes")
    worksheet.write(0,1,"Sub_District_Name")
    worksheet.write(0,2,"Total- Adjusted average household size")
    worksheet.write(0,3,"Total- Prosperity Score")
    worksheet.write(0,4,"Total- Married Couples per household")
    worksheet.write(0,5,"Rural- Adjusted average household size")
    worksheet.write(0,6,"Rural- Prosperity Score")
    worksheet.write(0,7,"Rural- Married Couples per household")
    worksheet.write(0,8,"Urban- Adjusted average household size")
    worksheet.write(0,9,"Urban- Prosperity Score")
    worksheet.write(0,10,"Urban- Married Couples per household")
    rowToWrite=1

    #Loop To Iterate over the Data
    i=6
    while(i<93):
        if(b.iloc[i][3]!='00000'):
            
            try:
                n, arr = allPincodes(b.iloc[i][5], a)  # Properly unpack the returned values
            except Exception as e:
                print(f"Error unpacking result for sub-district: {b.iloc[i][5]}")
                i += 1
                continue
            
            #This Loop is to iterate over the number of Pincodes
            j=0
            while(j<n):
                #PinCode
                worksheet.write(rowToWrite,0,str(arr[j]))
            
                #Name
                worksheet.write(rowToWrite,1,str(b.iloc[i][5]))
            
                #Total1
                worksheet.write(rowToWrite,2,str(b.iloc[i][88]))
            
                #Total2
                worksheet.write(rowToWrite,3,str(b.iloc[i][89]))
            
                #Total3
                worksheet.write(rowToWrite,4,str(b.iloc[i][93]))
            
                if (b.iloc[i+1][6]=='Total'):
                    #Rural1
                    worksheet.write(rowToWrite,5,str(0))
                
                    #Rural2
                    worksheet.write(rowToWrite,6,str(0))
                
                    #Rural3
                    worksheet.write(rowToWrite,7,str(0))
                
                    #Urban1
                    worksheet.write(rowToWrite,8,str(0))
                
                    #Urban2
                    worksheet.write(rowToWrite,9,str(0))
                
                    #Urban3
                    worksheet.write(rowToWrite,10,str(0))
                    rowToWrite+=1
                    if(j==n-1):
                        i+=1
                    j+=1    
                elif(b.iloc[i+1][6]=='Urban'):
                    #Rural1
                    worksheet.write(rowToWrite,5,str(0))
                
                    #Rural2
                    worksheet.write(rowToWrite,6,str(0))
                
                    #Rural3
                    worksheet.write(rowToWrite,7,str(0))
                
                    #Urban1
                    worksheet.write(rowToWrite,8,str(b.iloc[i+1][88]))
            
                    #Urban2
                    worksheet.write(rowToWrite,9,str(b.iloc[i+1][89]))
            
                    #Urban3
                    worksheet.write(rowToWrite,10,str(b.iloc[i+1][93]))
                
                    rowToWrite+=1
                    if(j==n-1):
                        i+=2
                    j+=1
                else:
                    #Rural1
                    worksheet.write(rowToWrite,5,str(b.iloc[i+1][88]))
                
                    #Rural2
                    worksheet.write(rowToWrite,6,str(b.iloc[i+1][89]))
                
                    #Rural3
                    worksheet.write(rowToWrite,7,str(b.iloc[i+1][93]))
                
                    if(b.iloc[i+2][6]=='Total'):
                        rowToWrite+=1
                        if(j!=n-1):
                            i+=2
                        j+=1
                    else:    
                        #Urban1
                        worksheet.write(rowToWrite,8,str(b.iloc[i+2][88]))
            
                        #Urban2
                        worksheet.write(rowToWrite,9,str(b.iloc[i+2][89]))
            
                        #Urban3
                        worksheet.write(rowToWrite,10,str(b.iloc[i+2][93]))
                
                        rowToWrite+=1
                        if(j==n-1):
                            i+=3
                        j+=1
        else:
                i+=1

    #Saving and Closing the File            
    workbook.close()

if __name__ == "__main__":
    prosperity_index()
