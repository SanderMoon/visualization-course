from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout, make_header_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.splom import Splom
from jbi100_app.views.map import Map

from jbi100_app.views.multiscatter import MultiScatter
from jbi100_app.views.relationship import Relationship
import jbi100_app.data as data

from dash import Dash, html, ctx
import dash_daq as daq

from dash.dependencies import Input, Output, State
from jbi100_app import data

if __name__ == '__main__':
    # Create data
    df = data.get_data()

    map = Map("map", df)
    relationship = Relationship("relationship", "price", "number of reviews", df)
    multiscatter = MultiScatter("Multi-scatter", df)

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Header(
                id="header",
                className="twelve columns",
                children=make_header_layout()
            ),

            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout(df)
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    map,
                    relationship,
                    multiscatter
                ],
            ),

        ],
    )


    @app.callback(
        Output("Map", "figure"),
        Input("neighbourhood_group", "value")
    )
    def update_map(selected_neighbourhood):
        if selected_neighbourhood == "All":
            return map.update()


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
        Input("second_vars", "value")
    )
    def update_relationship(host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, value1, value2):

        triggered_id = ctx.triggered_id

        return relationship.update(host_id, neighbourhood_group, instant_bookable, cancellation, room_type,
                                   price, service_fee, nr_nights, nr_reviews, rating, value1, value2, triggered_id)

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
        Input(relationship.html_id, "selectedData"),
        Input("first_vars", "value"),
        Input("second_vars", "value")
    ])
    def update_map(on, selected_variable, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, click_data, selected_data, relationship_first, relationship_second):
        return map.update(on, selected_variable, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, click_data, selected_data, relationship_first, relationship_second, ctx.triggered_id)

    @app.callback(
        Output("boolean_switch", "on"), [
        Input(map.html_id, "clickData")
        ])
    def update_switch(click_data):
        boroughs = ["Bronx", "Brooklyn", "Manhatten", "Queens", "Staten Island"]
        print(click_data["points"][0]["location"])
        if click_data["points"][0]["location"] in boroughs:
            return {"on": True}
        else:
            return {"on": False}


    app.run_server(debug=True, dev_tools_ui=True)
