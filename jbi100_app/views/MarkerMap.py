from dash import dcc, html
import plotly.express as px
import json
import pandas as pd
import geopandas as gpd
from jbi100_app import data


class MarkerMap(html.Div):
    def __init__(self, name, df: pd.DataFrame):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        self.sups = pd.read_csv('data/MarkerData/supermarkets.csv')
        # self.laund = pd.read_csv('data/MarkerData/laundromats.csv')
        self.subways = json.load((open("data/MarkerData/SubwayStations.geojson", "r")))
        self.taxis = json.load((open("data/MarkerData/taxi_zones.geojson", "r")))
        self.artgalleries = json.load((open("data/MarkerData/artgalleries.geojson", "r")))

        # testprints
        print(self.sups.head(10))
        print(self.sups.tail(10))

        # TODO, selected hovers
        selfhover_vars = []

        super().__init__(className="graph_card",
                         children=[
                             html.H6(name),
                             dcc.Graph(id=self.html_id)
                         ], )

        # # Create the filters
        # filters = html.Div([
        #     html.Label("Dataset"),
        #     dcc.Dropdown(
        #         id="dataset-dropdown",
        #         options=[
        #             {"label": "Subway Stations", "value": self.subways},
        #             {"label": "Taxi Zones", "value": self.taxis},
        #             {"label": "Art Galleries", "value": self.artgalleries},
        #             {"label": "Supermarkets", "value": self.sups},
        #             {"label": "Laundromats", "value": self.laund}
        #         ],
        #         value=self.subways
        #     )
        # ])
        #
        # # Create the map
        # map = dcc.Graph(id="map")
        #
        # # Define the layout of the Dash app
        # df.layout = html.Div([
        #     html.H1("Map Plot Categories"),
        #     # filters,
        #     map
        # ])

        def update(value):
            if value == "supermarkets":
                self.fig = px.scatter_mapbox(self.df,
                                             lon=self.sups['Longitude'],
                                             lat=self.sups['Latitude'],
                                             zoom=3,
                                             color=self.sups['Borough'],
                                             width=1200,
                                             height=900,
                                             title="MarkerMap",
                                             )
            elif value == "laundromats":
                self.fig = px.scatter_mapbox(self.df,
                                             lon=self.sups['Longitude'],
                                             lat=self.sups['Latitude'],
                                             zoom=3,
                                             color=self.sups['Borough'],
                                             width=1200,
                                             height=900,
                                             title="MarkerMap",
                                             )
            elif value == "subways":
                self.fig = px.scatter_mapbox(self.df,
                                             lon=self.subways['coordinates'][0],
                                             lat=self.subways['coordinates'][1],
                                             zoom=3,
                                             color=self.sups['Borough'],
                                             width=1200,
                                             height=900,
                                             title="MarkerMap",
                                             )
            elif value == "taxis":
                self.fig = px.scatter_mapbox(self.df,
                                             lon=self.taxis['coordinates'][0],
                                             lat=self.taxis['coordinates'][1],
                                             zoom=3,
                                             color=self.sups['Borough'],
                                             width=1200,
                                             height=900,
                                             title="MarkerMap",
                                             )
            elif value == "ArtGalleries":
                self.fig = px.scatter_mapbox(self.df,
                                             lon=self.artgalleries['coordinates'][0],
                                             lat=self.artgalleries['coordinates'][1],
                                             zoom=3,
                                             color=self.sups['Borough'],
                                             width=1200,
                                             height=900,
                                             title="MarkerMap",
                                             )

        self.fig = px.scatter_mapbox(self.df, lat="lat", lon="long", color="price",
                                     color_continuous_scale=px.colors.sequential.Plasma)
        self.fig.update_layout(mapbox_style="open-street-map")
        self.fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 10})
        self.fig.show()
        return self.fig
