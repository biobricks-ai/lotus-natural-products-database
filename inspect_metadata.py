import pandas as pd
df = pd.read_csv('download/230106_frozen_metadata.csv.gz', nrows=5)
print(df.columns)
print(df.head(1))
