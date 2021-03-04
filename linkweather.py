import numpy as np
import pandas as pd
import datetime
import os.path
from os import path

if not path.exists("train.csv"):
	df = pd.read_csv('troyweather.csv')
	df2 = pd.read_csv('features.csv')
	for index, row in df2.iterrows():
		df2.at[index, 'endTime'] = df2.at[index, 'endTime'].split()[0]
		df2.at[index, 'endTime'] = (datetime.datetime.strptime(df2.at[index, 'endTime'], '%m/%d/%Y')).strftime("%m/%d/%Y")

	df2.drop(['Unnamed: 0', 'Unnamed: 0.1'],axis=1,inplace = True)
	df2.dropna(inplace = True)
	fdf = pd.DataFrame()
	for index, row in df.iterrows():	
		query = df2[df2.endTime == row['Date time']]
		for indexq, rowq in query.iterrows():
			rowq.drop('endTime',inplace=True)
			rowq = rowq.append(row)
			fdf = fdf.append(rowq,ignore_index=True)
	fdf.drop(['Unnamed: 0', 'trackID'],axis=1,inplace = True)
	fdf.to_csv("train.csv",index=False)