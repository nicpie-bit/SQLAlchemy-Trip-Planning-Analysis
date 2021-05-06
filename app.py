import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///../Resoucres/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create our session from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

#12 month earlier
year_earlier_date = '2016-08-23'

#Most active station
most_active_stid = 'USC00519281'

#Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Lets look into the precipitation data."""
    #Query last 12 months prcp data
    precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_earlier_date).group_by(Measurement.date).all()
    prcp_dict = []
    for date, prcp in precip_results:
        prcp_data = {}
        prcp_data["date"] = date
        prcp_data["prcp"] = prcp
        prcp_dict.append(prcp_data)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station():
    stat_results = session.query(Station.station, Station.name).all()
    return jsonify(stat_results)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_earlier_date).filter(Measurement.station == most_active_stid).order_by(Measurement.tobs).all()
    tobs_dict = []
    for date, tobs in tobs_results:
        tobs_data = {}
        tobs_data["date"] = date
        tobs_data["tobs"] = tobs
        tobs_dict.append(tobs_data)
    return jsonify(tobs_dict) 

if __name__ == "__main__":
    app.run(debug=True)