import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)
session = Session(engine)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.datetime(2016, 8, 23)
    sel = [Measurement.date, 
        Measurement.prcp]
    prcp_data = session.query(*sel).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.name).all()
    station_data = list(np.ravel(station_names))

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.datetime(2016, 8, 23)
    station_data = session.query(Measurement.tobs).filter(Measurement.date > last_year).filter(Measurement.station == 'USC00519281').all()
    tobs_data = list(np.ravel(station_data))

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def begin(start = None):
    answer = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    answer = list(np.ravel(answer))
    
    return jsonify(answer)

@app.route("/api/v1.0/<start>/<end>")
def start_data(start = None, end = None):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    results = list(np.ravel(results))
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
