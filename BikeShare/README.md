#Toronto Bike Share DashApp Visualization

This repo visualizes the [Q3 and Q4 bikeshare ride data](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#343faeaa-c920-57d6-6a75-969181b6cbde)
available from the Toronto open data catalogue.

The `bike_stations_15_11_2018.csv` file was created from cleaned data from [the
station information JSON feed](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#84045f23-7465-0892-8889-7b6f91049b29)
accessible from the Toronto open data catalogue.

#Requirements

Jupyter Notebook:

jupyter==1.0.0<br>
numpy==1.15.1<br>
pandas==0.23.4<br>
requests==2.19.1<br>

Dash App:

Mapbox requries a public API key, which must be stored in a ``secrets.py`` file
containing the following:

```Python
# Mapbox API key.
MAPBOX_TOKEN = '<YOUR_API_TOKEN'>
```

To obtain a token, go to [your Mapbox settings](https://www.mapbox.com/account/).
``secrets.py`` must be in your Python PATH.

In addition, for both the notebook and dashboard, you'll need to set the
environmental variable `BIKESHARE_FOLDER_PATH`, the path where you placed the
`2016_Bike_Share_Toronto_Ridership_Q3.xlsx` and `2016_Bike_Share_Toronto_Ridership_Q4.xlsx`
files.  On Bash, this can be done with:

```
export BIKESHARE_FOLDER_PATH='<YOUR_FILE_PATH>'
```
 