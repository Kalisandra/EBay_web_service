import os

from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# Ebay API keys
APPID = ""
CERTID = ""
DEVID = ""
RUNAME = ""

# Web service keys
SECRET_KEY = ""

# Data base
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=5)
