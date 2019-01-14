import numpy as np
import pandas as pd
import datetime

from dash.dependencies import Input, Output, State

from . import app
from . import bike_stations
from . import db_con as con
from . import PLOTLY_USER, PLOTLY_API, MAPBOX_TOKEN

import plotly
plotly.tools.set_credentials_file(username=PLOTLY_USER,
                                  api_key=PLOTLY_API)
from plotly import graph_objs as go

from matplotlib import colors as mpl_colors
from matplotlib import cm as mpl_cm
bwr_cmap = mpl_cm.get_cmap('bwr')


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
        # Determine all unique origin/destination pairs for rides, and count
        # the number of rides for each journey.
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
    "nuit": datetime.datetime(2016, 10, 2),
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
