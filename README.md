# iDetect
### Introduction
iDetect is a Python based desktop application using PyQT6, Tensorflow, OpenCv-Python etc.
iDetect is a implementation of Object Detection using Deep Neural Network.
Refer the Paper - 
### Project Support Features
* Users can setup 
* Public (non-authenticated) users can access the details of stores, items and tags on the platform
* Authenticated users in addition, can create or modify store, item, tag or link/unlink a store and tag.
### Installation Guide
* Clone this repository [here](https://github.com/karti358/flask-rest-api.git).
* The main branch is the most stable branch at any given time, ensure you're working from it.
* Ensure you create a virtual environment and activate the environment
* ## Create Virtual Environment
      python -m venv venv
* ## Activate virtual environment
  ## Linux
      source ./venv/bin/activate
  ## Windows
      ./venv/Scripts/activate
* ## Run the following command to install all dependencies
      pip install -r requirements.txt
* ## Create a new .env in project root and paste following line in it. Fill the needed data.
      SECRET_KEY=<secret_key>
      DATABASE_URI=<database-uri>
### Usage
* ## Run the following command to start the application.
      flask run
  ## if the above do not work
      python app.py
* Connect to the API using Postman.
### API Endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| | Users | |
| POST | /user/register | To sign up a new user account |
| POST | /user/login | To login an existing user account |
| POST | /user/logout | To logout an existing user account |
| POST | /user/refresh | To refresh an existing refresh token of user account |
| | Stores | |
| GET | /store | To retrieve details of all stores on the platform |
| POST | /store | To add a store on the platform |
| GET | /store/:store_id | To retrieve an existing store on platform with id |
| DELETE | /store/:store_id | To delete an existing store on platform with id |
| | Items | |
| GET | /item | To retrieve details of a all items |
| POST | /item | To add an item to the platform |
| GET | /item/:item_id | To retrieve a single item by id |
| DELETE | /item/:item_id | To delete a single item by id |
| PUT | /item/:item_id | To modify a single item by id |
| | Tags | |
| GET | /store/:store_id/tag | To retrieve all tags of a store |
| POST | /store/:store_id/tag | To add a single tag to a store |
| POST | /item/:item_id/tag/:tag_id | To link a tag and an item |
| DELETE | /item/:item_id/tag/:tag_id | To unlink an already linked tag and item |
| GET | /tag/:tag_id | To retrieve a single tag with its id |
| POST | /tag/:tag_id | To delete a single tag with ist id |
### Technologies Used
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
### License
This project is available for use under the Apache 2.0 License.
