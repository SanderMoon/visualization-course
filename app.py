from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout, make_header_layout
from jbi100_app.views.map import Map
from jbi100_app.views.distribution import Distribution
from jbi100_app.views.multiscatter import MultiScatter
from jbi100_app.views.relationship import Relationship
from dash import html, ctx
from dash.dependencies import Input, Output
from jbi100_app import data

if __name__ == '__main__':
    # Create data
    df = data.get_data()

    # Create the visualization instances
    map = Map("Map", df)
    distribution = Distribution("Distribution", df)
    relationship = Relationship("Relationship", "price", "number of reviews", df)

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Header(
                id="header",
                className="twelve columns",
                children=make_header_layout()
            ),

            # Create sidebar
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout(df)
            ),

            # Create visualizations
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    map,
                    distribution,
                    relationship
                ],
            ),

        ],
    )

    # Callback for output relationship graph
    @app.callback(
        Output(relationship.html_id, "figure"),
        Input("host_id", "value"),
        Input("neighbourhood_group", "value"),
        Input("instant_bookable", "value"),
        Input("cancellation_policy", "value"),
        Input("room_type", "value"),
        Input("price", "value"),
        Input("service_fee", "value"),
        Input("nr_nights", "value"),
        Input("nr_reviews", "value"),
        Input("rating", "value"),
        Input("first_vars", "value"),
        Input("second_vars", "value"),
        Input(map.html_id, "clickData")
    )
    def update_relationship(host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, value1, value2, click_data):

        triggered_id = ctx.triggered_id

        return relationship.update(host_id, neighbourhood_group, instant_bookable, cancellation, room_type,
                                   price, service_fee, nr_nights, nr_reviews, rating, value1, value2, click_data,
                                   triggered_id)

    # Callback for map output
    @app.callback(
        Output(map.html_id, "figure"), [
            Input("boolean_switch", "on"),
            Input("map_var", "value"),
            Input("host_id", "value"),
            Input("neighbourhood_group", "value"),
            Input("instant_bookable", "value"),
            Input("cancellation_policy", "value"),
            Input("room_type", "value"),
            Input("price", "value"),
            Input("service_fee", "value"),
            Input("nr_nights", "value"),
            Input("nr_reviews", "value"),
            Input("rating", "value"),
            Input(map.html_id, "clickData"),
            Input(distribution.html_id, "selectedData"),
            Input("first_vars", "value"),
            Input("second_vars", "value")
        ])
    def update_map(on, selected_variable, host_id, neighbourhood_group, instant_bookable, cancellation, room_type,
                   price, service_fee, nr_nights, nr_reviews, rating, click_data, selected_data_relationship,
                   selected_data_dist, relationship_second):
        return map.update(on, selected_variable, host_id, neighbourhood_group, instant_bookable, cancellation,
                          room_type, price, service_fee, nr_nights, nr_reviews, rating, click_data,
                          selected_data_relationship, selected_data_dist, relationship_second, ctx.triggered_id)

    # Callback for distribution graph output
    @app.callback(
        Output(distribution.html_id, "figure"),
        Input("map_var", "value"),
        Input("host_id", "value"),
        Input("neighbourhood_group", "value"),
        Input("instant_bookable", "value"),
        Input("cancellation_policy", "value"),
        Input("room_type", "value"),
        Input("price", "value"),
        Input("service_fee", "value"),
        Input("nr_nights", "value"),
        Input("nr_reviews", "value"),
        Input("rating", "value"),
        Input(map.html_id, "clickData")
    )
    def update_distribution(x_var, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, click_data):
        return distribution.update(x_var, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                                   service_fee, nr_nights, nr_reviews, rating, click_data, ctx.triggered_id)

    # Callback for boolean toggle borough - neighbourhood
    @app.callback(
        Output("boolean_switch", "on"), [
            Input(map.html_id, "clickData"),
            Input(relationship.html_id, "selectedData")
        ])
    def update_switch(click_data, selected_data):
        boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

        # Checks if a borough was clicked
        if click_data is not None:
            if click_data["points"][0]["location"] in boroughs:
                view = "borough"
            else:
                view = "neighbourhood"

        # Checks if borough was clicked in the relationship graph
        if selected_data is not None:
            view = "borough"
            if map.relationship_var == "neighbourhood group":
                if selected_data["points"][0]["label"] not in boroughs:
                    view = "neighbourhood"

        # Sets toggle on or off
        if view == "borough":
            return {"on": False}
        else:
            return {"on": True}

    app.run_server(debug=True, dev_tools_ui=True)
