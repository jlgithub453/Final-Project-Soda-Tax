import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# db = SQLAlchemy(app)
#
# # DATABASE_URL will contain the database connection string:
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
# #   # Connects to the database using the app config
# # db = SQLAlchemy(app)
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)
#
# # Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    # stmt = db.session.query(Samples).statement
    df = pd.read_csv('app_data.csv')
    used = set()
    store_name=list(df['store_code_uc'])
    store_unique_name=[x for x in store_name if x not in used and (used.add(x) or True)]
    # Return a list of the column names (sample names)
    return jsonify(store_unique_name)


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    # """Return the MetaData for a given sample."""
    # sel = [
    #     Samples_Metadata.sample,
    #     Samples_Metadata.ETHNICITY,
    #     Samples_Metadata.GENDER,
    #     Samples_Metadata.AGE,
    #     Samples_Metadata.LOCATION,
    #     Samples_Metadata.BBTYPE,
    #     Samples_Metadata.WFREQ,
    # ]
    #
    # results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    #for result in results:

    df = pd.read_csv('app_data.csv')
    print(df['store_code_uc'])
    print(type(sample))

    status= df.loc[df['store_code_uc'] == int(sample), ['region']]
    used = set()
    status_list=list(status['region'])
    result=[x for x in status_list if x not in used and (used.add(x) or True)]
    sample_metadata["tax status"] = result[0]


    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):

    df = pd.read_csv('app_data.csv')

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df['store_code_uc'] == int(sample), ['year_week','y_counterfactual','y_predict','week_sales']]
    # Format the data to send as json
    data = {
        "year_week": sample_data.year_week.tolist(),
        "y_counterfactual": sample_data.y_counterfactual.tolist(),
        "y_predict": sample_data.y_predict.tolist(),
        "week_sales": sample_data.week_sales.tolist()
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
