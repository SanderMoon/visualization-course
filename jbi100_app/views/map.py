from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import json
import pandas as pd

class Map(html.Div):
    def __init__(self, name, df: pd.DataFrame):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.neighbourhoods = json.load(open("data/neighbourhoods.geojson", "r"))

        self.df_agg = self.aggregateData(self.df)
        # print(self.df_agg)

        for feature in self.neighbourhoods["features"]:
            if feature["properties"]["neighborhood"] in self.df["neighbourhood"].unique():
                feature["id"] = feature["properties"]["neighborhood"]

                # This part downscales the polygons, turns out to be unnecessary
                # polygon = feature["geometry"]["coordinates"][0]
                # # feature["geometry"]["coordinates"][0] = self.downscalePolygon(polygon, 128)

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def aggregateData(self, df: pd.DataFrame):
        aggregatedData = df.groupby(by="neighbourhood", as_index=False).mean()

        return aggregatedData
    
    # Downscales polygons for the map. Polygons sizes differ in the range of [vertices, 2*vertices]
    def downscalePolygon(self, polygon: list, vertices: int = 16):
        length = len(polygon)
        if length <= vertices:
            return polygon

        ratio = length // (vertices - 1)
        smallPolygon = []

        for i in range(length):
            if i % ratio == 0:
                smallPolygon.append(polygon[i])
        smallPolygon.append(polygon[-1])

        return smallPolygon
    
    def update(self):
        self.fig = px.choropleth_mapbox(
            self.df_agg,
            featureidkey = "properties.neighborhood",
            geojson=self.neighbourhoods,
            color = self.df_agg["review rate number"],
            locations=self.df_agg["neighbourhood"],
            color_continuous_scale="viridis"
        )

        self.fig.update_layout(
            mapbox_style = "carto-positron",
            mapbox_zoom = 8,
            mapbox_center = {"lat": 40.73, "lon":-73.93}                               
        )

        return self.fig