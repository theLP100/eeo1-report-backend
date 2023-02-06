from flask import Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

#-------a single group by query. required params: company, year, sortBy--------#
@query_bp.route("", methods = ["GET"]) 
def query():
    #THIS ROUTE NEEDS TESTING
    #make helper functions for this to make it read more clearly and have only one job per function?
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

    # trying to get it alphabetically: 
    # field_totals = db.session.query(field, 
    #     func.sum(Eeo1_data.count_employees)).filter_by(company=company_query,
    #     year=year_query).group_by(field).order_by(func.sum(Eeo1_data.count_employees).desc()).all()



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


#----the following two may be better suited to be their own endpoint, organization-wise----
@query_bp.route("/company_years_jobs", methods = ["GET"])
def get_companies_and_years():
    #TESTING NEEDS TO BE UPDATED FOR THIS.
    """this returns a dictionary with companies as keys 
    and values a list of valid years for that company. """
    company = Eeo1_data.company
    year = Eeo1_data.year
    job = Eeo1_data.job_category
    company_years = db.session.query(company, year).group_by(company, year)
    company_jobs = db.session.query(company, job, func.sum(Eeo1_data.count_employees)).group_by(company, job).all()
    
    response = {}
    #populate the 'years' list.
    for company, year in company_years:
        if company not in response.keys():
            response[company] = {'years': [year]}
        else:
            response[company]['years'].append(year)
    
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

# @query_bp.route("/company_jobs", methods = ["GET"])
# def get_companies_job_categories():
#     #THIS ROUTE NEEDS TESTING
#     # job_categories = ['Exec/Sr. Officials & Mgrs','First/Mid Officials & Mgrs','Professionals','Technicians','Sales Workers','Administrative Support','Craft Workers','Operatives','Laborers & Helpers','Service Workers']
#     company = Eeo1_data.company
#     job = Eeo1_data.job_category

#     company_jobs = db.session.query(company, job, func.sum(Eeo1_data.count_employees)).group_by(company, job).all()
#     response = {}
    
#     for company, job, count_employees_total in company_jobs:
#         if count_employees_total > 0:
#             if company not in response.keys():
#                 response[company] = [job]
#             else:
#                 response[company].append(job)
#         for job_lst in response.values():
#             job_lst.sort()
        
#     return jsonify(response), 200


