import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import LabelBinarizer
train = pd.read_csv("train.csv")
jobs_encoder = LabelBinarizer()
jobs_encoder.fit(train['Conditions'])
transformed = jobs_encoder.transform(train['Conditions'])
ohe_df = pd.DataFrame(transformed)
train = pd.concat([train, ohe_df], axis=1).drop(['Conditions'], axis=1)
train.drop(['artistName','trackName','Name','Snow','Heat Index','Unnamed: 0.1'],axis=1,inplace = True)
train[['Wind Gust']] = train[['Wind Gust']].fillna(10.00)
train[['Wind Chill']] = train[['Wind Chill']].fillna(10.00)
train[['Snow Depth']] = train[['Snow Depth']].fillna(0.0)
dates = train['Date time'].unique()
fdf = pd.DataFrame()
label = pd.DataFrame()
x_val = pd.DataFrame()
for date in dates:
    query = train[date == train['Date time']]
    external = query[['Cloud Cover', 0,1,2,3,4,
       'Maximum Temperature', 'Minimum Temperature','Precipitation',
       'Relative Humidity','Snow Depth', 'Temperature', 'Visibility', 'Wind Gust','Wind Chill', 'Wind Speed']].iloc[0]
    song_mean = query[['danceability', 'duration_ms', 'energy',
       'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'msPlayed',
       'speechiness', 'tempo', 'time_signature', 'valence']].mean()
    x_val = x_val.append(external,ignore_index=True)
    label = label.append(song_mean,ignore_index=True)
    fdf = fdf.append(pd.concat([song_mean,external]),ignore_index=True)
x_val.to_csv("input.csv",index=False)
label.to_csv("label.csv",index=False)
fdf.to_csv("test.csv",index=False)