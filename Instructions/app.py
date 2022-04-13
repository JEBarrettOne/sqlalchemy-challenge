# Import packages
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# ---------------------------------------------------
# Database Setup

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
print(Station)

# ---------------------------------------------------
# Flask Setup
app = Flask(__name__)

# ---------------------------------------------------
# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Close session
    session.close()

    # Convert list of tuples into dictionary
    bydate = dict(results)
    print(bydate)

    return jsonify(bydate)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations = session.query(Station.station, Station.name).all()
    
    station_info = [(row[0], row[1]) for row in stations]
    
    return jsonify(station_info)

@app.route("/api/v1.0/<tobs>")
def tobs():

    session = Session(engine)

    activity = session.query(Measurement.station, func.count(Measurement.station)).order_by(func.count(Measurement.station)).all()

    leader = activity[0][0]

    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == leader).all()
    
    yeardata = [(row[0], row[1]) for row in data]

    return jsonify(yeardata)

@app.route("/api/v1.0/<start>")
def time_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query data past given date
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start).\
        with_entities(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()

    # Close session
    session.close()

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def time_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query data past start date and before end date
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).\
        with_entities(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()

    # Close session
    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

