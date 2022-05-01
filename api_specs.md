GET all users
GET/users/
<HTTP STATUS CODE 200>
{
    "users":[
        "id": 1,
        "name": "sam",
        "internship": [<SERIALIZED INTERNSHIP>]
    ]
}
CREATE a user
POST/api/users/
<HTTP STATUS CODE 201>

REQUEST
{
    "name": "Mustafa"
    "username":"zeLionKing"
}

RESPONSE
{
    "id":<ID>
    "name": "Mustafa"
    "internships": []
}

DELETE a user
DELETE/api/users/{id}/
<HTTP STATUS CODE 200>

RESPONSE 
{
    "id":<ID>
    "name": "Mustafa"
    "internships":<USER_INTERSHIPS>

}

Get a user internship
GET /api/users/{id}/
<HTTP STATUS CODE 200>

RESPONSE
{
    "id":<ID>
    "name": "Mustafa"
    "internships":<USER_INTERSHIPS>
}


CREATE a specific internship
POST/api/{user_id}/internships/{internship_id>}/
<HTTP STATUS CODE 201>
REQUEST
{

    "company" = "Petronas"
    "application_status" = "applied"
    "description": "nice company" 
    "tasks" = []
}

RESPONSE 
{
    "id" = <ID>
    "description" = ""
    "company" = "Petronas" 
    "application_status" = "applied"
    "tasks" = []
}

DELETE a specific internship
DELETE/api/{user_id}/internships/{internship_id>}/
<HTTP STATUS CODE 200>

RESPONSE 
{
    id = <ID>
    "company" = "Petronas" 
    "application_status" = "applied"
    "tasks" = []
}

EDIT a specific internship
POST /api/{user_id}/internships/{internship_id>}/
<HTTP STATUS CODE 200>

REQUEST
{
    "status":
    "description":
}

RESPONSE
{
    "id": <ID>,
    "company": "meta",
    "application_status": <USER_INPUT>,
}

GET all tasks
GET/api/{user_id}/internships/{internship_id>}/tasks/
<HTTP STATUS CODE 200>

RESPONSE
{
    "id":<ID>,
    "task_name":"get boba",
    "completed":True
}

GET specific task
GET/api/{user_id}/internship/{internship_id}/tasks/{task_id}/
<HTTP STATUS CODE 200>

RESPONSE
{
    "id":<ID>,
    "task_name":"get boba",
    "completed":True
}

CREATE a task
POST/api/{user_id}/internships/{internship_id>}/tasks/
<HTTP STATUS CODE 201>

REQUEST
{
    "task name" = "do backend hw"
}

RESPONSE
{
    "id":<TASK_ID>,
    "task_name":"do backend hw",
    "completed":False
}

EDIT specific task
POST/api/{user_id}/internship/{internship_id}/tasks/{task_id}/
<HTTP STATUS CODE 200>

REQUEST
{
    "task_name" = "download cheat sheet"
    "completed" = "False"
}

RESPONSE
{
    "id":<TASK_ID>,
    "task_name":"download cheat sheet",
    "completed": "True"
}

