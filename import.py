import pymongo
from pymongo import MongoClient
import pandas as pd
from glob import glob
import json
"""
class MongoDB(object):

    def __init__(self, dBName=None, collectionName=None):

        self.dBName = dBName
        self.collectionName = collectionName
        uri = "mongodb://<andrew>:<poko44>@<cluster0.dt9it.mongodb.net>:27017"
        self.client = MongoClient(uri)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]



    def InsertData(self, df):
     
        data = df.to_dict('records')

        self.collection.insert_many(data, ordered=False)
        print("All the Data has been Exported to Mongo DB Server .... ")
  """
if __name__ == "__main__":
	files = sorted(glob('data/*.csv'))
	df = pd.concat((pd.read_csv(file).assign(filename = file) for file in files), ignore_index = True)
	df.to_csv('raw_data.csv', index=False)