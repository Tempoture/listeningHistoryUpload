import numpy as np
import pandas as pd

df = pd.read_csv('complete weather/troyweather.csv')
df2 = pd.read_csv('features.csv')
for index, row in df2.iterrows():
	df2.at[index, 'endTime'] = df2.at[index, 'endTime'].split()[0]
df2 = df2.rename(columns = {'endTime': 'Date time'})
print(pd.merge(df2,df, how='outer', on='Date time'))