import json
from flask import Flask, request
import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# routes
@app.route("/internships/")
def get_internships():
    """
    Endpoint for getting all internships
    """