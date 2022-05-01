from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String,nullable =False)
    internships = db.relationship("Internship",cascade = "delete")


    def __init__(self, **kwargs):
        """Initialises the User"""
        self.name = kwargs.get("name")


    def serialize(self):
        """Serializes the User object"""
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
   
class Internship(db.Model):
    """
    Creates the Internship object      
    """
    __tablename__ = "internships"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String, nullable = False)
    time_since_application = db.Column(db.String, nullable = False)
    application_status = db.Column(db.String, nullable = False)
    tasks = db.relationship("Task", cascade = "delete") 
    additional_notes = db.Column(db.String, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),unique = True)
    
    def __init__(self, **kwargs):

        """Initialises the Internship Object"""

        self.company = kwargs.get("company")
        self.time_since_application = kwargs.get("time_since_application")
        self.application_status = kwargs.get("application_status")
        self.additional_notes = kwargs.get("additional_notes")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serializes the internship object
        """
        return {
            "id":self.id,
            "company":self.company,
            "time_since_application":self.time_since_application,
            "application_status":self.application_status,
            "tasks":[a.simple_serialize() for a in self.tasks],
            "additional_notes":self.additional_notes
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
        """Initialises the Task object"""
        self.task_name = kwargs.get("task_name", "")
        self.completed = kwargs.get("completed","")
        self.internship_id = kwargs.get("internship_id")

    def serialize(self):
        
        """Serialises the Task Object"""

        return{
            "id":self.id,
            "task_name":self.task_name,
            "completed":self.completed
        }
        

    