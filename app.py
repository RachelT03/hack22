from db import db
from db import User
from db import Internship
from db import Task
from flask import Flask, request
import json

import os
app = Flask(__name__)
db_filename = "db_file.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response format
def success_response(data, code = 200):
    return json.dumps(data), code

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code

# routes
@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users and general information of their internships
    """
    users = [u.serialize() for u in User.query.all()]
    return success_response({"users": users})

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Ednpoint for creating a user
    """
    body = json.loads(request.data)
    if body.get("name") is None:
        return failure_response("user can't be created", 400)
    new_user = User(
        name = body.get("name")
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/", methods = ["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a specific user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


@app.route("/api/<int:user_id>/internships/")
def get_user_internships(user_id):
    """
    Endpoint for getting general information of all internships for a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    return success_response(user.simple_serialize())

@app.route("/api/<int:user_id>/internships/<int:internship_id>/")
def get_specific_internship(user_id, internship_id):
    """"
    Endpoint for getting a specific internship with detailed information for a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    return success_response(internship.serialize())

@app.route("/api/internships/<int:user_id>/", methods = ["POST"])
def create_internship(user_id):
    """
    Endpoint for creating an internship for a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    body = json.loads(request.data)
    if body.get("company") is None or body.get("status") is None:
        return failure_response("please include necessary information to create internship", 400)
    company = body.get("company")
    status = body.get("status")
    new_internship = Internship(
        company = company, 
        application_status = status,
        time_since_application = 2,
        user_id = user_id
        )
    user.internships.append(new_internship)
    db.session.add(new_internship)
    db.session.commit()
    return success_response(new_internship.serialize(), 201)

@app.route("/api/<int:user_id>/internships/<int:internship_id>/", methods = ["DELETE"])
def delete_internship(user_id, internship_id):
    """
    Endpoint for deleting an internship for a user
    """
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("user not found", 404)

    internship = Internship.query.filter_by(id=internship_id).first()
    
    if internship is None:
        return failure_response("internship not found", 404)

    user.internships.remove(internship)
    db.session.delete(internship)
    db.session.commit()
    return success_response(internship.serialize()),201

@app.route("/api/<int:user_id>/internships/<int:internship_id>/", methods = ["POST"])
def edit_internship(user_id, internship_id):
    """
    Endpoint for editing a specific internship
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    body = json.loads(request.data)
    status = body.get("status")
    if status is not None:
        internship.application_status = status
    db.session.commit()
    return success_response(internship.serialize(), 201)

# @app.route("/api/<int:user_id>/internship/<int:internship_id>/tasks/")
# def get_tasks(user_id, internship_id):
#     """
#     Endpoint for getting all tasks for a user's internship
#     """
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return failure_response("user not found", 404)
#     internship = user.internship[internship_id]
#     if internship is None:
#         return failure_response("internship not found", 404)
#     tasks = internship.task
#     return success_response(tasks.serialize(), 201)

# @app.route("/api/<int:user_id>/internship/<int:internship_id>/tasks/<int:task_id>/")
# def get_tasks(user_id, internship_id, task_id):
#     """
#     Endpoint for getting a specific task for a user's internship
#     """
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return failure_response("user not found", 404)
#     internship = user.internship[internship_id]
#     if internship is None:
#         return failure_response("internship not found", 404)
#     tasks = internship.task[task_id]
#     if tasks is None:
#         return failure_response("task not found", 404)
#     return success_response(tasks.serialize(), 201)

# @app.route("/api/<int:user_id>/internship/<int:internship_id>/tasks/", methods = ["POST"])
# def create_task(user_id, internship_id):
#     """
#     Endpoint for creating a task for a user's internship
#     """
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return failure_response("user not found", 404)
#     internship = user.internship[internship_id]
#     if internship is None:
#         return failure_response("internship not found", 404)
#     body = json.loads(request.data)
#     completed = body.get("completed")
#     name = body.get("task name")
#     new_task = Task(
#         task_name = name,
#         completed = completed,
#         task_id=task_id
#     )
#     internship.task.append(new_task)
#     db.session.add(new_task)
#     db.session.commit()
#     return success_response(new_task.serialize(), 201)


# @app.route("/api/<int:user_id>/internship/<int:internship_id>/tasks/<int:task_id>/", methods = ["POST"])
# def edit_task(user_id, internship_id, task_id):
#     """
#     Endpoint for editing a task for a user's internship
#     """
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return failure_response("user not found", 404)
#     internship = user.internship[internship_id]
#     if internship is None:
#         return failure_response("internship not found", 404)
#     tasks = internship.task[task_id]
#     if tasks is None:
#         return failure_response("task not found", 404)
#     body = json.loads(request.data)
#     completed = body.get("completed")
#     name = body.get("task name")
#     if completed is not None:
#         task.completed = completed
#     if name is not None:
#         task.task_name = name
#     db.session.commit()
#     return success_response(new_task.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)