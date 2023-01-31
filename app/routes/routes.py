from flask import Blueprint, jsonify, request
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

@query_bp.route("", methods = ["GET"]) #this will be for a single group by query. 
def query():
    #THIS ROUTE NEEDS TESTING
    queryParam = request.args
    company_query = queryParam.get('company', type=str) #put in default?
    year_query = queryParam.get('year', type=int) #make type date? #put in default?
    groupBy_field = queryParam.get('groupBy', type=str)
    
    #set up a dictionary for this!!!
    if groupBy_field == "race":
        field = Eeo1_data.race
    elif groupBy_field == "gender":
        field = Eeo1_data.gender
    elif groupBy_field == "job":
        field = Eeo1_data.job_category
    else:
        pass #return an error.
    #make results in the form valueData and labelData. 
    field_totals = db.session.query(field, func.sum(Eeo1_data.count_employees)).filter_by(company=company_query, year=year_query).group_by(field).all()
    return_dict = {}
    for field_label, count_employees_total in field_totals:
        return_dict[field_label] = count_employees_total
    return jsonify(return_dict)


@query_bp.route("/get_all", methods = ["GET"])
def get_all_entries():
    #THIS ROUTE NEEDS TESTING
    queryParam = request.args

    data = Eeo1_data.query.filter_by(**queryParam)

    response = [data_line.to_dict() for data_line in data]
    return jsonify(response)

#make a route that returns the list of companies #need to pull once
#returns a dictionary with keys that are companies and values that is a list of valid years? 


