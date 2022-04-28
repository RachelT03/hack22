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
    Endpoint for getting all internships with general info
    """
    return

@app.route("/internships/<int:int_id>")
def get_specific_internship(int_id):
    """"
    Gets a specific internship with more specific info
    """

    return

@app.route("/internships/" , methods = ["POST"])
def create_internship():
    """
    Creates an internship
    """

    return

@app.route("/internships/<int: int_id>", methods = ["DELETE"])
def delete_internship(int_id):
    """
    Deletes a specific internship
    """

    return

@app.route("/internships/<int: int_id>" , methods = ["POST"])
def edit_internship():
    """
    Edits a specific internship
    """

    return


@app.route("/internship/<int: int_id>/subtask/" , methods = ["POST"])
def create_subtask(int_id):
    """
    Creates a subtask
    """
    return


@app.route("/internship/<int: int_id>/subtask/<int:subtask>" , methods = ["POST"])
def edit_subtask():
    """
    Editing a subtask
    """
    return

@app.route("/user/")
def get_users():
    """
    Endpoint for getting all users
    """
    return


@app.route("/user/" , methods = ["POST"])
def create_user():
    """
    Ednpoint for Creating an user
    """
    return

@app.route("/user/<int:user_id>" , methods = ["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting
     a specific user
    """
    return