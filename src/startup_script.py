import pandas as pd
import os

def show_data_stats(df):
    print("Number of rows: " + str(len(df.axes[0])))
    print("Number of columns: " + str(len(df.axes[1])))
    print(df.head(5))
    print(df.columns)
    


file = os.path.join(os.path.dirname(__file__), '..', 'data', 'airbnb_open_data.csv')
dataset_facts_path = os.path.join(os.path.dirname(__file__), '..', 'data')

print(file)
data = pd.read_csv(file)
print(data.columns)
show_data_stats(data)

