import datetime
import hashlib
import os

import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String,nullable =False)
    internships = db.relationship("Internship",cascade = "delete")

    # User Login information
    email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)


    def __init__(self, **kwargs):
        """
        Initialises the User
        """
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()


    def serialize(self):
        """
        Serializes the User object
        """
        return {
            "id":self.id,
            "name":self.name,
            "internships": [a.simple_serialize() for a in self.internships]
        }
    
    def simple_serialize(self):
        """
        Simple serialises the user
        """
        return {
            "internship": [a.simple_serialize() for a in self.internships]
        }
        
    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == self.update_token
   
class Internship(db.Model):
    """
    Creates the Internship object      
    """
    __tablename__ = "internships"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    application_status = db.Column(db.String, nullable = False)
    tasks = db.relationship("Task", cascade = "delete") 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),unique = True)
    
    def __init__(self, **kwargs):
        """
        Initialises the Internship Object
        """
        self.company = kwargs.get("company")
        self.description = kwargs.get("description")
        self.title = kwargs.get("title")
        self.application_status = kwargs.get("application_status")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serializes the internship object
        """
        return {
            "id":self.id,
            "company":self.company,
            "title": self.title,
            "description": self.description,
            "application status":self.application_status,
            "tasks":[a.simple_serialize() for a in self.tasks],
        }
        
    def simple_serialize(self):
        """
        Simple Serialize a internship object with only name and status
        """
        return {
            "company":self.company,
            "status":self.application_status
        }

class Task(db.Model):
    """
    Creates the Task object
    """
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String, nullable = False)
    completed = db.Column(db.String, nullable = False)
    intership_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable = False)
    
    def __init__(self, **kwargs):
        """
        Initialises the Task object
        """
        self.task_name = kwargs.get("task_name", "")
        self.completed = kwargs.get("completed", "")
        self.internship_id = kwargs.get("internship_id")

    def serialize(self):  
        """
        Serialises the Task Object
        """
        return{
            "id":self.id,
            "task_name":self.task_name,
            "completed":self.completed
        }
        

    