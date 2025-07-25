import pandas as pd
import re
import requests
import time
import random



df = pd.read_csv('pg_catalog.csv')# Load the CSV file into a DataFrame

#print(df.columns)



# Split Subjects and Bookshelves by ';'
df['Bookshelves'] = df['Bookshelves'].str.split(';')

# Combine them into Genres
df['Genres'] = df['Bookshelves']

# remove dates from authors
def clean_authors(authors):    
    if not isinstance(authors, str):
        return authors
    return re.sub(r",? ?\d{4}-\d{0,4}", "", authors)
df['Authors'] = df['Authors'].apply(clean_authors)


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

# Split authors by ';' and remove duplicates
def split_authors(authors):
    """
    Takes a string of authors, splits by ';', removes duplicates,
    and returns a list.
    """
    if not isinstance(authors, str):
        return []
    authors_list = [author.strip() for author in authors.split(';')]
    return list(set(authors_list))  # Remove duplicates 

df['Authors'] = df['Authors'].apply(split_authors) # Ensure Authors is a list

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



# print(df.head())

print(new_df.head())

# Generate unique 13-digit ISBNs
def generate_isbn13(n):
    isbns = set()
    while len(isbns) < n:
        isbn = str(random.randint(10**12, 10**13 - 1))
        isbns.add(isbn)
    return list(isbns)

isbn_list = generate_isbn13(len(new_df))
new_df['ISBN'] = isbn_list

# Assign random page numbers between 100 and 500
new_df['Pages'] = [random.randint(100, 500) for _ in range(len(new_df))]

new_df100 = new_df.head(100) # Limit to first 100 rows

# Save to CSV
new_df100.to_csv('new_pg_catalog_100.csv', index=False)

# Save to JSON
new_df100.to_json('book_json.json', orient='records', force_ascii=False, indent=4)


