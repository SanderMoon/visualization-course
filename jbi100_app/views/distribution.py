from dash import dcc, html
import pandas as pd
import numpy as np
from jbi100_app import data
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split


class Distribution(html.Div):
    def __init__(self, name, df: pd.DataFrame):
        self.fig = go.Figure()
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.train, self.test = train_test_split(self.df, test_size=0.5)

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, x_var, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
               service_fee, nr_nights, nr_reviews, rating, click_data, triggered_id):
        '''
        Updates the data for this graph based on the filtered data

        :param x_var: the variable to show the distribution for
        :param host_id: variable to be filtered on
        :param neighbourhood_group: variable to be filtered on
        :param instant_bookable: variable to be filtered on
        :param cancellation: variable to be filtered on
        :param room_type: variable to be filtered on
        :param price: variable to be filtered on
        :param service_fee: variable to be filtered on
        :param nr_nights: variable to be filtered on
        :param nr_reviews: variable to be filtered on
        :param rating: variable to be filtered on
        :param click_data: variable to be filtered on
        :param triggered_id: variable to be filtered on
        :return: nothing
        '''

        self.fig = go.Figure()

        # Check if the map was clicked
        if triggered_id == "map":
            boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

            if click_data["points"][0]["location"] in boroughs:
                neighbourhood_group = [click_data["points"][0]["location"]]
                df_processed = data.filter_data(self.df, [host_id, neighbourhood_group, instant_bookable, cancellation,
                                                          room_type, price, service_fee, nr_nights, nr_reviews, rating])
            else:
                df_processed = self.df.loc[self.df["neighbourhood"] == click_data["points"][0]["location"]]

        else:
            # filter the data normally
            df_processed = data.filter_data(self.df, [host_id, neighbourhood_group, instant_bookable, cancellation,
                                                      room_type, price, service_fee, nr_nights, nr_reviews, rating])

        # Data is too big, we can split it randomly to make the program faster
        self.train, self.test = train_test_split(df_processed, test_size=0.5)
        self.var = self.test[x_var]

        # calculate the range of the data
        data_range = np.ptp(self.var)

        # calculate the number of bins
        bins = int(np.ceil(data_range / 1))
        if bins > 300:
            bins = bins // 8
        elif bins > 100:
            bins = bins // 4

        # Create the histogram on x_var with the number of bins as specified
        self.fig.add_trace(go.Histogram(x=self.var, histnorm='percent', nbinsx=bins))

        # Update the layout of the graph
        self.fig.update_layout(
            xaxis_title=x_var,
            yaxis_title="Percentage of cases",
            clickmode="event+select"
        )

        # Update the style of the graph
        self.fig.update_traces(
            opacity=0.85,
            marker_line_width=0.5,
            marker_line_color="white")

        return self.fig
