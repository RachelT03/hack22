from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User Model

    Has a many-to-many relationship with the Internship Model
    {
        "users": [
            {
                "id": 1,
                "name": "sam",
                "internships" : []
            }
        ]
    }
    """
    def __init__(self, **kwargs):
        return

    def serialize(self):
        return
    
    def simple_serialize(self):
        return
    
class Internship(db.Model):
    """
    Internship Model

    Has a one to-many relationship with the User Model
    {
        "internships":[
            {
                "id": 1,
                "user_id": <user_input>
                "company name": "Google",
                "time since application" : "3 weeks",
                "application status": "applied,in progress, accepted/denied",
                "contact information": [],
                "tasks" : [],
                "additional notes": OPTIONAL
            }
        ]
    }
    """
    def __init__(self, **kwargs):
        return

    def serialize(self):
        return
    
    def simple_serialize(self):
        return

class Task(db.Model):
    """
    Task Model

    Has a one-to-many relationship with Internship Model
    {
        "tasks":[
            {
                "id": 1,
                "task name": practice leetcode,
                "completed": TRUE or FALSE
            }
        ]
    }
    """
    def __init__(self, **kwargs):
        return

    def serialize(self):
        return
    
    def simple_serialize(self):
        return

    