# API Development and Documentation Final Project

## Capstone Casting Agency App

The project documented here is the final project of Udacity Full Stack Nanodegree Program. The goal here is to create a Flask application with Postgres Database that should be deployed in the AWS kubernetes engine along with CI/CD pipelines. Also, we need to enable the Authentication and role-based access control using Auth0. 

This project depicts the backend APIs that can be integrated to any Frontend application.

## Starting and Submitting the Project

[clone](https://github.com/kubergoel/udacity-final-project.git) the project repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.


### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

Install Backend Dependencies

Please follow the below steps to start the application on local environment:

1. Make sure python v3.12 is installed in the system, you can check the version of python using below command:
    python --version

2. Set up Virtual Environment for the project to keep the dependencies for the project separate and organized. Please use below commands to create a virtual env and activate it in Windows:
    python -m venv venv
    source myvenv/bin/activate

3. Once the virtual environment is setup and running, install the required dependencies by navigating to the /backend directory and running:
     pip install -r requirements.txt

Set up the Database for casting_agency application:

Populate the database using the database/init.sql file provided. From the backend folder in terminal run:
    psql -Upostgres < database/init.sql

The above script will create both the casting_agency DB and test_casting_agency DB used to execute the test cases.


Run the Server:

To run the server, use the below command in the /backend folder:
   export FLASK_APP=app.py
   export FLAS_ENV=development
   FLASK_APP=app.py FLASK_DEBUG=true flask run

To run the test case, use the below command:
    python test_app.py

Authorization & Authentication:

The access token for making the REST calls is generated using Auth0. Use the below URL to generate the access token:

https://dev-iyauk2au1anrxgs7.us.auth0.com/authorize?audience=casting-agency-api&response_type=token&client_id=LLlhXGEd6NaHPLYbwLxdXQp8M70mILEt&redirect_uri=https://127.0.0.1:5000/

Note: Make sure the application is up in local mode while generating the token.

API Documentation

GET '/movies'
    1. Fetches list of Movie with the permission: 'get:movies'
    2. Request Arguments: None
    3. Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
    4. Example:
        Request: $ curl http://127.0.0.1:5000/categories -X GET
        Response:    {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "success": true
            }

GET '/questions?page=${integer}'

    1. Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    2. Request Arguments: page - integer type
    3. Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
    4. Example:
        Request: $ curl http://127.0.0.1:5000/questions?page=1 -X GET
        Response:    {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "current_category": "Entertainment",
            "questions": [
                {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                ...
            ],
            "success": true,
            "total_questions": 20
            }

GET '/categories/${id}/questions'

    1. Fetches questions for a cateogry specified by id request argument
    2. Request Arguments: Category ID - integer
    3. Returns: An object with questions for the specified category, total questions, and current category string
    4. Example:
        Request: curl http://127.0.0.1:5000/categories/6/questions -X GET
        Response:   {
                "current_category": "Sports",
                "questions": [
                    {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                    }
                ],
                "success": true,
                "total_questions": 1
                }

DELETE '/questions/${id}'

    1. Deletes a specified question using the id of the question
    2. Request Arguments: Question id - integer
    3. Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
    4. Example:
        Request:  curl http://127.0.0.1:5000/questions/14 -X DELETE -H "Content-Type: application/json"
        Respoonse:    {
            "question_id": 14,
            "success": true
            }

POST '/questions'

    1. Sends a post request in order to add a new question
    2. Request Body:
        {
        "question": "Heres a new question string",
        "answer": "Heres a new answer string",
        "difficulty": 1,
        "category": 3
        }
    3. Example:
        Request:        curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d  '{"question":"Which is the only team to fail against India?","answer":"Pakistan"
        ,"difficulty":5,"category":"3"}'
        Response:   {
                    "question_id": 26,
                    "success": true
                    }
POST '/questions/search'

    1. Sends a post request in order to search for a specific question by search term
    2. Request Body:
        {
        "searchTerm": "this is the term the user is looking for"
        }
    3. Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
    4. Example:
        Request:  curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"AFRICA"}'
        Response:    {
            "current_category": "Geography",
            "questions": [
                {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
                }
            ],
            "success": true,
            "total_questions": 1
            }

POST '/quizzes'

    1. Sends a post request in order to get the next question
    2. Request Body:
        {
            'previous_questions': [1, 4, 20, 15]
            quiz_category': 'current category'
        }
    3. Returns: a single new question object
    4. Example:
        Request: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[1,2,3,4,14,15,13,24], "quiz_category": "3"}'
        Response:    {
            "question": {
                "answer": "Pakistan",
                "category": 3,
                "difficulty": 5,
                "id": 26,
                "question": "Which is the only team to fail against India?"
            },
            "success": true
            }
