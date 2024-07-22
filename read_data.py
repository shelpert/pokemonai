import pandas as pd
from itertools import batched
from collections import Counter

df = pd.read_csv("/Users/danielgu/Downloads/length_6_battles.csv")
data = zip(df["PlayerHP"], df["OpponentHP"])

for i in batched(data, 12):
    print(i)
    break
