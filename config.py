"""Configuration for the app"""
import os

from sqlalchemy import create_engine


db_filename = "cadmv.db"
basedir = os.path.dirname(__file__)
db_url = "sqlite:////" + os.path.join(basedir, db_filename)

engine = create_engine(db_url, echo=False)  # leave echo=True while developing
