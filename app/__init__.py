from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


##Create Database
db = SQLAlchemy()

##Create application
def create_app(config_class = Config)