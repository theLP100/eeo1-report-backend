from flask import Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

#-------a single group by query. required params: company, year, groupBy--------#
@query_bp.route("", methods = ["GET"]) 
def query():
    #THIS ROUTE NEEDS TESTING
    #make helper functions for this to make it read more clearly and have only one job per function?
    queryParam = request.args
    company_query = queryParam.get('company', type=str) 
    year_query = queryParam.get('year', type=int) 
    groupBy_field = queryParam.get('sortBy', type=str)
    
    field_dict = {
        "race": Eeo1_data.race,
        "gender": Eeo1_data.gender,
        "job": Eeo1_data.job_category
    }
    try: field = field_dict[groupBy_field]
    except:
        response_str = f"Please enter a field to sort by.  Enter a query param with key sortBy and value race, gender, or job."
        abort(make_response({"message": response_str}, 400))

    field_totals = db.session.query(field, func.sum(Eeo1_data.count_employees)).filter_by(company=company_query, year=year_query).group_by(field).all()
    labelData = []
    valueData = []
    for field_label, count_employees_total in field_totals:
        labelData.append(field_label)
        valueData.append(count_employees_total)
    return_dict = {"labelData": labelData, "valueData": valueData}
    return jsonify(return_dict), 200

#------------get all records for the matching params---------#
@query_bp.route("/get_all", methods = ["GET"])
def get_all_entries():
    #THIS ROUTE NEEDS TESTING
    queryParam = request.args

    data = Eeo1_data.query.filter_by(**queryParam)

    response = [data_line.to_dict() for data_line in data]
    return jsonify(response), 200

#make a route that returns the list of companies #need to pull once
#returns a dictionary with keys that are companies and values that is a list of valid years? 

@query_bp.route("/company_years", methods = ["GET"])
def get_companies_and_years():
    """this returns a dictionary with companies as keys and values a list of valid years for that company. """
    #THIS ROUTE NEEDS TESTING
    company = Eeo1_data.company
    year = Eeo1_data.year
    company_years = db.session.query(company, year).group_by(company, year)
    response = {}

    for company, year in company_years:
        if company not in response.keys():
            response[company] = [year]
        else:
            response[company].append(year)
    for year_lst in response.values():
        year_lst.sort()
    #format this data better. 
    return jsonify(response), 200



