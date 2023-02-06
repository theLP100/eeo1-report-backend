from flask import Flask, Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func

adv_query_bp = Blueprint("adv_query_bp", __name__, url_prefix = "/adv_query")


#-----------A double groupby query.  required params: company, year, sortBy1, sortBy2"------
#returns: labelData and valueData, organized alphabetically.
#new requirements: sortBy1 will always be job.  however! now, it will be a list of job categories.
@adv_query_bp.route("", methods = ["GET"])
def adv_query():
    """params: company, year, sortBy1, sortBy2.  sortBy1 is a list of job categories to display."""
    # LATER, make it DRY using helper functions.
    #job_categories = ['Exec/Sr. Officials & Mgrs','First/Mid Officials & Mgrs','Professionals','Technicians','Sales Workers','Administrative Support','Craft Workers','Operatives','Laborers & Helpers','Service Workers']

    queryParam = request.args
    company_query = queryParam.get('company', type=str) 
    year_query = queryParam.get('year', type=int) 
    job_cat_lst = queryParam.getlist('sortBy1[]')
    sortBy2_field = queryParam.get('sortBy2', type=str)

    field_dict = {
        "race": Eeo1_data.race,
        "gender": Eeo1_data.gender,
    }

    try: 
        field2 = field_dict[sortBy2_field]
    except:
        response_str = f"Please enter 'gender' or 'race' for sortBy2"
        abort(make_response({"message": response_str}, 400))

    #the query:
    field_totals = db.session.query(Eeo1_data.job_category, field2, 
        func.sum(Eeo1_data.count_employees)).filter(Eeo1_data.job_category.in_(job_cat_lst)).filter_by(company=company_query,year=year_query).group_by(Eeo1_data.job_category, field2).order_by(Eeo1_data.job_category, func.sum(Eeo1_data.count_employees).desc()).all()

    #setting up returns.
    labelData = []
    valueData = {}
    for field1_label, field2_label, count_employees_total in field_totals:
        #get a list of field1_labels with no repeats:
        if field1_label not in labelData:
            labelData.append(field1_label)
        #valueData is a dictionary with keys = the values of field2, 
        # and values = count employees in that category.
        if field2_label not in valueData.keys():
            valueData[field2_label] = [count_employees_total]
        else:
            valueData[field2_label].append(count_employees_total)
    
    return_obj = {"labelData": labelData, "valueData": valueData}
    return jsonify(return_obj), 200


