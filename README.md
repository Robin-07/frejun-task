# Frejun-Task
**This is a Django/ Django REST application which exposes 2 API endpoints for an SMS service**
## How To Run
### 1. Clone Repository using `git clone https://github.com/Robin-07/frejun-task.git`
### 2. Inside Repository, install requirements using `pip install -r requirements.txt`
### 3. Create a local Postgres server and connect it to the app by editing DATABASE settings in `src/src/settings.py`
### 4. Populate the Postgres server with the data dump and then inside src directory, run commands `python manage.py makemigrations` and `python manage.py migrate`
### 5. Start local development server by using command `python manage.py runserver` inside src directory
## Testing
### While the local server is running, run command `python manage.py test` inside src directory. This will run all the tests.
## Heroku Deployment
#### I have deployed the app on heroku - https://dj-sms-service.herokuapp.com/ but some DB changes are required for it to work properly
