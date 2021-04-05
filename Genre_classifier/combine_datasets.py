import pandas as pd

extra_data = pd.read_csv('Extradata.csv')
spotify_data = pd.read_csv('Cleaned.csv')
extra_data = extra_data.rename(columns={"id": "track_id"})
merged_data = pd.concat([spotify_data,extra_data], axis=0)
merged_data.drop_duplicates(subset=['track_id'])
merged_data.to_csv("Merge.csv",index=False)
