"""BikeShare Dash App

Dash-based visualization of Toronto BikeShare data from Q3 and Q4 of 2016.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import psycopg2
from dash.dependencies import Input, Output, State
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

import plotly
plotly.tools.set_credentials_file(username=PLOTLY_USER,
                                  api_key=PLOTLY_API)
from plotly import graph_objs as go

from matplotlib import colors as mpl_colors
from matplotlib import cm as mpl_cm
bwr_cmap = mpl_cm.get_cmap('bwr')


# Declare Dash app.
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css?family=Open+Sans:400,600']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config.suppress_callback_exceptions = True


# Create connection-load bike stations dataframe.
con = psycopg2.connect(database='bikes', user=POSTGRES_USER,
                       password=POSTGRES_PASSWORD,
                       host=POSTGRES_HOST, port=POSTGRES_PORT)

bike_stations = pd.read_sql("SELECT * FROM bike_stations;", con)


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
                           'OpenDataToronto/bikeshare/BikeShare/'
                           'webapp/legend.png'),
                      style={'width': '100%'}),
             className='row legend')
])


def query_bike_rides(timestamp):
    """Queries active bike rides from PostgreSQL table.

    Parameters
    ----------
    timestamp : datetime.datetime
        Time to query.

    Returns
    -------
    pandas.DataFrame
    """
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    sql_query = """SELECT * FROM bike_trips
    WHERE trip_start_time <= '{0}' AND trip_stop_time > '{0}';""".format(
        timestamp_str)
    return pd.read_sql(sql_query, con)


def get_rider_lines(ride_trajectories, item, n_riders, color):
    """Draw ride lines for trips with a certain number of riders, and riders
    of a certain type.

    Parameters
    ----------
    ride_trajectories : pandas.DataFrame
        Data frame containing all possible ride start and end stations, and
        the number of casual and member riders.
    item : 'N_casual', 'N_member' or 'N_both'
        Typer of rider to draw.
    n_riders : int > 0
        Which rider number to use.
    color : str
        Hex code for color.

    Returns
    -------
    plotly.graph_objs.Scattermapbox
    """
    wanted_riders = (ride_trajectories[item] == n_riders)
    n_wanted_riders = int(np.sum(wanted_riders))
    rider_subset = ride_trajectories.index[wanted_riders]
    # Following https://github.com/plotly/plotly.js/issues/2778, adding NaNs to
    # prevent connecting different trips together.
    lats = (np.vstack([ride_trajectories.loc[rider_subset, 'lat_from'].values,
                       ride_trajectories.loc[rider_subset, 'lat_to'].values,
                       np.nan * np.ones(n_wanted_riders)])
            .T.ravel())
    lons = (np.vstack([ride_trajectories.loc[rider_subset, 'lon_from'].values,
                       ride_trajectories.loc[rider_subset, 'lon_to'].values,
                       np.nan * np.ones(n_wanted_riders)])
            .T.ravel())
    return go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines',
        line=dict(
            color=color,
            width=np.minimum(0.25 * n_riders**2, 20),
        ),
        hoverinfo='none',
        name='Trips' + str(n_riders))


def make_ride_map(timestamp):
    """Make map of all active bikeshare rides at a given time using
    `plotly.graph_objs.Scattermapbox`.

    Parameters
    ----------
    timestamp : datetime.datetime
        Time to display.

    Returns
    -------
    plotly.graph_objs.Figure
    """
    current_rides = query_bike_rides(timestamp)
    data = []

    # Determine balance of arriving and department rides for stations.
    station_balance = pd.DataFrame(dict(
        from_station=current_rides.groupby('from_station_id')['trip_id'].count(),
        to_station=current_rides.groupby('to_station_id')['trip_id'].count()))
    station_balance.reset_index(inplace=True)
    station_balance.columns = ['station_id', 'N_departing', 'N_arriving']

    stations = (bike_stations.copy()
                .merge(station_balance, how='left',
                       left_on='station_id', right_on='station_id')
                .fillna(value=0.))

    stations['N_total'] = stations['N_departing'] + stations['N_arriving']
    stations['N_balance'] = (
        (stations['N_arriving'] - stations['N_departing']) /
        (2. * stations['N_total'])) + 0.5
    stations['N_balance'].fillna(0.5, inplace=True)

    if current_rides.shape[0]:
        # Determine all unique origin/destination pairs for rides, and count the
        # number of rides for each journey.
        ride_trajectories = (
            current_rides.groupby(
                ['from_station_id', 'to_station_id'])['user_type']
            .value_counts().unstack(fill_value=0).reset_index())
        ride_trajectories.rename(columns={'Member': 'N_member',
                                          'Casual': 'N_casual'}, inplace=True)
        if 'N_member' not in ride_trajectories.columns:
            ride_trajectories['N_member'] = (
                np.zeros(ride_trajectories.shape[0]))
        if 'N_casual' not in ride_trajectories.columns:
            ride_trajectories['N_casual'] = (
                np.zeros(ride_trajectories.shape[0]))
        # Separate ride trajectories into three mutually exclusive
        # categories - casual, member and both - setting N_casual and N_member
        # to zero if N_both > 0.
        both = ((ride_trajectories['N_casual'] > 0) &
                (ride_trajectories['N_member'] > 0))
        ride_trajectories['N_both'] = np.zeros(ride_trajectories.shape[0],
                                               dtype=int)
        ride_trajectories.loc[both, 'N_both'] = (
            ride_trajectories.loc[both, 'N_casual'] +
            ride_trajectories.loc[both, 'N_member'])
        ride_trajectories.loc[both, 'N_casual'] = 0
        ride_trajectories.loc[both, 'N_member'] = 0
        ride_trajectories = (
            ride_trajectories.merge(bike_stations[['lat', 'lon', 'station_id']],
                                    how='left', left_on='from_station_id',
                                    right_on='station_id')
            .rename(columns={'trip_id': 'N_rides', 'lat': 'lat_from',
                             'lon': 'lon_from'})
            .merge(bike_stations[['lat', 'lon', 'station_id']],
                   how='left', left_on='to_station_id', right_on='station_id')
            .rename(columns={'lat': 'lat_to', 'lon': 'lon_to'}))

        # https://plot.ly/python/reference/#scatter
        # I can't find a way to vary the thickness of this line except with
        # different Plotly traces, so plot trajectories with different numbers
        # of riders separately.
        for item, color in (('N_casual', '#ffa144'), ('N_member', '#64ce5f'),
                            ('N_both', '#fff24c')):
            n_riders_arr = np.sort(ride_trajectories[item].unique())
            if n_riders_arr[0] == 0:
                n_riders_arr = n_riders_arr[1:]
            data += [get_rider_lines(ride_trajectories, item, n_riders, color)
                     for n_riders in n_riders_arr]

    # Add stations.
    station_text = [
        "{0}<br>Bikes departing: {1}<br>Bikes arriving: {2}".format(
            name, int(dpt), int(arrv))
        for i, (name, dpt, arrv) in
        stations[['Name', 'N_departing', 'N_arriving']].iterrows()]

    data += [
        go.Scattermapbox(
            lat=stations['lat'].values,
            lon=stations['lon'].values,
            mode='markers',
            marker=dict(
                symbol='circle',
                opacity=1.0,
                size=np.maximum(5., 4 * (stations['N_total'].values)**0.6),
                color=[mpl_colors.rgb2hex(bwr_cmap(balance)[:3])
                       for balance in stations['N_balance'].values],
            ),
            text=station_text,
            name='',
        ),
    ]

    layout = go.Layout(
        autosize=True,
        height=600,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            bearing=0,
            center=dict(
                lat=43.6532,
                lon=-79.3932
            ),
            pitch=0,
            zoom=12,
            style='mapbox://styles/cczhu/cjounit2f1cwm2sl62e2jzjqs'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )

    return go.Figure(data=go.Data(data), layout=layout)


@app.callback(Output("map-graph", "figure"),
              [Input('submit-button', 'n_clicks')],
              [State('date-picker', 'date'),
               State('hour-slider', 'value'),
               State('min-slider', 'value')])
def do_the_map(n_clicks, date, hour, minute):
    return make_ride_map((datetime.datetime.strptime(date, '%Y-%m-%d') +
                          datetime.timedelta(hours=hour, minutes=minute)))


# Series of functions to handle the presets.
preset_date_picker_dict = {
    "D": datetime.datetime(2016, 9, 15),
    "wkdy": datetime.datetime(2016, 9, 15),
    "wknd": datetime.datetime(2016, 9, 10),
    "civic": datetime.datetime(2016, 8, 1),
    "nuit": datetime.datetime(2016, 10, 1),  
}

preset_hour_slider_dict = {
    "D": 17,
    "wkdy": 8,
    "wknd": 16,
    "civic": 15,
    "nuit": 3,
}

preset_min_slider_dict = {
    "D": 30,
    "wkdy": 40,
    "wknd": 30,
    "civic": 35,
    "nuit": 0,
}

@app.callback(Output('date-picker', 'date'),
              [Input('presets-dropdown', 'value')])
def preset_date_picker(dropvalue):
    return preset_date_picker_dict[dropvalue]


@app.callback(Output('hour-slider', 'value'),
              [Input('presets-dropdown', 'value')])
def preset_hour_slider(dropvalue):
    return preset_hour_slider_dict[dropvalue]


@app.callback(Output('min-slider', 'value'),
              [Input('presets-dropdown', 'value')])
def preset_min_slider(dropvalue):
    return preset_min_slider_dict[dropvalue]


if __name__ == '__main__':
    app.run_server(debug=True)
