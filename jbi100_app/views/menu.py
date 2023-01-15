from dash import dcc, html
from ..config import color_list1, color_list2
import numpy as np

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

            # filters for the splom visualization
            html.Label("Filters for the Splom visualization: "),
            html.Hr(),
            html.Label("First variables"),
            dcc.Dropdown(
                id="first_vars",
                options=[{

                }],
                multi=True,
                value=0
            ),

            html.Label("Second variables"),
            dcc.Dropdown(
                id="second_vars",
                options=[{
                    # same variables
                }],
                multi=True,
                value=0
            ),


        ],
    )


def make_header_layout():
    return generate_header()


def make_menu_layout(df):
    return generate_control_card(df)
