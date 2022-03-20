# api_poc

This project is the django api rest for a simple social network. Its was made with django rest framework.

## Software Requirements

**Programming language**: Python 3

**Framework** : Django

**Database** : Sqlite

**Virtual Environment**: Virtualenv 

**Deploy of api_poc**: [Heroku](https://app-poc-dspot.herokuapp.com/api/jwt/token/) -> [Documentation](https://app-poc-dspot.herokuapp.com/docs/)  

## Download & Run on local

### Clone the repository, install packages and run the api

```bash
//on local
git clone https://github.com/vestefano/api_poc.git
cd api_poc
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

>Note: By default the api starts running on port 8000. The api documentation can be found at 
http://localhost:8000/docs/

## Run test
```bash
python manage.py test

//to run tests with existing db test 
python manage.py test --keepdb

//to run unit tests only
python manage.py test --keepdb --settings=api_poc.settings_mocked_dev
```

>Note: To use all the entry points it is necessary to be authenticated except for creating a user and 
accessing the api documentation. In the project there is an administration layer, to access those entry 
points you must have an admin user. 

## Create admin user
```bash
// after the migrations
python manage.py createsuperuser
```

## Run seeder
To run the seeder it is necessary to have an internet connection and have the project running. In the console where 
it is going to run, it is necessary to have the virtual environment active with ```source venv/bin/activate```

```bash
python seeder_script.py
```

When the seeder finishes, a list will appear with the username and password data of each user that it was created, as shown 
below:
```bash
{'id': 63, 'username': 'sadmouse851', 'password': 'spoon'}
{'id': 64, 'username': 'goldenleopard281', 'password': 'iloveyou'}
{'id': 65, 'username': 'bigcat955', 'password': 'celeron'}
{'id': 66, 'username': 'brownrabbit327', 'password': 'qaz123'}
{'id': 67, 'username': 'happyostrich517', 'password': '123456'}
```

The seeder is passed the following parameters:
- The url of the api, in case nothing is passed to it, it is assumed to be ```http://localhost:8000```
- The number of profiles you want
- The number of friends each profile should have

>Note: The project has pylint-django for code quality. To run it use this command
```bash
pylint --load-plugins pylint_django --django-settings-module=api_poc.settings accounts api_poc seeder_script.py
```
