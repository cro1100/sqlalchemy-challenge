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


if __name__ == '__main__':
    app.run(debug=True)