import pandas as pd
import numpy as np
import os

file = os.path.join(os.path.dirname(__file__), '..', 'data', 'airbnb_open_data.csv')
data = pd.read_csv(file)
data['price'] = data['price'].replace({'\W':''}, regex = True)
data['service fee'] = data['service fee'].replace({'\$':''}, regex = True)

data['price'] = data['price'].astype('double')
data['service fee'] = data['service fee'].astype('double')
data['last review'] = data['last review'].astype('datetime64')


print(len(data['price'][(data['price'] - data['price'].mean()).abs() > (3*data['price'].std())]))


print(data.dtypes)


summary = pd.DataFrame(columns=['Attribute', '#_Null', '#_Outlier', 'Unique_values', 'Most_frequent', 'Count_Most_Freq', 'Max', 'Min'])

for column in data:
    nunique = data[column].nunique()
    nnull = data[column].isnull().sum()
    most_freq = data[column].value_counts().idxmax()
    count_most_freq  = data[column].value_counts()[most_freq]
    max = np.NaN
    min = np.NaN
    noutlier = np.NaN
    try:
        max = data[column].max()
        min = data[column].min()
        noutlier = len(data[column][(data[column] - data[column].mean()).abs() > (3*data[column].std())])
    except:
        pass
    summary.loc[len(summary.index)] = [column, nnull, noutlier, nunique, most_freq, count_most_freq,max,min]



print(summary)
summary.to_csv('data_summary.csv')

