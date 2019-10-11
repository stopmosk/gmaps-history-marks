import json
import pandas as pd
from pandas.io.json import json_normalize

#data = json_normalize(json.load(open(file, 'r'))['locations'])

#with open("hi.json", "r") as read_file:
#    data = json.load(read_file)

#json.load('hi.json')

df = pd.read_json('hi500.json')
#print(df)
data = json_normalize(df['locations'])
print(data.head(10))
