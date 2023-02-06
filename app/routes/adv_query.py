from flask import Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func

adv_query_bp = Blueprint("adv_query_bp", __name__, url_prefix = "/adv_query")


#-----------A double groupby query.  required params: company, year, sortBy1, sortBy2"------
#returns: labelData and valueData, organized alphabetically.
#I'm choosing to make this a separate query for now. there may be a better way to combine these later. 
@adv_query_bp.route("", methods = ["GET"])
def adv_query():
    #   THIS ROUTE NEEDS TESTING.
    #figure out what to do if they put the same field for both. 
    # write docstring with more details. 
    # LATER, make it DRY using helper functions.
    queryParam = request.args
    company_query = queryParam.get('company', type=str) 
    year_query = queryParam.get('year', type=int) 
    sortBy1_field = queryParam.get('sortBy1', type=str)
    sortBy2_field = queryParam.get('sortBy2', type=str)

    field_dict = {
        "race": Eeo1_data.race,
        "gender": Eeo1_data.gender,
        "job": Eeo1_data.job_category
    }

    try: 
        field1 = field_dict[sortBy1_field]
        field2 = field_dict[sortBy2_field]
        #add a check here to make sure that these fields aren't the same?
    except:
        response_str = f"Please enter two fields to sort by.  Enter a query param with key sortBy1 and value race, gender, or job.  Do the same for sortBy2."
        abort(make_response({"message": response_str}, 400))

    #the query:
    field_totals = db.session.query(field1, field2, 
        func.sum(Eeo1_data.count_employees)).filter_by(company=company_query,
        year = year_query).group_by(field1, field2).order_by(func.sum(Eeo1_data.count_employees).desc()).all()
        #previously it was .order_by(field2, field1)

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


