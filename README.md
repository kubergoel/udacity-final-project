# API Development and Documentation Final Project

## Capstone Casting Agency App

The project documented here is the final project of Udacity Full Stack Nanodegree Program. The goal here is to create a Flask application with Postgres Database that should be deployed in the AWS kubernetes engine along with CI/CD pipelines. Also, we need to enable the Authentication and role-based access control using Auth0. 

This project depicts the backend APIs that can be integrated to any Frontend application.

## Starting and Submitting the Project

[clone](https://github.com/kubergoel/udacity-final-project.git) the project repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.


### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `app.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `app.py`
2. `test_app.py`

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

The application is deployed on AWS Kubernetes engine along with CI/CD pipeline. So, any change made to the repository will automatically trigger the build and changes will be reflected automatically.

API Documentation

There is an attached json file "casting-agency.postman_collection.json" which contains all the APIs along with the sample request body.

Please import the JSON in Postman to see individual API.