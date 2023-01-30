from flask import Blueprint, jsonify, request
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func

# TRYING - DOESN'T WORK YET
# from sqlalchemy import create_engine
# engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/eeo1_db")
# session = Session(bind=engine)


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

@query_bp.route("", methods = ["GET"])
def query():
    #THIS ROUTE NEEDS TESTING
    gender_totals = db.session.query(Eeo1_data.race, func.sum(Eeo1_data.count_employees)).filter_by(**queryParam).group_by(Eeo1_data.race).all()
    return_dict = {}
    for gender, count_employees_total in gender_totals:
        return_dict[gender] = count_employees_total
    return jsonify(return_dict)

