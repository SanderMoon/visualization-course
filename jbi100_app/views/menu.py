from dash import dcc, html
from ..config import color_list1, color_list2
import numpy as np
from dash import html
from dash.dependencies import Input, Output
from jbi100_app.main import app
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

            html.Br(),

            #General variable filters
            html.Hr(),
            html.Label("Host identity confirmed"),
            dcc.RadioItems(["Unconfirmed", "Verified"], style={'padding': 10, 'flex': 1}),

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
                id = "map_var",
                options = useful_int_vars,
                value = "price"
            ),
            

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


# Create the header and menu
def make_header_layout():
    return generate_header()


def make_menu_layout(df):
    return generate_control_card(df)
