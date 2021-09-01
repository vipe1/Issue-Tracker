# Issue Tracker
> Issue Tracker inspired by Jira

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Docker](#docker)
* [App screenshots](#app-screenshots)

## General info
This is issue tracking app made for organising work on projects.
You can create your own teams or join other teams with invitation link.
Every team consists of members who have one of the 3 roles (excluding project's owner):
* Admin
* Developer
* Spectator

Members can create issues which can have different types, priorities and statuses (based on Jira issue system).
Every issue has it's history and comments.
Every user has his own dashboard where he can see all of the active issues asssigned to him.
Creating new users is protected with [Google reCAPTCHA V3](https://developers.google.com/recaptcha/docs/v3)

## Technologies
Project has been created using:
* Django - version: 3.2
* django-simple-history - version: 3.0
* django-tables2 - version .4
* Django Crispy Forms - version: 1.12
* Whitenoise - version: 5.3
* requests - version 2.26
	
## Setup
To run this project locally, download the code from repo and run it in virtual environment with:

```
$ cd issue-tracker-master
$ pip install -r requirements.txt
$ python manage.py runserver
```
You will also have to set these environmental variables:
```
SECRET_KEY=

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASS=

CAPTCHA_SITE_KEY=
CAPTCHA_SECRET_KEY=

SENDGRID_API_KEY=
FROM_EMAIL=
```

If you don't want to use Sendgrid you can use Django's Console Email by setting
`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

## Docker
Docker container image coming soon...

## App screenshots
* Invite page
![Invite](/screenshots/its-invite.png?raw=true "Invite")

* Members page
![Members](/screenshots/its-members.png?raw=true "Members")

* Member details page
![Member details](/screenshots/its-member-details.png?raw=true "Member details")

* Issue details page
![Issue details](/screenshots/its-issue-details.png?raw=true "Issue details")

* Dashboard page
![Dashboard](/screenshots/its-dashboard.png?raw=true "Dashboard")

