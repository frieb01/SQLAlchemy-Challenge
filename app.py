import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').filter(Measurement.prcp > 0).all()

    session.close()

    # Convert list of tuples into normal list
    dates = []
    precip = []
    for date, prcp in results:
        dates.append(date)
        precip.append(prcp)
    
    all_prcp_dict = dict(zip(dates, precip))
        
    return jsonify(all_prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >='2016-08-23').all()

    session.close()
    
    all_tobs = list(np.ravel(results))
      
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>", methods=['GET'])
def temps(start):
    
    session = Session(engine)

    min_results = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    avg_results = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    max_results = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    summary_dict = {"Minimum Temp":min_results,
                   "Average Temp":avg_results,
                   "Maximum Temp":max_results}
    
    return jsonify(summary_dict)

@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def temps_two(start,end):
    
    session = Session(engine)

    min_results = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg_results = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    max_results = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    summary_dict = {"Minimum Temp":min_results,
                   "Average Temp":avg_results,
                   "Maximum Temp":max_results}
    
    return jsonify(summary_dict)

if __name__ == '__main__':
    app.run(debug=True)