import pandas as pd


df=pd.read_csv('pg_catalog.csv')

# Add genres to the dataset
df['Subjects'] = df['Subjects'].str.split(';')
df['Bookshelves'] = df['Bookshelves'].str.split(';')
df['Genres']=df['Subjects']+df['Bookshelves']
df['Genres']=df['Genres'].str.split('--')
df['Genres'] = df['Genres'].str.replace('Browsing: ', '')


new_df=df[['Authors', 'Title', 'Genres']]


print(new_df.head()) # Display the first few rows of the DataFrame

new_df.to_csv('new_pg_catalog.csv', index=False) # Save the modified DataFrame to a new CSV file
