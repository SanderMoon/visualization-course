from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout, make_header_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.splom import Splom
from jbi100_app.views.map import Map
from jbi100_app.views.multiscatter import MultiScatter

from dash import html
from dash.dependencies import Input, Output
from jbi100_app import data


if __name__ == '__main__':
    # Create data
    # df = px.data.iris()
    df = data.get_data()

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)
    features = ["sepal_width", "sepal_length", "petal_width", "petal_length"]
    splom = Splom("splom", features, df)
    map = Map("map", df)
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
                    splom, map, multiscatter
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

    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)
    
    @app.callback(
        Output(splom.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(splom.html_id, 'selectedData')
    ])
    def update_splom(selected_color, selected_data):
        return splom.update(selected_color, selected_data)

    @app.callback(
        Output(map.html_id, "figure"), [
        Input(map.html_id, "selectedData")
    ])
    def update_map(selected_data):
      return map.update()


    app.run_server(debug=True, dev_tools_ui=True)