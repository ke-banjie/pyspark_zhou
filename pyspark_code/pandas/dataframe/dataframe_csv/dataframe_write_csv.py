import pandas as pd

df = pd.read_csv('nba.csv', header=0, names=['name', 'age'])

print(df.to_string())