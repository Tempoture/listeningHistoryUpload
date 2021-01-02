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
df = pd.read_csv('raw_data.csv')

df['trackID'] = ''
print(df)
for index, row in df.iterrows():
	track_id = sp.search(q='artist: '+row['artistName']+' 	track: '+row['trackName'],type='track',limit=1)
	if track_id['tracks']['total'] > 0:
		df.at[index, 'trackID'] = track_id['tracks']['items'][0]['id']

df.to_csv('listeningHistory.csv')
