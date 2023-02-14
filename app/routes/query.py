from flask import Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

#-------a single group by query. required params: company, year, sortBy--------#
@query_bp.route("", methods = ["GET"]) 
def query():
    """takes in params: company (str), year (int), sortBy ['race', 'gender', or 'job']
    It returns the count of employees in each of the categories for your given sortBy field, filtered by the given company and year, in the following format:
    returns {'labelData': [the names of the labels], 'valueData': [the values matching those labels in the same order]}"""
    #organizing queries: 
    queryParam = request.args
    company_query = queryParam.get('company', type=str) 
    year_query = queryParam.get('year', type=int) 
    sortBy_field = queryParam.get('sortBy', type=str)
    
    field_dict = {
        "race": Eeo1_data.race,
        "gender": Eeo1_data.gender,
        "job": Eeo1_data.job_category
    }
    try: field = field_dict[sortBy_field]
    except:
        response_str = f"Please enter a field to sort by.  Enter a query param with key sortBy and value race, gender, or job."
        abort(make_response({"message": response_str}, 400))

    #the query
    field_totals = db.session.query(field, 
        func.sum(Eeo1_data.count_employees)).filter_by(company=company_query,
        year=year_query).group_by(field).all()

    #setting up returns in the form we want.
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
    queryParam = request.args

    data = Eeo1_data.query.filter_by(**queryParam)

    response = [data_line.to_dict() for data_line in data]
    return jsonify(response), 200

#---------------Returns valid years and jobs for companies, and total employees per company year ------#
@query_bp.route("/company_years_jobs", methods = ["GET"])
def get_companies_and_years():
    """this returns a dictionary with companies as keys 
    and values a dict, containing 'years': list of valid years, 
    'jobs': list of jobs with non-zero employees,
    and 'totalEmployees': dict of year: count_employees (total) for that year."""
    company = Eeo1_data.company
    year = Eeo1_data.year
    job = Eeo1_data.job_category
    company_years = db.session.query(company, year, func.sum(Eeo1_data.count_employees)).group_by(company, year)
    company_jobs = db.session.query(company, job, func.sum(Eeo1_data.count_employees)).group_by(company, job).all()
    
    response = {}
    #populate the 'years' list and 'totalEmployees' dict
    for company, year, totalEmployees in company_years:
        if company not in response.keys():
            response[company] = {'years': [year], 'totalEmployees': {year: totalEmployees}}
        else:
            response[company]['years'].append(year)
            response[company]['totalEmployees'][year]=totalEmployees
    
    #populate the 'jobs' list
    for company, job, count_employees_total in company_jobs:
        if count_employees_total > 0:
            if 'jobs' not in response[company].keys():
                response[company]['jobs'] = [job]
            else:
                response[company]['jobs'].append(job)
    
    for company_dict in response.values():
        company_dict['years'].sort()
        company_dict['jobs'].sort()

    return jsonify(response), 200



