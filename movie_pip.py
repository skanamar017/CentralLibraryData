import pandas as pd
import re
import requests
import time
import random
import os
import ast



df = pd.read_csv('movies_metadata.csv')

def conv_gen(genres):
    gen_arr = []
    for genre in genres:
        gen_arr.append(genre['name'])
    return gen_arr

df['genres'] = df['genres'].apply(ast.literal_eval).apply(conv_gen)

print(df['genres'])
