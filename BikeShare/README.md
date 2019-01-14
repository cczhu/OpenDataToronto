# Toronto Bike Share DashApp Visualization

[Data Munging ipynb](https://nbviewer.jupyter.org/github/cczhu/OpenDataToronto/blob/master/BikeShare/BikeShare%20DashApp%20Data%20Munging.ipynb)

This repo visualizes the [Q3 and Q4 bikeshare ride data](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#343faeaa-c920-57d6-6a75-969181b6cbde)
available from the Toronto open data catalogue.

The `bike_stations_15_11_2018.csv` file was created from cleaned data from [the
station information JSON feed](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#84045f23-7465-0892-8889-7b6f91049b29)
accessible from the Toronto open data catalogue.

# Requirements

## Jupyter Notebook

```bash
jupyter==1.0.0
numpy==1.15.1
pandas==0.23.4
requests==2.19.1
plotly==2.0.12
```

The notebook requires a number of requries a number of login credentials and
API keys to function; these must be stored in a `secrets.py` file containing
the following:

```Python
MAPBOX_TOKEN = 'YOUR_MAPBOX_TOKEN'
PLOTLY_USER = 'YOUR_PLOTLY_USERNAME'
PLOTLY_API = 'YOUR_PLOTLY_API_KEY'
POSTGRES_PASSWORD = 'YOUR_POSTGRES_PASSWORD'
```

In addition, you'll need to set the environmental variable
`BIKESHARE_FOLDER_PATH`, the path where you placed the
`2016_Bike_Share_Toronto_Ridership_Q3.xlsx` and
`2016_Bike_Share_Toronto_Ridership_Q4.xlsx` files.  On Bash, this can be done
with:

```bash
export BIKESHARE_FOLDER_PATH='<YOUR_FILE_PATH>'
```

## Web App

The dash-based web app is located inside the `webapp` folder.  The following
instructions describe how to deploy it on Amazon AWS.

#### 1. Generate Postgres tables

* Run the ``BikeShare DashApp Data Munging.ipynb`` notebook to completion.  Its
final section saves cleaned data tables into a local Postgres database.  Follow
the instructions within the section to install and set up Postgres on an
Ubuntu system.
* Once finished, check Postgres status:

```bash
sudo service postgresql status
```

* Sign in as user `<USERNAME>` and launch the interactive Postgres terminal

```bash
su <USERNAME>
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

### 2. Set up an AWS user

* Log in to AWS.
* If one doesn't already exist, [create an IAM
account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)
and attach it to a policy that gives it `AmazonRDSFullAccess` and
`AmazonEC2FullAccess` (or just `AdministratorAccess`).  Then, log in using the
IAM.

### 3. Create an EC2 instance
* Under the default VPC, create a new security group for the EC2 instance,
opening the ports needed (eg. 8050) to run the dash app and nginx server.
* Launch a t2.micro EC2 instance and associate it with the security group.
* Create an Elastic IP and associate it with your instance.

### 4. Create a production virtualenv with the required packages

* Create a virtualenv:

```bash
virtualenv --no-site-packages -p python3 <YOUR_VENV_PATH>
source <YOUR_VENV_PATH>/bin/activate
```

* Clone the webapp:

```bash
cd ~/
git clone https://github.com/cczhu/OpenDataToronto.git
```

* Install the Python package requirements:

```bash
cd OpenDataToronto/BikeShare/webapp
pip install -r requirements.txt
```

### 5. Create RDS Postgres database

* Follow [this tutorial](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html#CHAP_GettingStarted.Creating.PostgreSQL)
to create a Postgres database on AWS RDS with the following settings:
  * DB engine version: 9.6.11-R1.
  * DB instance class: t2.micro
  * DB instance identifier: bikeshareapp
  * DB username: postgres
  * VPC: whichever VPC your EC2 instance is located in.
  * Public accessibility: yes
  * DB name: bikes
  * Disable deletion protection
* If you have trouble with subnet groups, have a look at [this tutorial](
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.CreateDBSubnetGroup),
and:
  * Go to `Subnet groups` in the RDS.
  * Find the subnet group associated with your VPC (for the default VPC, it
should be `default`).
  * Add all available subnets in the VPC to the group.  If no subnets exist,
 create new subnets.  To generate default subnets, refer to [this tutorial](
 https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html#create-default-subnet).
* Once finished, test your endpoint:

```bash
psql --host=<YOUR_ENDPOINT> --port=<YOUR_PORT> --username=postgres --password --dbname=bikes
```

### 6. Upload local tables to RDS database

We'll dump our local Postgres table to a file, then upload that file to the RDS
following [this tutorial](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html).
The reason we're not directly writing from pandas to the remote Postgres
table is that it's [prohibitively slow](https://stackoverflow.com/q/30286775).

* Save the local `bikes` database as a .sql file:

```bash
pg_dump -Fc -v -h localhost -U postgres bikes > <PATH_TO_FILE>/bikes.dump
```
* Upload the dump to RDS:

```bash
pg_restore -v -h <YOUR_ENDPOINT> -U postgres -d bikes <PATH_TO_FILE>/bikes.dump
```

* Once finished, test the remote database:

```bash
psql --host=<YOUR_ENDPOINT> --port=<YOUR_PORT> --username=postgres --password --dbname=bikes
\dt
SELECT * FROM bike_stations LIMIT 10;
SELECT * FROM bike_trips LIMIT 10;
```

#### 7. Restrict RDS database to only connect with the EC2 instance

* Create a new security group that restricts access to only the EC2's security
group, and assign it to the RDS.  Also, deselect `public accessibility` in the
RDS instance settings.
* To check that `psycopg2` on the EC2 instance still has access to the RDS,
try running in IPython:

```python
import psycopg2
import pandas as pd

con = psycopg2.connect(database='bikes', user='postgres', password=<YOUR_PASSWORD>,
                       host=<YOUR_ENDPOINT>, port=<YOUR_PORT>)
sql_query = """
SELECT * FROM bike_trips
WHERE trip_start_time <= '2016-07-08 17:15:00' AND trip_stop_time > '2016-07-08 17:15:00';
"""

bikes_from_sql = pd.read_sql(sql_query, con)
bikes_from_sql.head(n=10)
```

### 8. Declare environmental variables

* The app obtain plotly, Mapbox, and Postgres connection API keys, usernames
and host information either by importing `secrets.py` file or, failing that,
reading in environmental variables.  To use a file, make sure `secrets.py` is
in your Python PATH and has the same format as the `secrets.py` for the
Jupyter Notebook (see above).  To use environmental variables, set them eg.
with `export PLOTLY_USER=<YOUR_USERNAME>`.  For either, you'll need to set:
  * `PLOTLY_USER`: plotly account username
  * `PLOTLY_API`: plotly account API key
  * `POSTGRES_USER`: Postgres database username
  * `POSTGRES_PASSWORD`: Postgres database password
  * `POSTGRES_HOST`: Postgres hostname (defaults to 'localhost' if not set)
  * `POSTGRES_PORT`: Postgres port number (defaults to '5432' if not set)
  * `MAPBOX_TOKEN`: Mapbox API access token

### 9. Check the app

* Once all variables are set, check that the webapp works.  First, go to
`OpenDataToronto/BikeShare/` and modify the last two lines in `run_webapp.py`
to resemble:

```python
# app.run_server(debug=True)
app.run_server(host='0.0.0.0', debug=True)
```

* Then, run:

```bash
python run_webapp.py
```

* Use your web browser to check the EC2 public IP with port 8050 for the right
output.

### 10. Install the gunicorn webserver and run the app

* Install and launch nginx:

```bash
sudo apt-get install nginx
sudo /etc/init.d/nginx start
```

* Modify nginx to properly point to the app:

```bash
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/application
sudo ln -s /etc/nginx/sites-available/application /etc/nginx/sites-enabled/application
```

* Modify the application file to look like the `server` block below:

```bash
sudo vim /etc/nginx/sites-enabled/application
```

```
server {
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /assets {
        alias <YOUR_HOME>/OpenDataToronto/BikeShare/webapp/assets/;
    }
}
```

* Restart nginx:

```bash
sudo /etc/init.d/nginx restart
```

* Install gunicorn:

```bash
pip install gunicorn
```

* Add the BikeShare folder to the virtualenv path:

```bash
echo '/home/ubuntu/OpenDataToronto/BikeShare/' > /home/ubuntu/pythonenv/biketracker/lib/python3.5/site-packages/dashapp.pth
```

* Start gunicorn:

```bash
gunicorn webapp:app.server -D
```

* To kill gunicorn:

```bash
pkill gunicorn
```

### 11. Shut the app down

* Remember that when shutting the app down, you need to remove:
  * The EC2 instance
  * The Elastic IP
  * The RDS instance
