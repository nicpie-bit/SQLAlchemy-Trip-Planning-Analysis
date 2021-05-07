import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resoucres/hawaii.sqlite", connect_args={'check_same_thread': False},echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
    prcp_data = []
    for date, prcp in precip_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station():
    stat_results = session.query(Station.station, Station.name).all()
    stat_data = pd.read_sql(stat_results.statement, stat_results.session.bind)
    return jsonify(stat_results)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_earlier_date).filter(Measurement.station == most_active_stid).order_by(Measurement.tobs).all()
    return jsonify(tobs_results) 

@app.route("/api/v1.0/<start>")
def start_date(start):
    temp1_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(temp1_results)

@app.route("/api/v1.0/<start>/<end>")
def startend_date(start,end):
    temp2_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp2_results)

if __name__ == "__main__":
    app.run(debug=True)