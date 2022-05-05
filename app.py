from db import db
from db import User
from db import Internship
from db import Task
from flask import Flask, request
import json
import datetime

import os
import users_dao
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


@app.route("/api/internships/")
def get_user_internships():
    """
    Endpoint for getting general information of all internships for a user
    """
    was_successful, session_token = extract_token(request)
    if not was_successful:
       return session_token
    user = users_dao.get_user_by_session_token(session_token)
    if user is None:
        return failure_response("user not found", 404)

    return success_response(user.simple_serialize())

@app.route("/api/internships/<int:internship_id>/")
def get_specific_internship(internship_id):
    """"
    Endpoint for getting a specific internship with detailed information for a user
    """
    was_successful, session_token = extract_token(request)
    if not was_successful:
       return session_token
    user = users_dao.get_user_by_session_token(session_token)
    if user is None:
        return failure_response("user not found", 404)
        
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    return success_response(internship.serialize())

@app.route("/api/internships/", methods = ["POST"])
def create_internship():
    """
    Endpoint for creating an internship for a user
    """
    was_successful, session_token = extract_token(request)
    if not was_successful:
       return session_token
    user = users_dao.get_user_by_session_token(session_token)
    if user is None:
        return failure_response("user not found", 404)
    body = json.loads(request.data)
    if body.get("company") is None or body.get("status") is None or body.get("title") is None or body.get("description") is None:
        return failure_response("please include necessary information to create internship", 400)
    company = body.get("company")
    status = body.get("status")
    title = body.get("title")
    description = body.get("description")

    new_internship = Internship(
        company = company, 
        title = title,
        description = description,
        application_status = status,
        user_id = user.id
        )
    db.session.add(new_internship)
    db.session.commit()
    return success_response(new_internship.serialize(), 201)

@app.route("/api/internships/<int:internship_id>/", methods = ["DELETE"])
def delete_internship(internship_id):
    """
    Endpoint for deleting an internship for a user
    """
    was_successful, session_token = extract_token(request)
    if not was_successful:
       return session_token
    user = users_dao.get_user_by_session_token(session_token)

    if user is None:
        return failure_response("user not found", 404)
        
    internship = Internship.query.filter_by(id=internship_id).first()
    
    if internship is None:
        return failure_response("internship not found", 404)
    db.session.delete(internship)
    db.session.commit()
    return success_response(internship.serialize(),201)

@app.route("/api/internships/<int:internship_id>/", methods = ["POST"])
def edit_internship(internship_id):
    """
    Endpoint for editing a specific internship
    """
    was_successful, session_token = extract_token(request)
    if not was_successful:
       return session_token
    user = users_dao.get_user_by_session_token(session_token)

    if user is None:
        return failure_response("user not found", 404)

    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    body = json.loads(request.data)
    status = body.get("status")
    description = body.get("description")
    if status is not None:
        internship.application_status = status
    if description is not None:
        internship.description = description
    db.session.commit()
    return success_response(internship.serialize(), 201)

@app.route("/api/<int:user_id>/internships/<int:internship_id>/tasks/")
def get_tasks(user_id, internship_id):
    """
    Endpoint for getting all tasks for a user's internship
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    tasks = [t.serialize() for t in internship.tasks]
    return success_response(tasks, 201)

@app.route("/api/<int:user_id>/internship/<int:internship_id>/tasks/<int:task_id>/")
def get_specific_task(user_id, internship_id, task_id):
    """
    Endpoint for getting a specific task for a user's internship
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("task not found", 404)
    return success_response(task.serialize(), 201)

@app.route("/api/<int:user_id>/internships/<int:internship_id>/tasks/", methods = ["POST"])
def create_task(user_id, internship_id):
    """
    Endpoint for creating a task for a user's internship
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    body = json.loads(request.data)
    name = body.get("task name")
    if name is None:
        return failure_response("please include necessary information to create task", 400)
    new_task = Task(
        task_name = name,
        completed = "False",
        internship_id = internship_id
    )
    internship.tasks.append(new_task)
    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize(), 201)


@app.route("/api/<int:user_id>/internships/<int:internship_id>/tasks/<int:task_id>/", methods = ["POST"])
def edit_task(user_id, internship_id, task_id):
    """
    Endpoint for editing a task for a user's internship
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found", 404)
    internship = Internship.query.filter_by(id=internship_id).first()
    if internship is None:
        return failure_response("internship not found", 404)
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("task not found", 404)
    body = json.loads(request.data)
    completed = body.get("completed")
    name = body.get("task name")
    if completed is not None:
        task.completed = completed
    if name is not None:
        task.task_name = name
    db.session.commit()
    return success_response(task.serialize(), 201)


#AUTHENTICATION

def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """

    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, json.dumps({"Missing authorization header"})
    
    #gets the token from auth header value
    bearer_token = auth_header.replace("Bearer", "").strip()

    #now that we have the token itself we can return 
    return True, bearer_token


@app.route("/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)

    name = body.get("name")
    email = body.get("email")
    password = body.get("password")


    if name is None or email is None or password is None:
        return failure_response("Missing name or email or password")

    was_successful, user = users_dao.create_user(name, email, password)

    if not was_successful:
        return failure_response("User already exists")

    return success_response(
        {
            "session_token":user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token        }
    )
    
@app.route("/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if (email is None) or (password is None): #normal failure error
        return failure_response("Missing email or password", 400)

    was_successful, user = users_dao.verify_credentials(email,password)
    
    if not was_successful: #authorisation error 
        return failure_response("Incorrect username or password", 401)
    
    return success_response(
        {
            "session_token":user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token 
        }
    )
@app.route("/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    """
    was_successful, update_token = extract_token(request)
    
    if not was_successful:
        return update_token
    
    try:
        user = users_dao.renew_session(update_token)
    except Exception as e:
        return failure_response(f"Invalid update token: {str(e)}")
    
    return success_response(
        {
            "session_token":user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token 
        }
    )


@app.route("/secret/", methods=["GET"])
def secret_message():
    """
    Endpoint for verifying a session token and returning a secret message

    In your project, you will use the same logic for any endpoint that needs 
    authentication
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
       return session_token #it'll return a failure response

    #similar to getting user by their ID, but instead now by their session token 
    user = users_dao.get_user_by_session_token(session_token)

    #make sure the user exists and the session token is valid
    if not user or not user.verify_session_token(session_token):
        return failure_response({"Invalid session token"})

    #return the secret message
    return success_response({"message":"You have succesfully implemented the session"})

@app.route("/logout/", methods=["POST"])
def logout():
    
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    user = users_dao.get_user_by_session_token(session_token)

    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    user.session_expiration = datetime.datetime.now()
    db.session.commit()

    return success_response({
         "message": "You have successfully logged out!"
    }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)