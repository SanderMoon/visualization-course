import plotly.express as px
import pandas as pd


def get_data():
    # Read data
    df = pd.read_csv("airbnb_data.csv")

    for index, group in df["neighbourhood group"].items():
        if group == "brookln":
            df.at[index, "neighbourhood group"] = "Brooklyn"

    df["instant_bookable"] = df["instant_bookable"].map({True: 'True', False: 'False'})
    return df


def filter_data(df, list):
    variables = ["host_identity_verified", "neighbourhood group", "instant_bookable", "cancellation_policy",
                 "room type", "price", "service fee", "minimum nights", "number of reviews", "review rate number"]
    if list[1] == "All":
        list[1] = ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"]

    for index, value in enumerate(list):
        if value == []:
            value = None
        if value is not None:
            variable = variables[index]
            if variable == "price" or variable == "service fee" or variable == "minimum nights" or \
                    variable == "number of reviews" or variable == "review rate number":
                df = df.loc[(df[variable] >= value[0]) & (df[variable] <= value[1])]
            else:
                if len(value) == 1:
                    df = df.loc[df[variable] == value[0]]
                else:
                    df = df.loc[df[variable].isin(value)]

    return df

