#!/usr/bin/python
import MySQLdb
import unittest
from datetime import datetime, timedelta
from app.models import User, Recipe
from config import basedir
from app import app, db
import os
import sqlalchemy as sa
import sqlalchemy.orm as orm

def clean_string(s):
    s = s.replace(chr(0x91),"'")
    s = s.replace(chr(0x96),"-")
    s = s.replace(chr(0x92),"'")
    s = s.replace(chr(0x94),"\"")
    s = s.replace(chr(0x93),"\"")
    s = s.replace(chr(0x85),"\"")
    s = s.replace(chr(0xbd),"1//2")
    s = s.replace(chr(0xbc),"1//4")
    s = s.replace(chr(0xe9),"e")
    s = s.replace(chr(0xb0),"deg ")
    s = s.replace(chr(0xba),"deg ")
    s = s.replace(chr(0xae),"")
    s = s.replace(chr(0x95),":")
    s = s.replace(chr(0x99),"")
    return s

def import_our_recipes():
    cur.execute("SELECT * FROM recipes")
    bad_recipes = []#54,53,83, 101,108,109,114,115,120,121,122,123,125,126,128,132]
    max_length = 0
    for row in cur.fetchall() :
        if row[0] not in bad_recipes:
            rec = Recipe()
            print row[0]
            rec.recipe_name = row[2]
            rec.recipe_name = clean_string(rec.recipe_name)
            rec.ingredients = row[3].replace("|","\n")
            rec.ingredients = clean_string(rec.ingredients)
            rec.directions = row[4].replace("|","\n")
            rec.directions = clean_string(rec.directions)
            rec.notes =row[5].replace("|","\n")
            rec.notes = clean_string(rec.notes)
            rec.notes = clean_string(rec.notes)
            rec.user_id = 1
            rec.timestamp = row[1]
            rec.image_path = row[9]
            rec.rating = row[8]
            rec.was_cooked = 1
            db_session.add(rec)
            db_session.commit()
def import_moms_recipes():
    cur.execute("SELECT * FROM moms")
    bad_recipes = []#5,18,70,77]
    max_length = 0
    for row in cur.fetchall() :
        if row[0] not in bad_recipes:
            rec = Recipe()
            print row[0]
            rec.recipe_name = row[1]
            rec.recipe_name = clean_string(rec.recipe_name)
            
            rec.ingredients = row[3].replace("|","\n")
            rec.ingredients = clean_string(rec.ingredients)
            rec.directions = row[4].replace("|","\n")
            rec.directions = clean_string(rec.directions)
            rec.notes =row[5].replace("|","\n")
            rec.notes = clean_string(rec.notes)
            rec.user_id = 2
            

            db_session.add(rec)
            db_session.commit()

def create_session():
    engine = sa.create_engine('sqlite:///app.db')
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session  

db = MySQLdb.connect(host="192.168.1.101", # your host, usually localhost
                     user="root", # your username
                      passwd="matthew", # your password
                      db="recipes") # name of the data base

cur = db.cursor() 
db_session = create_session()
import_moms_recipes()
import_our_recipes()



