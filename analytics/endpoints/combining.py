from prosperity_index import *
from market_size import *
from education_data import *

#res1 is population Data and res2 is from prosperity Index
res1 = population_Data(1,1)
res2 = prosperityIndex()
res3 = education_data(1, 1, 1)

def combine(res1,res2):
    result_final=pd.merge(res1,res2,on=["PinCodes"])
    filename="Combined.xlsx"
    result_final.to_excel(filename)

def combine_df(res1,res2):
    result_final=pd.merge(res1,res2,on=["PinCodes","Name"])
    return result_final

c1 = combine_df(res1,res2)
c2 = combine(c1,res3)