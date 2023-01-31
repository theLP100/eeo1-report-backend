from flask import Blueprint, jsonify, request
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

@query_bp.route("", methods = ["GET"])
def query():
    #THIS ROUTE NEEDS TESTING
    queryParam = request.args
    #there will always be a company and year, so you can just use those explicitly.
    #LP: MAKE THIS GENERALIZABLE FOR THE GROUP_BY FIELD (replace gender with the field and make that work.)
    #(double check that the **queryParams works when one of the params is group by.) (you'll need to separate the args)
    gender_totals = db.session.query(Eeo1_data.gender, func.sum(Eeo1_data.count_employees)).filter(**queryParam).group_by(Eeo1_data.gender).all()
    return_dict = {}
    for gender, count_employees_total in gender_totals:
        return_dict[gender] = count_employees_total
    return jsonify(return_dict)


@query_bp.route("/get_all", methods = ["GET"])
def get_all_entries():
    #THIS ROUTE NEEDS TESTING
    queryParam = request.args

    data = Eeo1_data.query.filter_by(**queryParam)

    response = [data_line.to_dict() for data_line in data]
    return jsonify(response)


