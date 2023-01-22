from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
from sklearn.model_selection import train_test_split
import jbi100_app.data as data


class Relationship(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower()
        self.df = df
        self.train, self.test = train_test_split(self.df, test_size=0.05)
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.processed_df = self.df

        # define 3 cases
        self.type_first_var = None
        self.type_second_var = None

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, host_id, neighbourhood_group, instant_bookable, cancellation, room_type,
               price, service_fee, nr_nights, nr_reviews, rating, var1, var2, triggered_id):

        if triggered_id != "first_vars" or triggered_id != "second_vars":
            list = [host_id, neighbourhood_group, instant_bookable, cancellation, room_type,
                    price, service_fee, nr_nights, nr_reviews, rating]
            filtered_df = data.filter_data(self.df, list)
            self.processed_df = filtered_df
            self.train, self.test = train_test_split(self.processed_df, test_size=0.05)


        self.fig = go.Figure()

        # define 3 cases
        self.type_first_var = "categorical"
        self.type_second_var = "categorical"
        match var1:
            case "host_identity_verified" | "neighbourhood group" | "instant_bookable" | "cancellation_policy" | \
                 "room type" | "review rate number":
                self.type_first_var = "categorical"
            case "price" | "service fee" | "minimum nights" | "number of reviews" | \
                 "reviews per month" | "availability 365":
                self.type_first_var = "interval"

        match var2:
            case "host_identity_verified" | "neighbourhood group" | "instant_bookable" | "Cancellation_policy" | \
                 "room type" | "review rate number":
                self.type_second_var = "categorical"
            case "price" | "service fee" | "minimum nights" | "number of reviews" | \
                 "reviews per month" | "availability 365":
                self.type_second_var = "interval"

        x_values = self.test[var1]
        y_values = self.test[var2]

        # case 1
        if self.type_first_var == "interval" and self.type_second_var == "interval":
            self.fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker_color='#123C69'
            ))

            self.fig.update_traces(overwrite=True, mode='markers', marker_size=10)
            self.fig.update_layout(
                yaxis_zeroline=False,
                xaxis_zeroline=False,
                dragmode='select'
            )
            self.fig.update_xaxes(fixedrange=True)
            self.fig.update_yaxes(fixedrange=True)

            # # highlight points with selection other graph
            # if selected_data is None:
            #     selected_index = self.df.index  # show all
            # else:
            #     selected_index = [  # show only selected indices
            #         x.get('pointIndex', None)
            #         for x in selected_data['points']
            #     ]
            #
            # self.fig.data[0].update(
            #     selectedpoints=selected_index,
            #
            #     # color of selected points
            #     selected=dict(marker=dict(color=selected_color)),
            #
            #     # color of unselected pts
            #     unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
            # )

            # update axis titles
            self.fig.update_layout(
                xaxis_title=var1,
                yaxis_title=var2,
            )

        if self.type_first_var == "categorical" and self.type_second_var == "categorical":
            counts = self.processed_df.groupby(var1)[var2].value_counts()
            for group, group_df in counts.groupby(level=0):
                self.fig.add_bar(name=group, y=group_df.index.get_level_values(1), x=group_df.values)

            self.fig.update_traces(orientation='h')
            self.fig.update_layout(barmode='group',
                                   xaxis_title="Number of listings")

        if self.type_first_var == "categorical" and self.type_second_var == "interval":
            self.fig.add_box(x=self.processed_df[var2], y=self.processed_df[var1])
            self.fig.update_traces(orientation='h')
            self.fig.update_layout(
                xaxis_title=var2,
                yaxis_title=var1,
            )

        if self.type_first_var == "interval" and self.type_second_var == "categorical":
            self.fig.add_box(x=self.processed_df[var1], y=self.processed_df[var2])
            self.fig.update_traces(orientation='h')
            self.fig.update_layout(
                xaxis_title=var1,
                yaxis_title=var2,
            )

        return self.fig
