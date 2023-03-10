from flask import Flask, Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func

adv_query_bp = Blueprint("adv_query_bp", __name__, url_prefix = "/adv_query")


#-----------A double groupby query.  required params: company, year, sortBy1, sortBy2"------
#returns: labelData and valueData, organized alphabetically.
@adv_query_bp.route("", methods = ["GET"])
def adv_query():
    """params: company, year, sortBy1 (which is a list of job categories), sortBy2 (either 'race' or 'gender').  
    year will be either an int or a string "all".  if year is "all", job category will only be one job category.
    returns labelData and valueData, where value data is the count employees matching the label in the corresponding list position."""
    
    queryParam = request.args
    company_query = queryParam.get('company', type=str) 
    year_query = queryParam.get('year') 
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

    #if year is "all", returns are different:
    if year_query == "all":
        #   THIS PART OF THE CODE NEEDS TESTING.  GIVEN: YEARS AND ONE JOB_CAT, RETURN BREAKDOWN BY RACE OR GENDER OVER THOSE YEARS.
        field_totals = db.session.query(Eeo1_data.year, field2, 
            func.sum(Eeo1_data.count_employees)).filter(Eeo1_data.job_category.in_(job_cat_lst)).filter_by(company=company_query).group_by(Eeo1_data.year, field2).order_by(Eeo1_data.year, field2, func.sum(Eeo1_data.count_employees).desc()).all()
        #set up returns:
        labelData = []
        valueData = {}
        for year, field2_label, count_employees_total in field_totals:
            if year not in labelData:
                labelData.append(year)
            if field2_label not in valueData.keys():
                valueData[field2_label] = [count_employees_total]
            else:
                valueData[field2_label].append(count_employees_total)
            

    else:
        field_totals = db.session.query(Eeo1_data.job_category, field2, 
            func.sum(Eeo1_data.count_employees)).filter(Eeo1_data.job_category.in_(job_cat_lst)).filter_by(company=company_query,year=year_query).group_by(Eeo1_data.job_category, field2).order_by(func.sum(Eeo1_data.count_employees).desc()).all()

        #record the order of the list of job categories.
        job_cat_order = {}
        for ix, job_cat in enumerate(job_cat_lst):
            job_cat_order[job_cat] = ix
        #save the number of job_cats:
        num_job_cats = len(job_cat_lst)
        
        #setting up returns.
        if len(field_totals) == 0:
            labelData = []
        else:
            labelData = [None]*num_job_cats
        valueData = {}
        for job_cat_label, field2_label, count_employees_total in field_totals:
            #valueData is a dictionary with keys = the values of field2 (eg. 'Female' and 'Male')
            # and values = count employees in that category.
            #figure out what index to put it in the list.
            index = job_cat_order[job_cat_label]
            if job_cat_label in job_cat_lst:
                labelData[index] = job_cat_label

            #put the field2 lables in as keys to the value data dictionary:
            if field2_label not in valueData.keys():
                valueData[field2_label] = [None] * num_job_cats
            
            valueData[field2_label][index] = count_employees_total
        
    return_obj = {"labelData": labelData, "valueData": valueData}
    return jsonify(return_obj), 200


