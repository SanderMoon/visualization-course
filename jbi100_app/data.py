import plotly.express as px
import pandas as pd


def get_data():
    # Read data
    df = pd.read_csv("airbnb_data.csv")

    # One listing has a typo
    for index, group in df["neighbourhood group"].items():
        if group == "brookln":
            df.at[index, "neighbourhood group"] = "Brooklyn"

    # Change booleans in 'instant bookable' to strings
    df["instant_bookable"] = df["instant_bookable"].map({True: 'True', False: 'False'})
    return df


def filter_data(df, varlist) -> pd.DataFrame:
    '''
    filters the data based on the input from the filters in the sidebar
    :param df: the current dataframe
    :param varlist: the list of variables that can be filtered on
    :return: the filtered df
    '''

    # Create a list of the variable names corresponding to the varlist input
    variables = ["host_identity_verified", "neighbourhood group", "instant_bookable", "cancellation_policy",
                 "room type", "price", "service fee", "minimum nights", "number of reviews", "review rate number"]
    if varlist[1] == "All":
        varlist[1] = ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"]

    # Filter the data based on what filters have been selected in the sidebar
    for index, value in enumerate(varlist):
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

