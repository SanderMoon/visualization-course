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

# print(data.dtypes)

def getSummary(data):
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
          std = data[column].std()
          mean = data[column].mean()
          noutlier = len(data[column][(data[column] - mean).abs() > (3*std)])
      except:
          pass
      summary.loc[len(summary.index)] = [column, nnull, noutlier, nunique, most_freq, count_most_freq,max,min]

  print(summary)
  summary.to_csv('data_summary.csv')


def dropOutliers(data):
  columns = ['lat', 'long', 'Construction year', 'price', 'service fee', 'minimum nights',
       'number of reviews','reviews per month',
       'review rate number', 'calculated host listings count',
       'availability 365']
  for column in columns:
    std = data[column].std()
    mean = data[column].mean()
    data = data[ (data[column] - mean).abs() < (3 * std)]
  return data

data.drop('license', axis=1, inplace=True)
data.drop('house_rules', axis=1, inplace=True)
data.dropna(inplace=True)
data = dropOutliers(data)
data = data[data['minimum nights']>0]
data = data[data['availability 365']>0]
getSummary(data)

data.to_csv("airbnb_data.csv")
