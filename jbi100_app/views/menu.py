from dash import dcc
import numpy as np
from dash import html
import dash_daq as daq


def generate_header():
    return html.Header(
        id="title",
        children=[
            html.H1(
                children="AirBnB Data Visualization",
                style={
                    'textAlign': 'center'
                }),
            html.Div(
                id="description",
                children="Welcome to this visualization tool for New AirBnB hosts. "
                         "You can use the tool to find out everything about successful "
                         "and unsuccessful AirBnB's in New York ",
                style={
                    'textAlign': 'center'
                }
            ),
        ],
    )


def generate_neighbourhood_options(df):
    neighbourhood_options = df['neighbourhood group'].unique(),
    neighbourhoods = np.insert(neighbourhood_options[0], 0,  'All')
    return neighbourhoods


useful_vars = [{"label": "Host identity verified", "value": "host_identity_verified"},
               {"label": "Neighbourhood group", "value": "neighbourhood group"},
               {"label": "Instant bookable", "value": "instant_bookable"},
               {"label": "Cancellation policy", "value": "cancellation_policy"},
               {"label": "Room type", "value": "room type"},
               {"label": "Price", "value": "price"},
               {"label": "Service fee", "value": "service fee"},
               {"label": "Minimum number of nights", "value": "minimum nights"},
               {"label": "Number of reviews", "value": "number of reviews"},
               {"label": "Reviews per month", "value": "reviews per month"},
               {"label": "Review rate number", "value": "review rate number"},
               {"label": "Availability 365", "value": "availability 365"}]

useful_int_vars = [{"label": "Price", "value": "price"},
               {"label": "Service fee", "value": "service fee"},
               {"label": "Minimum number of nights", "value": "minimum nights"},
               {"label": "Number of reviews", "value": "number of reviews"},
               {"label": "Reviews per month", "value": "reviews per month"},
               {"label": "Review rate number", "value": "review rate number"},
               {"label": "Availability 365", "value": "availability 365"}]

value_index_map = {opt['value']: index for index, opt in enumerate(useful_vars)}


def generate_control_card(df):
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            # Graph filters
            html.Label("Filters for the map visualization"),
            # Toggle for neighbourhood/borough view
            html.Hr(),
            html.Label("Toggle between neighbourhood and borough view"),
            daq.BooleanSwitch(id="boolean_switch", on=False, color="#123c69"),
            # Select for different variables
            html.Br(),
            html.Label("Variable to visualize on map:"),
            dcc.Dropdown(
                id="map_var",
                options=useful_int_vars,
                value="price"
            ),

            html.Br(),

            # General variable filters
            html.Hr(),
            html.Label("Host identity verified", style={"font-weight": "bold"}),
            dcc.Checklist(
                id="host_id",
                options=df["host_identity_verified"].unique()
            ),

            html.Label("Neighbourhood group", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id="neighbourhood_group",
                options=generate_neighbourhood_options(df),
                value=generate_neighbourhood_options(df)[0],
                multi=True
            ),

            html.Label("Instant bookable", style={"font-weight": "bold"}),
            dcc.Checklist(
                id="instant_bookable",
                options=df["instant_bookable"].unique()
            ),

            html.Label("Cancellation Policy", style={"font-weight": "bold"}),
            dcc.Checklist(
                id="cancellation_policy",
                options=df["cancellation_policy"].unique()
            ),

            html.Label("Room type", style={"font-weight": "bold"}),
            dcc.Checklist(
                id="room_type",
                options=df["room type"].unique()
            ),

            html.Label("Price", style={"font-weight": "bold"}),
            dcc.RangeSlider(
                id="price",
                min=df["price"].min(),
                max=df["price"].max(),
                tooltip={"placement": "top", "always_visible": False}
            ),

            html.Label("Service fee", style={"font-weight": "bold"}),
            dcc.RangeSlider(
                id="service_fee",
                min=df["service fee"].min(),
                max=df["service fee"].max(),
                tooltip={"placement": "top", "always_visible": False}
            ),

            html.Label("Minimum number of nights", style={"font-weight": "bold"}),
            dcc.RangeSlider(
                id="nr_nights",
                min=df["minimum nights"].min(),
                max=df["minimum nights"].max(),
                tooltip={"placement": "top", "always_visible": False}
            ),

            html.Label("Number of reviews", style={"font-weight": "bold"}),
            dcc.RangeSlider(
                id="nr_reviews",
                min=df["number of reviews"].min(),
                max=df["number of reviews"].max(),
                tooltip={"placement": "top", "always_visible": False}
            ),

            html.Label("Rating", style={"font-weight": "bold"}),
            dcc.RangeSlider(
                id="rating",
                min=df["review rate number"].min(),
                max=df["review rate number"].max(),
                step=1,
                tooltip={"placement": "top", "always_visible": False}
            ),

            # filters for the comparing visualization
            html.Label("Filters for the third visualization", style={"font-weight": "bold"}),
            html.Hr(),
            html.Label("First variables"),
            dcc.Dropdown(
                id="first_vars",
                options=useful_vars,
                value=useful_vars[0]["value"]
            ),

            html.Label("Second variables"),
            dcc.Dropdown(
                id="second_vars",
                options=useful_vars,
                value=useful_vars[1]["value"]
            ),
        ],
    )


# Create the header and menu
def make_header_layout():
    return generate_header()


def make_menu_layout(df):
    return generate_control_card(df)
