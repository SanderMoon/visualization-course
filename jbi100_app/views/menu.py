from dash import dcc, html
from ..config import color_list1, color_list2
import numpy as np
from dash import html
from dash.dependencies import Input, Output
from jbi100_app.main import app

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
               {"label": "Review rate number", "value": "Review rate number"},
               {"label": "Availability 365", "value": "availability 365"}]

value_index_map = {opt['value']: index for index, opt in enumerate(useful_vars)}


def generate_control_card(df):
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            # html.Label("Color scatterplot 1"),
            # dcc.Dropdown(
            #     id="select-color-scatter-1",
            #     options=[{"label": i, "value": i} for i in color_list1],
            #     value=color_list1[0],
            # ),
            # html.Br(),
            # html.Label("Color scatterplot 2"),
            # dcc.Dropdown(
            #     id="select-color-scatter-2",
            #     options=[{"label": i, "value": i} for i in color_list2],
            #     value=color_list2[0],
            # ),
            # html.Br(),

            # Filter for neighborhood groups on map
            html.Label("Filters for the map visualization"),
            html.Hr(),
            html.Label("Neighbourhood group"),
            dcc.Dropdown(
                id="neighbourhood_group",
                options=generate_neighbourhood_options(df),
                value=generate_neighbourhood_options(df)[0]
            ),

            # Filter for which variable to show on the choropleth
            html.Br(),
            html.Label("Choropleth variable"),
            dcc.Dropdown(
                id="choropleth_var",
                options=["Price", "Service fee", "Rating"],
                value=0,
            ),

            html.Br(),

            # filters for the comparing visualization
            html.Label("Filters for the third visualization: "),
            html.Hr(),
            html.Label("First variables"),
            dcc.Dropdown(
                id="first_vars",
                options=useful_vars
            ),

            html.Label("Second variables"),
            dcc.Dropdown(
                id="second_vars",
                options=useful_vars
            ),
            # html.Button(
            #     id="submit-button-state",
            #     children="Compare",
            #     n_clicks=0
            # )

        ],
    )


# Create the chained dropdowns
@app.callback(
    Output("second_vars", "options"),
    Input("first_vars", "value"))
def update_options_var2(value):
    useful_vars.pop(value_index_map[value])
    return useful_vars


# Create the header and menu
def make_header_layout():
    return generate_header()


def make_menu_layout(df):
    return generate_control_card(df)
