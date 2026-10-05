import pandas as pd

df = pd.read_json('sites.json')

print(df.to_string())