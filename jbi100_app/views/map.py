from dash import dcc, html
import plotly.express as px
import json
import pandas as pd
from jbi100_app import data


class Map(html.Div):
    def __init__(self, name, df: pd.DataFrame):
        self.html_id = name.lower().replace(" ", "-")

        # Load in the airbnb and geojson data
        self.df = df
        self.neighbourhoods = json.load(open("data/neighbourhoods.geojson", "r"))
        self.boroughs = json.load(open("data/boroughs.geojson", "r"))

        # Variable for the map/relationship interaction
        self.relationship_var = "neighbourhood group"

        # Variables to show on hover
        self.hover_vars = ["price", "service fee", "minimum nights", "number of reviews", "review rate number", "availability 365", "number of listings"]

        # Add an id item to the neighbourhoods to connect datasets
        for feature in self.neighbourhoods["features"]:
            if feature["properties"]["neighborhood"] in self.df["neighbourhood"].unique():
                feature["id"] = feature["properties"]["neighborhood"]

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    # Function that aggregates the data either on neighbourhood or borough level
    def aggregateData(self, df: pd.DataFrame, groupby):
        aggregatedData = df.groupby(by=groupby, as_index=False).mean(numeric_only=True).round(2)
        aggregatedData["number of listings"] = df.groupby(by=groupby, as_index=False).count()["Unnamed: 0"]

        return aggregatedData
    
    # This runs on launch and whenever a callback is triggered for the map
    def update(self, on, selected_variable, host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating, click_data, selected_data_relationship, selected_data_dist, 
                            relationship_second, triggered_id):
        
        # Filters the data based on which filter is used
        df_processed = data.filter_data(self.df, [host_id, neighbourhood_group, instant_bookable, cancellation, room_type, price,
                            service_fee, nr_nights, nr_reviews, rating])
        
        # The average latitude and longitude
        lat = 40.73
        long = -73.93

        # This runs if the relationship's y_var is updated
        if triggered_id == "second_vars":
            # Update the relationship variable
            self.relationship_var = relationship_second

        # This runs if the figure is updated because of a click in the distribution graph
        if triggered_id == "distribution":

            lat = 40.73
            long = -73.93
            zoom = 9

            # Identify which points are selected
            point_indices = []
            for point in selected_data_dist["points"]:
                point_indices += point["pointNumbers"]
            
            # Filter the data on these points
            filtered_df = df_processed.filter(items=point_indices, axis=0)

            # If we are in neighbourhood view 
            if on:

                # Aggregate the data
                df_processed_neighbourhood = self.aggregateData(filtered_df, "neighbourhood")

                # Plot the map
                self.fig = px.choropleth_mapbox(
                    df_processed_neighbourhood,
                    featureidkey="properties.neighborhood",
                    geojson=self.neighbourhoods,
                    color=df_processed_neighbourhood[selected_variable],
                    locations=df_processed_neighbourhood["neighbourhood"],
                    color_continuous_scale="greens",
                    width=1000,
                    height=800,
                    hover_data=self.hover_vars
                )

            # If we are in borough view
            else:

                # Aggregate the data
                df_processed_borough = self.aggregateData(filtered_df, "neighbourhood group")

                # Plot the map
                self.fig = px.choropleth_mapbox(
                    df_processed_borough,
                    featureidkey="properties.boro_name",
                    geojson=self.boroughs,
                    color=df_processed_borough[selected_variable],
                    locations=df_processed_borough["neighbourhood group"],
                    color_continuous_scale="greens",
                    width=1000,
                    height=800,
                    hover_data=self.hover_vars
                )

        # This runs if the figure is updated because of a click in the relationship graph
        elif triggered_id == "relationship":

            # Check what type of graph relationship currently is
            if "label" in selected_data_relationship["points"][0]:
                graph_type = "bar"
            else:
                graph_type = "scatter"

            # Update map if relationship graph is a scatter plot
            if graph_type == "scatter":
                lat = 40.73
                long = -73.93
                zoom = 9

                # Identify selected points
                point_indices = []
                for point in selected_data_relationship["points"]:
                    point_indices.append(point["pointIndex"])
                
                # Filter on the selected points
                filtered_df = df_processed.filter(items= point_indices, axis=0)

                # If we are in neighbourhood view
                if on:

                    # Aggregate the data
                    df_processed_neighbourhood = self.aggregateData(filtered_df, "neighbourhood")

                    # Plot the map
                    self.fig = px.choropleth_mapbox(
                        df_processed_neighbourhood,
                        featureidkey="properties.neighborhood",
                        geojson=self.neighbourhoods,
                        color=df_processed_neighbourhood[selected_variable],
                        locations=df_processed_neighbourhood["neighbourhood"],
                        color_continuous_scale="greens",
                        width=1000,
                        height=800,
                        hover_data=self.hover_vars
                    )

                # If we are in borough view
                else:

                    # Aggregate the data
                    df_processed_borough = self.aggregateData(filtered_df, "neighbourhood group")

                    # Plot the map
                    self.fig = px.choropleth_mapbox(
                        df_processed_borough,
                        featureidkey="properties.boro_name",
                        geojson=self.boroughs,
                        color=df_processed_borough[selected_variable],
                        locations=df_processed_borough["neighbourhood group"],
                        color_continuous_scale="greens",
                        width=1000,
                        height=800,
                        hover_data=self.hover_vars
                    )

            # Update map if relationship graph is a bar chart
            if graph_type == "bar":

                # The level of the categorical variable to be filtered on
                value = selected_data_relationship["points"][0]["label"]
                zoom = 10
                
                # Filter based on this variable
                df_processed_new = df_processed.loc[df_processed[self.relationship_var] == value]

                # If we filter on borough
                if self.relationship_var == "neighbourhood group":
                    
                    # Aggregate data on borough
                    df_processed_neighbourhood = self.aggregateData(df_processed_new, "neighbourhood")
                    
                    # Identify the latitudes and longitudes of the borough
                    lat = df_processed_neighbourhood["lat"].mean()
                    long = df_processed_neighbourhood["long"].mean()

                    # Plot the map
                    self.fig = px.choropleth_mapbox(
                        df_processed_neighbourhood,
                        featureidkey="properties.neighborhood",
                        geojson=self.neighbourhoods,
                        color=df_processed_neighbourhood[selected_variable],
                        locations=df_processed_neighbourhood["neighbourhood"],
                        color_continuous_scale="greens",
                        width=1000,
                        height=800,
                        hover_data=self.hover_vars
                    )
                
                # If we filter on another categorical variable
                else:

                    # If we are in neighbourhood view
                    if on:

                        # Aggregate the data and identify latitude and longitude
                        df_processed_neighbourhood = self.aggregateData(df_processed, "neighbourhood")
                        lat = df_processed_neighbourhood["lat"].mean()
                        long = df_processed_neighbourhood["long"].mean()

                        # Plot the map
                        self.fig = px.choropleth_mapbox(
                            df_processed_neighbourhood,
                            featureidkey="properties.neighborhood",
                            geojson=self.neighbourhoods,
                            color=df_processed_neighbourhood[selected_variable],
                            locations=df_processed_neighbourhood["neighbourhood"],
                            color_continuous_scale="greens",
                            width=1000,
                            height=800,
                            hover_data=self.hover_vars
                        )
                    
                    # If we are in borough view
                    else:

                        # Aggregate the data and identify latitude and longitude
                        df_processed_borough = self.aggregateData(df_processed, "neighbourhood group")
                        lat = df_processed_neighbourhood["lat"].mean()
                        long = df_processed_neighbourhood["long"].mean()

                        # Plot the map
                        self.fig = px.choropleth_mapbox(
                            df_processed_borough,
                            featureidkey="properties.boro_name",
                            geojson=self.boroughs,
                            color=df_processed_borough[selected_variable],
                            locations=df_processed_borough["neighbourhood group"],
                            color_continuous_scale="greens",
                            width=1000,
                            height=800,
                            hover_data=self.hover_vars
                        )

        # This runs if the figure is updated because of a click in the figure
        elif triggered_id == "map":

            # Check if we clicked on a borough or a neighbourhood
            source = "borough" if click_data["points"][0]["location"] in ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"] else "neighbourhood"
            zoom = 10

            # If we click on a borough
            if source == "borough":

                # The clicked borough
                borough = click_data["points"][0]["location"]

                # Filter and aggregate
                df_processed_new = df_processed.loc[df_processed["neighbourhood group"] == borough]
                df_processed_neighbourhood = self.aggregateData(df_processed_new, "neighbourhood")
                lat = df_processed_neighbourhood["lat"].mean()
                long = df_processed_neighbourhood["long"].mean()

                # Plot the map
                self.fig = px.choropleth_mapbox(
                    df_processed_neighbourhood,
                    featureidkey="properties.neighborhood",
                    geojson=self.neighbourhoods,
                    color=df_processed_neighbourhood[selected_variable],
                    locations=df_processed_neighbourhood["neighbourhood"],
                    color_continuous_scale="greens",
                    width=1000,
                    height=800,
                    hover_data=self.hover_vars
                )

        # This runs if the figure is updated by a sidebar filter or on launch
        else:
            lat = 40.73
            long = -73.93
            zoom = 9

            # If we are in neighbourhood view
            if on:

                # Aggregate data
                df_processed_neighbourhood = self.aggregateData(df_processed, "neighbourhood")

                # Plot the map
                self.fig = px.choropleth_mapbox(
                    df_processed_neighbourhood,
                    featureidkey="properties.neighborhood",
                    geojson=self.neighbourhoods,
                    color=df_processed_neighbourhood[selected_variable],
                    locations=df_processed_neighbourhood["neighbourhood"],
                    color_continuous_scale="greens",
                    width=1000,
                    height=800,
                    hover_data=self.hover_vars
                )
            # If we are in borough view
            else:

                # Aggregate data
                df_processed_borough = self.aggregateData(df_processed, "neighbourhood group")

                # Plot the map
                self.fig = px.choropleth_mapbox(
                    df_processed_borough,
                    featureidkey="properties.boro_name",
                    geojson=self.boroughs,
                    color=df_processed_borough[selected_variable],
                    locations=df_processed_borough["neighbourhood group"],
                    color_continuous_scale="greens",
                    width=1000,
                    height=800,
                    hover_data=self.hover_vars
                )

        # Update the layout
        self.fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=zoom,
            mapbox_center={"lat": lat, "lon": long},
            clickmode="event+select"
        )

        # Return fig
        return self.fig
