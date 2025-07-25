import pandas as pd
import re
import requests

df = pd.read_csv('tcc_ceds_music.csv')

# Rename the first column to 'id' regardless of its current name
df.rename(columns={df.columns[0]: 'id'}, inplace=True)

print(df.columns)

df = df[['id', 'artist_name', 'track_name', 'release_date', 'genre']]

print(df.head())

df.to_csv('new_tcc_ceds_music.csv', index=False)

df100 = df.head(100)

df100.to_json('music_json.json', orient='records', force_ascii=False, indent=4)
