from dash import dcc, html
import plotly.express as px
import json
import pandas as pd
from jbi100_app import data

class Map(html.Div):
    def __init__(self, name, df: pd.DataFrame):
        self.html_id = name.lower().replace(" ", "-")
        self.view = "borough"

        self.df = df
        self.neighbourhoods = json.load(open("data/neighbourhoods.geojson", "r"))
        self.boroughs = json.load(open("data/boroughs.geojson", "r"))

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

    def aggregateData(self, df: pd.DataFrame, groupby):
        aggregatedData = df.groupby(by=groupby, as_index=False).mean(numeric_only=True)

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
    
    def update(self, on, selected_variable, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, click_data, triggered_id):
        
        df_processed = data.filter_data(self.df, [host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating])
        df_processed_neighbourhood = self.aggregateData(df_processed, "neighbourhood")
        df_processed_borough = self.aggregateData(df_processed, "neighbourhood group")
        
        # This runs if the figure is updated because of a click in the figure
        if triggered_id == "map":
            source = "borough" if click_data["points"][0]["location"] in ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"] else "neighbourhood"

            if source == "borough":
                borough = click_data["points"][0]["location"]

                self.fig = px.choropleth_mapbox(
                    df_processed_neighbourhood,
                    featureidkey = "properties.neighborhood",
                    geojson=self.neighbourhoods,
                    color = df_processed_neighbourhood[selected_variable],
                    locations= df_processed_neighbourhood["neighbourhood"],
                    color_continuous_scale="greens",
                    width= 1000,
                    height= 800  
                )   

        # This runs if the figure is updated by a sidebar filter or on launch
        else:
            if on:
                self.fig = px.choropleth_mapbox(
                    df_processed_neighbourhood,
                    featureidkey = "properties.neighborhood",
                    geojson=self.neighbourhoods,
                    color = df_processed_neighbourhood[selected_variable],
                    locations= df_processed_neighbourhood["neighbourhood"],
                    color_continuous_scale="greens",
                    width= 1000,
                    height= 800  
                )
            else:
                self.fig = px.choropleth_mapbox(
                    df_processed_borough,
                    featureidkey = "properties.boro_name",
                    geojson=self.boroughs,
                    color = df_processed_borough[selected_variable],
                    locations= df_processed_borough["neighbourhood group"],
                    color_continuous_scale="greens",
                    width= 1000,
                    height= 800  
                )

        self.fig.update_layout(
            mapbox_style = "carto-positron",
            mapbox_zoom = 9,
            mapbox_center = {"lat": 40.73, "lon":-73.93},
            clickmode="event+select"                          
        )

        return self.fig