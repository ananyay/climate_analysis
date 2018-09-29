# Python SQL toolkit and Object Relational Mapper
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# view the classes
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)


# create an app (class instance of Flask)
app = Flask(__name__)

# Flask routes
@app.route("/")
def Welcome():
    return (
        f"Welcome to our Home Page<br/>"
        f"Here are the list of available API's:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #trip_start_date = "2018,1,1"
    prev_year_start = dt.date(2018, 1, 1) - dt.timedelta(days=365)
    prcp_res = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= prev_year_start ).group_by(Measurement.date).all()
    prcp_dict = {}
    for res in prcp_res:        
        prcp_dict[res.date] = res.prcp
    return jsonify(prcp_dict)
    

@app.route("/api/v1.0/stations")
def stations():
    st_list = session.query(Station.station).all()
    all_stations= list(np.ravel(st_list))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    #trip_start_date = "2018,1,1"
    prev_year_start = dt.date(2018, 1, 1) - dt.timedelta(days=365)
    tobs_list = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year_start ).all()
    all_tobs = list(np.ravel(tobs_list))
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def dynamic_tlist(start):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def dynamic_start_end_tlist(start,end):
    print(start, end)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)




if __name__ == "__main__":
    app.run(debug=True)

