# The Octopus Library

The Octopus Library is an online platform for selling/buying old books built with [Python](https://www.python.org/) using the [Django Web Framework](https://www.djangoproject.com/).

**P.S:** Implemented the Rest API using [Django Rest Framework](http://django-rest-framework.org/).

### Demo

Check the website at [http://theoctopuslibrary.pythonanywhere.com](http://theoctopuslibrary.pythonanywhere.com/)

![The Octopus Library Screenshot](https://image.ibb.co/mr1YfT/theoctopuslibrary_screenshot.jpg "The Octopus Library Screenshot")

### Technology Stack

* Python 3.6
* Django 1.11
* Django Rest Framework 3.8
* Twitter Bootstrap 4
* jQuery 3
* Pinax Messages (API built by hand)

### Installation Guide

Clone this repository:

```shell
$ git clone https://github.com/thetruefuss/theoctopuslibrary.git
```

Install requirements:

```shell
$ pip install -r requirements.txt
```

Copy `.env.example` file content to new `.env` file and update the credentials if any i.e Gmail account etc.

Run Django migrations to create database tables:

```shell
$ python manage.py migrate
```

Run the development server:

```shell
$ python manage.py runserver
```

Verify the deployment by navigating to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your preferred browser.
