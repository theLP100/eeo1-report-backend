from flask import Blueprint, jsonify
from app.models.Eeo1_data_line import Eeo1_data_line

query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

@query_bp.route("", methods = ["GET"])
def read_all_data():
    #this should return all the data we have.
    #add a query option for single queries.
    data = Eeo1_data_line.query.all()
    response = [data_line.to_dict() for data_line in data]
    return jsonify(response)