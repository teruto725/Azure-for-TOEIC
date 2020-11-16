import pandas as pd
import numpy as np
data = pd.read_csv("words.csv",header=None)
data1 = data.loc[:,0:1].values
data2 = data.loc[:,2:3].values
arr =np.concatenate([data1,data2], 0)
df = pd.DataFrame(arr)
df.to_csv("toeic_words.csv",header=None,index=None)