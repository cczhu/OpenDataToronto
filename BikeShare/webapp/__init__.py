"""BikeShare Dash App

Dash-based visualization of Toronto BikeShare data from Q3 and Q4 of 2016.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import psycopg2
import datetime

# Try to obtain login credentials and API keys by importing `secrets`; if this
# doesn't work, try obtaining them from environmental variables.
try:
    import secrets
except ImportError:
    import os
    PLOTLY_USER = os.environ.get('PLOTLY_USER')
    PLOTLY_API = os.environ.get('PLOTLY_API')
    MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost'
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
else:
    PLOTLY_USER = secrets.PLOTLY_USER
    PLOTLY_API = secrets.PLOTLY_API
    MAPBOX_TOKEN = secrets.MAPBOX_TOKEN
    try:
        POSTGRES_USER = secrets.POSTGRES_USER
    except AttributeError:
        POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = secrets.POSTGRES_PASSWORD
    try:
        POSTGRES_HOST = secrets.POSTGRES_HOST
        POSTGRES_PORT = secrets.POSTGRES_PORT
    except AttributeError:
        POSTGRES_HOST = 'localhost'
        POSTGRES_PORT = '5432'


# Declare Dash app.
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css?family=Open+Sans:400,600']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config.suppress_callback_exceptions = True


# Create connection-load bike stations dataframe.
db_con = psycopg2.connect(database='bikes', user=POSTGRES_USER,
                          password=POSTGRES_PASSWORD,
                          host=POSTGRES_HOST, port=POSTGRES_PORT)

bike_stations = pd.read_sql("SELECT * FROM bike_stations;", db_con)


mdtext = """# BikeTracker
## Visualizing Toronto BikeShare Rides From Q3 - Q4 2016

The Toronto [Q3 and Q4 bikeshare ridedata](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#343faeaa-c920-57d6-6a75-969181b6cbde)
captures (anonymized) trips taken with the Toronto bikeshare system between
July 1st and December 31st, 2016.  The data includes the trip start and end
times, duration, and origin and destination stations.  With this information,
we can map all active rides at a given point in time, and determine which
stations are the most popular points of origin and destination.

To plot different days and times of day, **use the sliders and date selector**
on the right, then **press plot**.  For some interesting times of year,
**select one of the presets**.  Hover the cursor over any bike station to see
the number of departing and arriving bike rides.
"""

app.layout = html.Div([
    html.Div([dcc.Markdown(children=mdtext)],
             className="description_div",
             style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div("Presets", className='control_names'),
        dcc.Dropdown(
            id="presets-dropdown",
            options=[
                {"label": "Typical weekday morning", "value": "wkdy"},
                {"label": "Typical weekend afternoon", "value": "wknd"},
                {"label": "Ontario Civic Holiday afternoon", "value": "civic"},
                {"label": "Nuit Blanche", "value": "nuit"},
            ],
            value="D",
            clearable=False,
        ),
        html.Div("Date", className='control_names'),
        dcc.DatePickerSingle(id='date-picker',
                             date=datetime.datetime(2016, 9, 15),
                             min_date_allowed=datetime.datetime(2016, 7, 1),
                             max_date_allowed=datetime.datetime(2016, 12, 31)),
        html.Div("Hour", className='control_names'),
        dcc.Slider(id='hour-slider', min=0, max=23, value=17,
                   marks={i: str(i) for i in range(0, 24, 2)}),
        html.Div("Minute", className='control_names'),
        dcc.Slider(id='min-slider', min=0, max=59, value=30,
                   marks={i: str(i) for i in range(0, 60, 5)}),
        html.Div(
            html.Button(id='submit-button', children='PLOT',
                        style={"margin-top": "20px"}),
            className="two columns",
            style={"float": "right", "padding": "30px 70px 20px 0px"},
        )],
        style={'width': '45%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='map-graph'),
             style={"padding-top": "20px"}),
    html.Div(html.Img(src=('https://raw.githubusercontent.com/cczhu/'
                           'OpenDataToronto/master/BikeShare/'
                           'webapp/legend.png'),
                      style={'width': '100%'}),
             className='row legend')
], className="primeDiv")

# Circular import, so needs to be defined after `app` is.
from . import functions
