#!/usr/bin/env python
# coding: utf-8

# get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()

# create a base
Base = automap_base()


# reflect an existing database into a new model
Base.prepare(engine, reflect=True)
# reflect the tables
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station


# # Include inspector
inspector = inspect(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# # Exploratory Climate Analysis

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    title_df = pd.read_sql("SELECT prcp, max(date) as oldest_date FROM measurement", connection)
    return jsonify(title_df)

    # Calculate the date 1 year ago from the last data point in the database
    from sqlalchemy import cast, Date
    from datetime import date
    # this is some code i'm trying to get work without manually entering the date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # latest_date = session.query(cast(Measurement.date, Date)).order_by(Measurement.date.desc()).first() 
    date_1_year = date.fromisoformat(latest_date)
    date_1_yr_ago = date_1_year - dt.timedelta(days=365)
    date_1_yr_ago
    # latest_date[0].split('-')

    # Perform a query to retrieve the date and precipitation scores
    prcp_df = pd.read_sql("SELECT date, prcp FROM measurement", connection)


    # Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df.set_index('date')

    # Sort the dataframe by date
    prcp_df.sort_values(by=['date'])
    prcp_df

    # Use Pandas Plotting with Matplotlib to plot the data
    prcp_df.plot()

    # Use Pandas to calcualte the summary statistics for the precipitation data
    summary_table = prcp_df.agg({"prcp":["mean","median","var","std","sem"]})
    summary_table

    # Design a query to show how many stations are available in this dataset?
    title_df = pd.read_sql("SELECT DISTINCT station FROM station", connection)
    len(title_df)


    # What are the most active stations? (i.e. what stations have the most rows)?
    # List the stations and the counts in descending order.
    sel = [Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs]
    measurement = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # list the number of stations for an internal loop

    # loop through the full measurement set to count the number of stations

    # Using the station id from the previous query, calculate the lowest temperature recorded, 
    # highest temperature recorded, and average temperature of the most active station?
    temps = session.query(Measurement.station, func.min(Measurement.tobs),                            func.max(Measurement.tobs), func.round(func.avg(Measurement.tobs),2)).                            filter(Measurement.station=='USC00519281').all()
    temps

    # Choose the station with the highest number of temperature observations.
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    high_stn = session.query(Measurement.tobs).filter(Measurement.station=='USC00519281', Measurement.date >= prev_year).all()
    high_stn = np.ravel(high_stn)
    
    return jsonify(high_stn)


# # Flask: see VS Code for it
if __name__ == '__main__':
    app.run(debug=True)