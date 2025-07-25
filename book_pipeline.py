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



def lookup_open_library(title, author): # Ensure title and author are strings
    query = f"{title} {author}"
    url = "https://openlibrary.org/search.json" # Open Library search API
    params = {"q": query, "limit": 1} # Limit to 1 result

    response = requests.get(url, params=params) # Ensure response is valid
    if response.status_code != 200: # Check if the request was successful
        return None

    data = response.json() # Parse the JSON response
    docs = data.get("docs", []) # Get the list of documents
    if not docs:
        return None

    top = docs[0] # Get the top result
    isbn_list = top.get("isbn", []) # Get ISBNs from the top result
    isbn = isbn_list[0] if isbn_list else None # Use the first ISBN if available
    pages = top.get("number_of_pages_median", None) # Get the median number of pages
    return {"isbn": isbn, "pages": pages} # Return a dictionary with ISBN and pages


# Add new columns
df['ISBN'] = None
df['Pages'] = None

# Look up each row (limit to first few for testing!)
for idx, row in df.iterrows():
    result = lookup_open_library(row['Title'], row['Authors'])
    if result:
        df.at[idx, 'ISBN'] = result['isbn']
        df.at[idx, 'Pages'] = result['pages']

print(df.head())

df.to_csv('new_pg_catalog.csv', index=False)
