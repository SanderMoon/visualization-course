from dash import dcc, html
import plotly.express as px
import json
import pandas as pd
import numpy as np
from jbi100_app import data
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split

class Distribution(html.Div):
    def __init__(self, name, df: pd.DataFrame):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.train, self.test = train_test_split(self.df, test_size=0.5)


        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, xvar, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, click_data, triggered_id):

        self.fig = go.Figure()

        if triggered_id == "map":
            boroughs = ["Bronx", "Brooklyn", "Manhatten", "Queens", "Staten Island"]
            if click_data["points"][0]["location"] in boroughs:
                neighbourhood_group = [click_data["points"][0]["location"]]
                df_processed = data.filter_data(self.df, [host_id, neighbourhood_group, instant_bookable, cancellation,
                                                  room_type, price, service_fee, nr_nights, nr_reviews, rating])
            else:
                df_processed = self.df.loc[self.df["neighbourhood"] == click_data["points"][0]["location"]]

        else:
            df_processed = data.filter_data(self.df, [host_id, neighbourhood_group, instant_bookable, cancellation,
                                                  room_type, price, service_fee, nr_nights, nr_reviews, rating])

        self.train, self.test = train_test_split(df_processed, test_size=0.5)
        self.var = self.test[xvar]

        # calculate the range of the data
        data_range = np.ptp(self.var)

        # calculate the number of bins
        bins = int(np.ceil(data_range / 1))
        if bins > 300:
            bins = bins // 8
        elif bins > 100:
            bins = bins // 4

        self.fig.add_trace(go.Histogram(x=self.var, histnorm='percent', nbinsx=bins))

        self.fig.update_layout(
            xaxis_title=xvar,
            yaxis_title="Percentage of cases",
            clickmode="event+select"
        )

        self.fig.update_traces(
            opacity=0.85,
            marker_line_width=0.5,
            marker_line_color="white")

        return self.fig