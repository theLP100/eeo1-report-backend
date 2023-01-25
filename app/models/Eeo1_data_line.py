from app import db
from flask import Blueprint

class Eeo1_data_line(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    count_employees = db.Column(db.Integer, nullable = False) #these numbers are large, but not large enough to justify using bigint.  int is fine.
    job_category = db.Column(db.String, nullable = False)  #to-do later: change these string columns to enums. 
    gender = db.Column(db.String, nullable = False)
    race = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    company = db.Column(db.String, nullable = False)

