# Survey Application
## Getting Started
### Python Installation
* The project runs on [Python 3.10](https://www.python.org/downloads/).

### Additional Downloads

Apart from cloning this project, you also need the following -

- [Postgres-14.0-1](https://www.postgresql.org/download/)

**Make sure you get both the PostgreSQL server, and the Postgres Admin. The
default installation comes with both.**

### Running the project
Clone the repository.

```sh
git clone https://github.com/imraan024/survey-application.git
```
Create and activate a virtual environment for the project.

For creating virtual environment we can use packages like [Virtualenv](https://pypi.org/project/virtualenv/) or [Pyenv](https://github.com/pyenv/pyenv). I've used Virtualenv.

```sh
cd survey-application
virtualenv venv
source venv/bin/activte
```
Install all required packages.

```sh
pip install -r requirements.txt
```

Create a `.env` file copying from `.env.keep` file and update these values.
```env
# Comma separated hosts or IPs, set * to allow all
ALLOWED_HOSTS=127.0.0.1
# DEBUG=True
# Secret key should be atleast 32 characters long and consists of alphanumeric and special characters
SECRET_KEY=****
#Create a database on postgres and update `DB_URL` according to your credentials
DB_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
```
If you do any update on models run this command
```sh
python manage.py makemigrations
```
Run migrations to apply those on database
```sh
python manage.py migrate
```
Create a super user
```sh
python manage.py createsuperuser
```
Run the project.
```sh
python manage.py runserver
```

### Additional instruction
1. After running project you need to log in using your super user credentials.
1. You can sign up new user or add new user from default django admin dashboard.
1. To make new user active you should have set user type as `Customer` and check the `is_active` field otherwise you can not log in using new users credentials.
1. For New user creation you need to follow instruction 2 & 3 everytime.
1. You can make new survey and add question to them from admin panel after log in as `Admin`
1. You can participate on surveys from customer panel after log in as a `Customer`
