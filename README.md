# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

Install Backend Dependencies

Please follow the below steps to complete installation process:

1. Make sure python is installed in the system, you can check the version of python using below command:
    python --version

2. Set up Virtual Environment for the project to keep the dependencies for the project separate and organized. Please use below commands to create a virtual env and activate it in Windows:
    python -m venv venv
    source venv/Scripts/activate

3. Once the virtual environment is setup and running, install the required dependencies by navigating to the /backend directory and running:
     pip install -r requirements.txt

Set up the Database for trivia application:

1. With Postgres running, create a trivia database:
    create DATABASE trivia;
2. Populate the database using the trivia.psql file provided. From the backend folder in terminal run:
    psql -Upostgres trivia < trivia.psql

Plaesae use the below steps to set up the database for the TEST cases:

1. Create a trivia_test Database:
    create DATABASE trivia_test;
2. Create a test user trivia_test_user:
    create USER trivia_test_user WITH ENCRYPTED PASSWORD 'trivia_test';
3. Grant the permissions to the user on the database:
    grant ALL PRIVILEGES ON DATABASE trivia_test TO trivia_test_user;
    ALTER USER trivia_test_user CREATEDB;
    ALTER USER trivia_test_user WITH SUPERUSER;
4. Finally, populate the database using the trivia.psql file provided. From the backend folder in terminal run:
    psql -Utrivia_test_user trivia_test < trivia.psql

Run the Server

To run the server, use the below command in the /backend folder:
   export FLASK_APP=flaskr
   export FLAS_ENV=development
   FLASK_APP=flaskr FLASK_DEBUG=true flask run

API Documentation

GET '/categories'
    1. Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
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

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

Installing Dependencies

1. Installing Node and NPM This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download. Please check the version of the node using below command:
    node --version

2. Installing project dependencies This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the /frontend directory of this repository. After cloning, open your terminal and run:
    npm install

Running Your Frontend in Dev Mode
1. The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.
    npm start
    
2. Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.
