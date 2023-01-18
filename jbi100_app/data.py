import plotly.express as px
import pandas as pd


def get_data():
    # Read data
    df = pd.read_csv("airbnb_data.csv")

    for index, group in df["neighbourhood group"].items():
        if group == "brookln":
            df.at[index, "neighbourhood group"] = "Brooklyn"

    return df
