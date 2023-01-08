from dash import dcc, html
import plotly.graph_objects as go
import geopandas as gp
from urllib.request import urlopen
import json

class Map(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        print("HI!")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
    
    def update(self):
        self.fig = go.Figure()

        with urlopen('https://raw.githubusercontent.com/veltman/snd3/master/data/nyc-neighborhoods.geo.json') as response:
            neighbourhoods = json.load(response)
        
        self.fig.add_trace(go.Choropleth(self.df, geojson=neighbourhoods))



        return self.fig