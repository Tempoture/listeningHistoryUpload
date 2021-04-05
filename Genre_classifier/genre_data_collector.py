from bs4 import BeautifulSoup
import urllib.request as urllib
import requests
import json
import pandas as pd

genre_list = ['Folk', 'Pop', 'Soundtrack', 'Reggaeton', 'Opera', 'Ska', 'Anime',
       'Soul', 'Rap', 'Electronic', 'Reggae', 'Country', 'Blues',
       'Children’s Music', 'Dance', 'Hip-Hop', 'Comedy', 'Alternative',
       'World', 'Classical', 'Movie', 'Jazz', 'R&B', 'Rock', 'Indie']
access_token = 'BQBn2xFCBjRVcZv5TG88FONINANu48T6fKFYGcTfRMd8fTT4DbvclxxZAvfly6JQCQoab9ouSaSZvRoqFQJ14kI5FRh259726ngLnrHVnqkcOjqKs6VprjFKfMjcPPYPn_WVMzV6Jttz1gE5ZPF09A9BhCs7GCxOgJpoaPnN9M4VuVuL7VwYXOlHv18X'
song_id = set()

def fresh_soup(url): 
  # when making requests identify as if using the Mozilla Browser
  hdr = {'User-Agent': 'Mozilla/5.0'} 
  # make a url request using the specified browser
  req = urllib.Request(url,headers=hdr)   
  # retrieve the page source
  source = urllib.urlopen(req,timeout=10).read()
  soup = BeautifulSoup(source,'lxml')   
  return soup

def get_genres():
    # url for a list of every mainstream genre
    origin = 'https://everynoise.com/everynoise1d.cgi?scope=mainstream%20only&vector=popularity'
    # get the formatted page source
    soup = fresh_soup(origin) 
    # retrieve a list of all table tags and grab the second table
    table = soup.find_all('table')[0]
    genres = list()
    # loop through every row in the table
    for row in table.find_all('tr'): 
        for genre in row.find_all("a",title='Re-sort the list starting from here.'):
            genres.append((genre.text).lower())                                
    return genres

def get_genre_songs(genre):
    offset = 0
    global access_token
    global song_id
    nextReqLink =  f'https://api.spotify.com/v1/search?q=genre:{genre}&type=track&limit=50'
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    genre_id = {
        genre : list()
    }
    req_made = 1
    popularity_id = dict()
    try:
        while nextReqLink is not None and offset < 1000:    
            resp =requests.get(nextReqLink, headers=auth_header)
            resp.raise_for_status()
            for track in resp.json()['tracks']['items']:
                if track['id'] not in song_id: # Check for duplicates
                    song_id.add(track['id'])
                    popularity_id[track['id']] = track['popularity']
                    genre_id[genre].append(track['id'])
            offset+= 50
            nextReqLink = resp.json()['tracks']['next']
            req_made+=1
    except requests.exceptions.HTTPError as err:
        print("ERR:" + str(err))
    return (genre_id,popularity_id)

def get_all_genre_songs():
    global genre_list
    popularity_id = dict()
    genre_id = dict()
    for genre in genre_list:
        tmp_genre,tmp_pop = get_genre_songs(genre)
        genre_id.update(tmp_genre)
        popularity_id.update(tmp_pop)
    return (genre_id,popularity_id)

def get_genre_list_csv():
    data = dict()
    genre_id,popularity_id = get_all_genre_songs()
    for genre,songs in genre_id.items():
        data.update(get_songs_audio_features(songs,genre,popularity_id))
    data_df = pd.DataFrame.from_dict(data, orient='index')
    data_df.to_csv('Extradata.csv', index=False) 

def genre_playlist_names(genres):
    genre_playlist_names = set()
    for genre in genres:
        genre_playlist_names.add(f'the sound of {genre}')
    return genre_playlist_names

def get_spotify_genre_playlists(genre_playlists):
    offset = 0
    global access_token
    nextReqLink =  f'https://api.spotify.com/v1/users/thesoundsofspotify/playlists?offset=0&limit=50'
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    playlists_id = dict()
    req_made = 1
    try:
        while nextReqLink is not None:    
            resp =requests.get(nextReqLink, headers=auth_header)
            resp.raise_for_status()
            for playlist in resp.json()["items"]:
                name = playlist['name'].lower()
                if name in genre_playlists:
                    playlists_id[name[13:len(name)]] = playlist["id"]
            offset+= 50
            nextReqLink = resp.json()['next']
            req_made+=1
    except requests.exceptions.HTTPError as err:
        print("ERR:" + str(err))
    return playlists_id

def chunks(lst, n): # We have to split our playlist requests in chunks of 50
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_playlist_songs(playlist):
    market_id = 'US'
    global access_token
    songs = list()
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    req_endpoint = f"https://api.spotify.com/v1/playlists/{playlist}/tracks?market={market_id}&limit=100&field=items(track(id))"
    try:
        resp =requests.get(req_endpoint, headers=auth_header)
        resp.raise_for_status()
        for track in resp.json()["items"]:
            songs.append(track['track']['id'])
    except requests.exceptions.HTTPError as err:
        print("ERR:" + str(err))
    return songs

def get_songs_audio_features(song_ids,genre,popularity_id=None):
    global access_token
    song_id_req = list(chunks(list(song_ids),50)) # In case they have more than 50 songs which is likely we need to split requests up into batches of 50.
    audio_dict = dict()
    for req in song_id_req:
        id_str =  ",".join(req)
        req_endpoint = f'https://api.spotify.com/v1/audio-features/?ids={id_str}'
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        audio_j = ""
        try:
            resp =requests.get(req_endpoint, headers=auth_header)
            resp.raise_for_status()
            audio_j = resp.json()
            temp_d = {}
            for a in audio_j['audio_features']:
                temp_d[a['id']] = a
                temp_d[a['id']]['genre'] = genre
                temp_d[a['id']].pop('type', None)
                temp_d[a['id']].pop('uri', None)
                temp_d[a['id']].pop('analysis_url', None)
                temp_d[a['id']].pop('track_href', None)
                if popularity_id is not None :
                    temp_d[a['id']]['popularity'] = popularity_id[a['id']]
            audio_dict.update(temp_d)
        except requests.exceptions.HTTPError as err:
            print("ERR:" + str(err))
    return audio_dict

def get_genre_csv():
    genres = get_spotify_genre_playlists(genre_playlist_names(get_genres()))
    data = dict()
    for genre,playlist_id in genres.items():
        genre_songs = get_playlist_songs(playlist_id)
        data.update(get_songs_audio_features(genre_songs,genre))
    data_df = pd.DataFrame.from_dict(data, orient='index')
    data_df.to_csv('Everynoisedata.csv', index=False)  

get_genre_list_csv()
