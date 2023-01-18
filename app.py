from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout, make_header_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.splom import Splom
from jbi100_app.views.map import Map

from jbi100_app.views.multiscatter import MultiScatter
from jbi100_app.views.relationship import Relationship
import jbi100_app.data as data

from dash import html
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
        filtered_df = df[df["neighbourhood group"] == selected_neighbourhood]

    @app.callback(
        Output(relationship.html_id, "figure"),
        # Input("submit-button-state", "n_clicks"),
        Input("first_vars", "value"),
        Input("second_vars", "value")
    )
    def update_relationship_graph(var_1, var_2):
        # print(n_clicks)
        # if n_clicks > 0:
        return relationship.update(var_1, var_2)



    # Define interactions
    # @app.callback(
    #     Output(scatterplot1.html_id, "figure"), [
    #     Input("select-color-scatter-1", "value"),
    #     Input(scatterplot2.html_id, 'selectedData')
    # ])
    # def update_scatter_1(selected_color, selected_data):
    #     return scatterplot1.update(selected_color, selected_data)
    #
    # @app.callback(
    #     Output(scatterplot2.html_id, "figure"), [
    #     Input("select-color-scatter-2", "value"),
    #     Input(scatterplot1.html_id, 'selectedData')
    # ])
    # def update_scatter_2(selected_color, selected_data):
    #     return scatterplot2.update(selected_color, selected_data)
    #
    # @app.callback(
    #     Output(splom.html_id, "figure"), [
    #     Input("select-color-scatter-1", "value"),
    #     Input(splom.html_id, 'selectedData')
    # ])
    # def update_splom(selected_color, selected_data):
    #     return splom.update(selected_color, selected_data)

    @app.callback(
        Output(map.html_id, "figure"), [
        Input(map.html_id, "selectedData")
    ])
    def update_map(selected_data):
      return map.update()


    app.run_server(debug=True, dev_tools_ui=True)