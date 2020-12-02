#!/usr/bin/env python
# coding: utf-8

# get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
# import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, cast, Date
from datetime import date, datetime
from flask import Flask, jsonify

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

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

#create a route in the base page which shows all the available routes 
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

# create a precipitation route which returns a json list of all of the rain 
# amounts with their date as the index portion.
# rather than running a for loop, i use the "to-dict" function to create the dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():
    # connection = engine.connect()
    # session = Session(engine)
    with engine.connect() as connection:
        title_df = pd.read_sql("SELECT prcp, date FROM measurement", connection)
        prcp_dict_list = title_df.set_index('date').T.to_dict('records')
        prcp_dict = prcp_dict_list[0]
        # 
        return jsonify(prcp_dict)


#create a route which returns a dictionary of the stations
@app.route("/api/v1.0/stations")
def stations():    
    session = Session(engine)
    stations = session.query(Station.station, Station.station).distinct()
    return jsonify(dict(stations))
    session.close()

# return a dictionary of temps from the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    with engine.connect() as connection:
        most_active_df = pd.read_sql("SELECT tobs, date FROM measurement where station = 'USC00519281'", connection)
        active_dict_list = most_active_df.set_index('date').T.to_dict('records')
        # active_dict = active_dict_list[0]
        # 
        return jsonify(active_dict_list)

# have an inteeractive route which will return the temp's min, max, and avg from a given date
@app.route("/api/v1.0/<start>", methods = ['GET'])
def start_fx(start):
    session = Session(engine)
    start_convert = datetime.strptime(start, "%Y-%m-%d").date()
    # date = dt.date(start)
    start_list = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                          func.max(Measurement.tobs)).filter(Measurement.date>=start_convert).all()
    session.close()
    
    results_list = []
    for date, min, avg, max in start_list:
        start_dict = {}
        start_dict["StartDate"] = start_convert
        start_dict["TMIN"] = min
        start_dict["TAVG"] = avg
        start_dict["TMAX"] = max
        results_list.append(start_dict)
    return jsonify(results_list)

# have an inteeractive route which will return the temp's min, max, and avg for a given date range
@app.route("/api/v1.0/<start>/<end>", methods = ['GET'])
def start_end_fx(start, end):
    session = Session(engine)
    start_convert = datetime.strptime(start, "%Y-%m-%d").date()
    end_convert = datetime.strptime(start, "%Y-%m-%d").date()
    # date = dt.date(start)
    start_list = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                          func.max(Measurement.tobs)).filter(Measurement.date>=start_convert).filter(Measurement.date<=end_convert).all()
    session.close()
    
    results_list = []
    for date, min, avg, max in start_list:
        start_dict = {}
        start_dict["StartDate"] = start_convert
        start_dict["EndDate"] = end_convert
        start_dict["TMIN"] = min
        start_dict["TAVG"] = avg
        start_dict["TMAX"] = max
        results_list.append(start_dict)
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)