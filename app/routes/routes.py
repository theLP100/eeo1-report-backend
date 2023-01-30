from flask import Blueprint, jsonify, request
from app.models.Eeo1_data import Eeo1_data
from sqlalchemy import func
from sqlalchemy.orm import Session

# TRYING - DOESN'T WORK YET
# from sqlalchemy import create_engine
# engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/eeo1_db")
# session = Session(bind=engine)


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

@query_bp.route("", methods = ["GET"])
def query():
    #THIS ROUTE NEEDS TESTING
    queryParam = request.args

    data = Eeo1_data.query.filter_by(**queryParam)

    response = [data_line.to_dict() for data_line in data]
    return jsonify(response)

#for now, I'm going to try to make a different route

