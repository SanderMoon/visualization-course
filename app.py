from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.splom import Splom
from jbi100_app.views.map import Map
import jbi100_app.data as data

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # Create data
    df_iris, df_air = data.get_data()

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df_iris)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df_iris)
    features = ["sepal_width", "sepal_length", "petal_width", "petal_length"]
    splom = Splom("splom", features, df_iris)
    map = Map("map", df_air)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    splom, map
                ],
            ),
        ],
    )

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