import pandas as pd
import numpy as np

df = pd.read_csv('history_data.csv')

for index, row in df.iterrows():
	if df.at[index, 'Precipitation'] > 0:
		df.at[index, 'Conditions'] = 'Rain'
		if df.at[index, 'Temperature'] < 32.0:
			df.at[index, 'Conditions'] = 'Snow'

df.to_csv('troyweather.csv')