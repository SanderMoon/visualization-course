import pandas as pd
import os

file = os.path.join(os.path.dirname(__file__), '..', 'data', 'airbnb_open_data.csv')
print(file)
data = pd.read_csv(file)
print(data.columns)