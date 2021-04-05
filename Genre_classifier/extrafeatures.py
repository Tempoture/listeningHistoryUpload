import pandas as pd
import requests
import json
from datetime import datetime


access_token = 'BQCAcS1cUR_X47LSCdaUSE1zPP86ZobHydag-eUUF_CM_5d8DvuHm4-qLd3NLr-jxuhibcsRyohX_B9tMC8nvnk1pfjM62bw3zMfXLniuB-69Yk0aDD6Y5fH2Fkuy3oN4jUTKWjyakCqtW-w2XGFY6UT5SIzUxx_w8q3cknOzWDVbL8_wWgn-cjkK0jj'

def chunks(lst, n): # We have to split our playlist requests in chunks of 50
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_songs_audio_features(song_ids):
    data =  pd.read_csv('SpotifyFeatures.csv')
    track_ids = data['track_id'].unique()
    song_id_req = list(chunks(list(song_ids),50)) # In case they have more than 50 songs which is likely we need to split requests up into batches of 50.
    feature_dict = dict()
    for req in song_id_req:
        id_str =  ",".join(req)
        req_endpoint = f'https://api.spotify.com/v1/tracks?ids={id_str}'
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        audio_j = ""
        try:
            resp =requests.get(req_endpoint, headers=auth_header)
            resp.raise_for_status()
            audio_j = resp.json()
            temp_d = {}
            for a in audio_j['tracks']:
                feature_dict[a['id']] ={
                    'explicit' : a['explicit'],
                    'release_date' : a['album']['release_date']
                }
        except requests.exceptions.HTTPError as err:
            print("ERR:" + str(err))
    return feature_dict

def validate_full(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_month(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m')
        return True
    except ValueError:
        return False

def write_to_file():
    f =  open("Features.json","w")
    f.write(json.dumps(get_songs_audio_features(track_ids),indent=4))
    f.close()

def add_features():
    with open('Features.json') as f:
        data = json.load(f)
        explicit_dict = dict()
        year_dict = dict()
        month_dict =  dict()
        day_dict =  dict()
        weekday_dict = dict()
        for song_id,feature in data.items():
            explicit_dict[song_id] = int(feature['explicit'])
            if validate_full(feature['release_date']):
                release_date =  datetime.strptime(feature['release_date'],"%Y-%m-%d")
                year_dict[song_id] = release_date.year
                month_dict[song_id] = release_date.month
                day_dict[song_id] = release_date.day
                weekday_dict[song_id] = release_date.strftime("%A")
            elif validate_month(feature['release_date']):
                release_date =  datetime.strptime(feature['release_date'],"%Y-%m")
                year_dict[song_id] = release_date.year
                month_dict[song_id] = release_date.month
                day_dict[song_id] = None
                weekday_dict[song_id] = None
            elif feature['release_date'] != '0000':
                release_date =  datetime.strptime(feature['release_date'],"%Y")
                year_dict[song_id] = release_date.year
                month_dict[song_id] = None
                day_dict[song_id] = None
                weekday_dict[song_id] = None
            else:
                year_dict[song_id] = None
                month_dict[song_id] = None
                day_dict[song_id] = None
                weekday_dict[song_id] = None
        Spdata =  pd.read_csv('SpotifyFeatures.csv')
        Spdata['is_explicit'] = Spdata['track_id'].map(explicit_dict)
        Spdata['release_year'] = Spdata['track_id'].map(year_dict)
        Spdata['release_month'] = Spdata['track_id'].map(month_dict)
        Spdata['release_day'] = Spdata['track_id'].map(day_dict)
        Spdata['release_weekday'] =  Spdata['track_id'].map(weekday_dict)
        Spdata.to_csv('ExtraFeatures.csv',index=False)  
add_features()