import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

cid = ''
secret = ''
user = 'andrew'
redirect_uri = 'http://localhost:8080/'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
df = pd.read_csv('listeningHistory.csv')

features = ['duration_ms','key','mode', 'time_signature', 'acousticness',
 'danceability', 'energy', 'instrumentalness', 'liveness', 
 'loudness', 'speechiness', 'valence', 'tempo']

for feature in features:
	df[feature]=np.nan

for index, row in df.iterrows():
	if pd.notnull(df.at[index, 'trackID']):
		ids = []
		ids.append(df.at[index, 'trackID'])
		afeats = sp.audio_features(ids)
		for feature in features:
			df.at[index, feature] = afeats[0][feature]

df.to_csv('features.csv')