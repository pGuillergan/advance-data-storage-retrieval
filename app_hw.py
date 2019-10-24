import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
# function usage example
# print(calc_temps('2012-02-28', '2012-03-05'))


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""

    return (
        f"------------------------------<br/>"
        f"Available Routes:<br/>"
        f"------------------------------<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"------------------------------<br/>"
        f"For the following routes please use this date format:<br/>"
        f"YYYY-MM-DD<br/>"
        f"ex: http://127.0.0.1:5000/api/v1.0/2012-02-28/2012-03-05<br/>"
        f"------------------------------<br/>"
        f"/api/v1.0/{{start date}}<br/>"
        f"/api/v1.0/{{start date}}/{{end date}}<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    latest_date, = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date_dt = dt.datetime.strptime(latest_date, '%Y-%m-%d')

    from dateutil.relativedelta import relativedelta

    def yearsago(years, from_date=None):
        if from_date is None:
            from_date = datetime.now()
        return from_date - relativedelta(years=years)

    year_ago_dt = yearsago(1, from_date=latest_date_dt)
    year_ago = year_ago_dt.strftime('%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    year_ago_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()
    YA_dict = dict(year_ago_query)
    
    return jsonify(YA_dict) 

@app.route("/api/v1.0/stations")
def stations():

    stat = session.query(Station).all()
    stations = stat.copy()
    station_list = []
    for i in stations:
        temp_dict = i.__dict__
        del temp_dict['_sa_instance_state']
        station_list.append(temp_dict)
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    latest_date, = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date_dt = dt.datetime.strptime(latest_date, '%Y-%m-%d')

    from dateutil.relativedelta import relativedelta

    def yearsago(years, from_date=None):
        if from_date is None:
            from_date = datetime.now()
        return from_date - relativedelta(years=years)

    year_ago_dt = yearsago(1, from_date=latest_date_dt)
    year_ago = year_ago_dt.strftime('%Y-%m-%d')

    # Perform a query to retrieve the temperature data
    year_ago_query = session.query(func.min(Measurement.tobs)\
                             ,func.max(Measurement.tobs)\
                             ,func.avg(Measurement.tobs))\
                            .filter(Measurement.date > year_ago).all()
    
    temp_dict = { 'Min Temperature:': year_ago_query[0][0],
            'Max Temperature:': year_ago_query[0][1],
            'Avg Temperature:': year_ago_query[0][2]}
            
    return jsonify(temp_dict)


@app.route("/api/v1.0/<date1>")
def fromdate(date1):

    latest_date, = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    temps = calc_temps(date1, latest_date)
    temp_dict = {'Min Temp':temps[0][0], 'Avg Temp':temps[0][1], 'Max Temp':temps[0][2]}

    return jsonify(temp_dict)

@app.route("/api/v1.0/<date1>/<date2>")
def fromtodate(date1, date2):

    temps = calc_temps(date1, date2)
    temp_dict = {'Min Temp':temps[0][0], 'Avg Temp':temps[0][1], 'Max Temp':temps[0][2]}

    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   