import pandas as pd
import re
import requests


df = pd.read_csv('pg_catalog.csv')

print(df.columns)



# Split Subjects and Bookshelves by ';'
df['Subjects'] = df['Subjects'].str.split(';')
df['Bookshelves'] = df['Bookshelves'].str.split(';')

# Combine them into Genres
df['Genres'] = df['Subjects'] + df['Bookshelves']

# Function to split '--' in each genre entry
def split_double_dash(genres_list):
    """
    Takes a list of genre strings, splits any '--' inside each,
    flattens to a single list.
    """
    if not isinstance(genres_list, list):
        return []
    result = []
    for genre in genres_list:
        parts = genre.split('--')
        for part in parts:
            result.append(part.strip())
    return result

df['Genres'] = df['Genres'].apply(split_double_dash) # Ensure Genres is a list

# Remove dates from Authors
def clean_author(author): # Ensure Author is a string
    if not isinstance(author, str):
        return author
    return re.sub(r'\s*\(\d{4}(-\d{4})?\)', '', author) # Remove year in parentheses

df['Authors'] = df['Authors'].apply(clean_author)



# Remove "Browsing: " and extra spaces
def clean_genres(genres_list): # Ensure Genres is a list
    cleaned = []
    for g in genres_list:
        g = g.replace('Browsing: ', '').strip()
        cleaned.append(g)
    return cleaned

df['Genres'] = df['Genres'].apply(clean_genres) # Ensure Genres is a list

# limit genres to 10
df['Genres'] = df['Genres'].apply(lambda x: x[:10] if isinstance(x, list) else [])

print("Genres done!")

new_df= df[['Text#', 'Title', 'Authors', 'Genres']].copy()

#get ISBN and page count from Open Library based on title and author

# add ISBN and page count to the dataframe

print(df.head())

print(new_df.head())


#df.to_csv('new_pg_catalog.csv', index=False)

new_df.to_csv('new_pg_catalog.csv', index=False)