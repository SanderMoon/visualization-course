import plotly.express as px
import pandas as pd


def get_data():
    # Read data
    df = px.data.iris()
    df_air = pd.read_csv("data/airbnb_open_data.csv")

    # Any further data preprocessing can go here

    return df, df_air
