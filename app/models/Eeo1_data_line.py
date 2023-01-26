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

    def to_dict(self):
        """given a line of data, reutrn it in a dictionary form we can work with.
        This is for raw data coming in..."""
        data_dict = {
            "id" : self.id,
            "count_employees" : self.count_employees,
            "job_category" : self.job_category,
            "gender" : self.gender,
            "race" : self.race,
            "year" : self.year,
            "company" : self.company
        }
        return data_dict

