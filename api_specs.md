GET all users
GET/api/users/
<HTTP STATUS CODE 200>
{
    "users": [
        {
            "id": 1,
            "name": "upson",
            "internships": [
                {
                    "id": 1,
                    "title": "sde",
                    "company": "google",
                    "status": "applied"
                }
            ]
        },
        {
            "id": 2,
            "name": "peepeepoopoo",
            "internships": []
        },
        {
            "id": 3,
            "name": "duff",
            "internships": [
                {
                    "id": 2,
                    "title": "step intern",
                    "company": "google",
                    "status": "applied"
                }
            ]
        }
    ]
}

----------------------------------------------------------

Register account
POST/register/
<HTTP STATUS CODE 201>

REQUEST
{
    "name": "Mustafa"
    "email":"zeLionKing"
    "password": "password"
}

RESPONSE
{
    "session_token": "6da156c5d3a98a59513b8dee358aada3b7267db7",
    "session_expiration": "2022-05-07 20:14:57.795677",
    "update_token": "1167c1f4d5d99b55358a18e321c8b5b8242e7e41"
}

----------------------------------------------------------

Login
POST/login/
<HTTP STATUS CODE 201>

REQUEST
{
    "email": "duff@gmail.com",
    "password": "duff123"
}

RESPONSE
{
    "session_token": "6da156c5d3a98a59513b8dee358aada3b7267db7",
    "session_expiration": "2022-05-07 20:14:57.795677",
    "update_token": "1167c1f4d5d99b55358a18e321c8b5b8242e7e41"
}

----------------------------------------------------------

DELETE a user
DELETE/api/users/{id}/
<HTTP STATUS CODE 200>

RESPONSE 
{
    "id": 2,
    "name": "peepeepoopoo",
    "internships": []
}

----------------------------------------------------------

Get all internships for one user
GET /api/internships
<HTTP STATUS CODE 200>

RESPONSE
{
    "internship": [
        {
            "id": 2,
            "title": "step intern",
            "company": "google",
            "status": "applied"
        }
    ]
}

----------------------------------------------------------

Get one specific internship
GET /api/internships/{internship_id}/
<HTTP STATUS CODE 200>

RESPONSE
{
    "id": 2,
    "company": "google",
    "title": "step intern",
    "description": "for first and second year",
    "application status": "applied",
    "tasks": []
}

----------------------------------------------------------

CREATE an internship
POST/api/internships/
<HTTP STATUS CODE 201>
REQUEST
{
    "company": "google",
    "status": "applied",
    "description": "for first and second year",
    "title": "step intern"
}

RESPONSE 
{
    "id": 2,
    "company": "google",
    "title": "step intern",
    "description": "for first and second year",
    "application status": "applied",
    "tasks": []
}

----------------------------------------------------------

DELETE a specific internship
DELETE/api/internships/{internship_id>}/
<HTTP STATUS CODE 200>

RESPONSE 
{
    "id": 2,
    "company": "google",
    "title": "step intern",
    "description": "for first and second year",
    "application status": "applied",
    "tasks": []
}

----------------------------------------------------------

EDIT a specific internship
POST /api/internships/{internship_id>}/
<HTTP STATUS CODE 200>

REQUEST
{
    "id": 1,
    "company": "google",
    "title": "sde",
    "description": "fun",
    "application status": "accepted",
    "tasks": []
}

RESPONSE
{
    "status": "accepted"
}

----------------------------------------------------------

GET all tasks of a user's internship
GET/api/{user_id}/internships/{internship_id>}/tasks/
<HTTP STATUS CODE 200>

RESPONSE
[
    {
        "id": 1,
        "task_name": "email recruiter",
        "completed": "False"
    }
]

----------------------------------------------------------

GET specific task
GET/api/{user_id}/internship/{internship_id}/tasks/{task_id}/
<HTTP STATUS CODE 200>

RESPONSE
{
    "id": 1,
    "task_name": "email recruiter",
    "completed": "False"
}

----------------------------------------------------------

CREATE a task
POST/api/{user_id}/internships/{internship_id>}/tasks/
<HTTP STATUS CODE 201>

REQUEST
{
    "task name": "go to information session"
}

RESPONSE
{
    "id": 1,
    "task_name": "go to information session",
    "completed": "False"
}

----------------------------------------------------------

EDIT specific task
POST/api/{user_id}/internship/{internship_id}/tasks/{task_id}/
<HTTP STATUS CODE 200>

REQUEST
{
    "completed": "True"
}

RESPONSE
{
    "id": 1,
    "task_name": "email recruiter",
    "completed": "True"
}