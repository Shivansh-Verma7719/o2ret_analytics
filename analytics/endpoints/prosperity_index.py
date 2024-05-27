import pandas as pd
from helper.sheet import get_sheet

def searchSubDistrict(name,a):
    i=0
    while i<36:
        if str(a.iloc[i][5]).strip()==str(name).strip():
            return i
            pass
        i=i+1
        pass
    return -1

def allPincodes(name,a):
    arr=[]
    row=searchSubDistrict(name,a)
    if(row==-1):
        return
    numberOfPincodes=a.iloc[row][6]
    i=1
    while i<(numberOfPincodes+1):
        arr.append(int(a.iloc[row][6+i]))
        i=i+1
    return numberOfPincodes,arr  
def prosperityIndex():
    url_pincode = 'https://docs.google.com/spreadsheets/d/1gb1Vx1rnzocZRq4q4sq4NUyaM_go6tBAaAbCMVEptcE'
    url_prosperity = 'https://docs.google.com/spreadsheets/d/13rebDqDJG0eqxq8bnBP08WZ0iX2Yg9XGngwbymw8zr8'
    a = get_sheet(url_pincode)
    c = get_sheet(url_prosperity)
    headers=["PinCodes","Name","Total- Adjusted average household size","Total- (0.6×Percentage of Total Good)+(0.1×Percentage of Households with Internet)+(0.1×Percentage of Households with Car/Jeep/Van)+(0.1×Percentage of Permanent Structures)+(0.1×Percentage of Households availing Banking Services)","Total- Married Couples per household","Rural- Adjusted average household size","Rural- (0.6×Percentage of Total Good)+(0.1×Percentage of Households with Internet)+(0.1×Percentage of Households with Car/Jeep/Van)+(0.1×Percentage of Permanent Structures)+(0.1×Percentage of Households availing Banking Services)","Rural- Married Couples per household","Urban- Adjusted average household size","Urban- (0.6×Percentage of Total Good)+(0.1×Percentage of Households with Internet)+(0.1×Percentage of Households with Car/Jeep/Van)+(0.1×Percentage of Permanent Structures)+(0.1×Percentage of Households availing Banking Services)","Urban- Married Couples per household"]
    result=pd.DataFrame(columns=headers)
    i=6
    while(i<93):
        if(c.iloc[i][3]!='00000'):
        
            try:
                n, arr = allPincodes(c.iloc[i][5], a)  # Properly unpack the returned values
            except Exception as e:
                print(f"Error unpacking result for sub-district: {c.iloc[i][5]}")
                i += 1
                continue
            j=0
            while(j<n):
                ans=[]
                #PinCode
                ans.append(str(arr[j]))
        
                #Name
                ans.append(str(c.iloc[i][5]))
            
                #Total1
                ans.append(str(c.iloc[i][88]))
            
                #Total2
                ans.append(str(c.iloc[i][89]))
            
                #Total3
                ans.append(str(c.iloc[i][93]))
            
                if (c.iloc[i+1][6]=='Total'):
                    #Rural1
                    ans.append(str(0))
            
                    #Rural2
                    ans.append(str(0))
                
                    #Rural3
                    ans.append(str(0))
                
                    #Urban1
                    ans.append(str(0))
            
                    #Urban2
                    ans.append(str(0))
            
                    #Urban3
                    ans.append(str(0))
                    if(j==n-1):
                        i+=1
                    j+=1
                    ser=pd.Series(ans,index=headers)
                    result=pd.concat([result,ser.to_frame().T],ignore_index=True)
                elif(c.iloc[i+1][6]=='Urban'):
                    #Rural1
                    ans.append(str(0))
                
                    #Rural2
                    ans.append(str(0))
                
                    #Rural3
                    ans.append(str(0))
                
                    #Urban1
                    ans.append(str(c.iloc[i+1][88]))
        
                    #Urban2
                    ans.append(str(c.iloc[i+1][89]))
            
                    #Urban3
                    ans.append(str(c.iloc[i+1][93]))
                
                    if(j==n-1):
                        i+=2
                    j+=1
                    ser=pd.Series(ans,index=headers)
                    result=pd.concat([result,ser.to_frame().T],ignore_index=True)
                else:
                    #Rural1
                    ans.append(str(c.iloc[i+1][88]))
                
                    #Rural2
                    ans.append(str(c.iloc[i+1][89]))
                
                    #Rural3
                    ans.append(str(c.iloc[i+1][93]))
                
                    if(c.iloc[i+2][6]=='Total'):
                        if(j!=n-1):
                            i+=2
                        j+=1
                        ser=pd.Series(ans,index=headers)
                        result=pd.concat([result,ser.to_frame().T],ignore_index=True)
                    else:    
                        #Urban1
                        ans.append(str(c.iloc[i+2][88]))
        
                        #Urban2
                        ans.append(str(c.iloc[i+2][89]))
            
                        #Urban3
                        ans.append(str(c.iloc[i+2][93]))
                
                        if(j==n-1):
                            i+=3
                        j+=1
                        ser=pd.Series(ans,index=headers)
                        result=pd.concat([result,ser.to_frame().T],ignore_index=True)
        else:
                i+=1
    return result