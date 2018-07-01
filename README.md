# What is this ?
Corefun is a modern, tranparent, and open-source social media.

# Why, isn't Facebook enough ?
Corefun, from its name, mainly aims to bring fun for the users!

We ain't competing, we just believe we are making things right.

# How to run this ?

As with any other django project, you have to migrate the database and then run the server:

```
python manage.py migrate
python manage.py runserver

```
runserver on localhost SSL:
* to test social account login: replace 127.0.0.1 with localhost.
'''
python manage.py runserver_plus --cert-file /tmp/cert
'''

install requirments file : pip install -r requirements.txt


