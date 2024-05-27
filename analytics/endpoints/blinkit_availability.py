import pandas as pd
from helper.scraper import blinkit

a,b = blinkit("dove", "110001")
print(a)
print(b)

# a=pd.read_excel("PIN Code Mapping.xlsx")
# #No. of pincodes in each sub-district
# arr=[]
# index=0
# j=2
# while j<36:
#     if (a.iloc[j][4]=='SUB-DISTRICT'):
#         arr.append(a.iloc[j][6])
#         pass
#     j=j+1
#     pass
# #Getting all PinCodes
# arr=[]
# index=0
# j=2
# while j<36:
#     if (a.iloc[j][4]=='SUB-DISTRICT'):
#         arr.append(a.iloc[j][6])
#         pass
#     j=j+1
#     pass

# #Take Input of keyword
# keyword=input("Enter The Keyword: ")

# #Getting back a 2D array from blinkit
# arr=blinkit(keyword)

# header=["PinCode","Blinkit Availability Score"]
# b=pd.DataFrame(columns=header)

# for i in range(len(arr)):
#     count=0
#     ans=[]
#     for j in range(len(arr[i])):
#         arr.append(arr[i][j])
#         if(keyword in arr[i][j]):
#             count+=1
#     ans.append(allPinCodes[i])
#     ans.append(str(count)+"/"+str(len(arr[i])))
#     for j in range(len(arr[i])):
#         ans.append(arr[i][j])
#     ser=pd.Series(ans,index=header)
#     b=pd.concat([b,ser.to_frame().T],ignore_index=True)

# b.to_excel("Result")