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

### 10 Jan. 2019

* [Downloaded Docker for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/),
and made sure it's working.  To give [non-root users access](
https://docs.docker.com/install/linux/linux-postinstall/), do:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

* Decided not to use Docker, however.  While it's definitely possible to connect
an [app container instance to an Nginx one](https://sladkovm.github.io/webdev/2017/10/16/Deploying-Plotly-Dash-in-a-Docker-Container-on-Digitital-Ocean.html),
connecting these to an RDS server [is complicated](https://stackoverflow.com/questions/32893876/accessing-rds-from-within-a-docker-container-not-getting-through-security-group).

### 12 Jan 2019

* Successfully deployed a small app following [this tutorial](
https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80),
but elected against using EBS since there's no way to specify the EC2 resources
to be used (since it's elastic).

### 13 Jan 2019

* Deployed app on AWS.