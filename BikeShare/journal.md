# BikeShare Dash App Design Journal

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

# App Deployment Notes

### AWS Setup

* Log in to AWS.  If one doesn't already exist, [create an IAM
account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)
and attach it to a policy that gives it `AmazonRDSFullAccess` and `AmazonEC2FullAccess`.
Then, log in using the IAM.
* 

### Export PostgreSQL Database

Check Postgres status:

```bash
sudo service postgresql status
```

Sign in as as user `postgres` and lanch interactive Postgres terminal

```bash
su postgres
psql
```

```bash
\c bikes
```