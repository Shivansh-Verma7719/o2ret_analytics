from prosperity_index import *
from market_size import *
#res1 is population Data and res2 is from prosperity Index
res1=population_Data(1,1)
res2=prosperityIndex()

def combine(res1,res1):
    result_final=pd.merge(res1,res2,on=["PinCodes","Name"])
    filename="Combined5.xlsx"
    result_final.to_excel(filename)

def combine_df(res1,res2):
    result_final=pd.merge(res1,res2,on=["PinCodes","Name"])
    return result_final