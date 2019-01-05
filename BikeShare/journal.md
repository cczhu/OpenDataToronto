# BikeShare Dash App Design Journal

## Journal

### 15 Nov. 2018

* Added folder to Git repo
* Preliminary attempt at data cleaning, including matching 2016 station names
with current ones

### 27 Nov. 2018

* Finished munging, and created prototype visualization.

### 25 Dec. 2018

* Deployed local Postgres table.

### 27 Dec. 2018

* Created self-contained webapp under `app.py`, and connected map inputs to
sliders.

### 30 Dec. 2018

* Fixed a few minor bugs with webapp.

### 31 Dec. 2018

* Horizontally stack components following [this
example](https://community.plot.ly/t/horizontally-stack-components/10806/2).
* Created dropdown menu and connected its output to sliders.
* Added [local CSS file](https://dash.plot.ly/external-resources) under assets.
* [Remove "Undo" workaround](https://stackoverflow.com/questions/45137459/how-to-remove-the-undo-button-in-plotly-dash-after-a-dropdown-update)
* Decided not to [incorporate matplotlib plots](https://github.com/4QuantOSS/DashIntro/blob/master/notebooks/Tutorial.ipynb)
into the app to create the legend.  The legend is static, so it's unnecessary.

### 1 Jan. 2019

* Added matplotlib script to generate legend figure, and added legend to app.

## Deployment Notes

### Create a Production Virtualenv
* Create a virtualenv:

```bash
virtualenv --no-site-packages -p python3 ~/pythonenv/bikeshare/
```

* Install the Python package requirements:

```bash
pip install numpy==1.15.1 pandas==0.23.4 tables==3.4.4 SQLAlchemy==1.2.11 plotly==3.4.1 psycopg2==2.7.5 matplotlib==3.0.0 dash==0.34.0 dash-html-components==0.13.4 dash-core-components==0.42.0
```

* Test that the web app works.

```bash
export PYTHONPATH='<PATH TO YOUR SECRETS>'
python app.py
```

### Check PostgreSQL Database

* The ``BikeShare DashApp Data Munging.ipynb`` notebook cleans raw data, and
contains a cell which saves the cleaned data as a Postgres table.  Uncomment
this cell and run the entire notebook.

* Check Postgres status:

```bash
sudo service postgresql status
```

* Sign in as as user `postgres` and lanch interactive Postgres terminal

```bash
su postgres
psql
```

* Connect the `bikes` database, and check that both `bike_stations` and
`bike_trips` are valid

```bash
\c bikes
```

```sql
SELECT * FROM bike_stations LIMIT 10;
```

```sql
SELECT * FROM bike_trips LIMIT 10;
```

### AWS Setup

* Log in to AWS.  If one doesn't already exist, [create an IAM
account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)
and attach it to a policy that gives it `AmazonRDSFullAccess` and `AmazonEC2FullAccess`.
Then, log in using the IAM.
