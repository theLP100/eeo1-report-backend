from flask import Blueprint, jsonify
from app.models.Eeo1_data import Eeo1_data
from sqlalchemy import func
from sqlalchemy.orm import Session

# TRYING - DOESN'T WORK YET
# from sqlalchemy import create_engine
# engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/eeo1_db")
# session = Session(bind=engine)


query_bp = Blueprint("query_bp" , __name__, url_prefix = "/query")

@query_bp.route("", methods = ["GET"])
def read_all_data():
    #this should return all the data we have.
    #add a query option for single queries.
    #THIS ROUTE NEEDS TESTING
    data = Eeo1_data.query.all()
    response = [data_line.to_dict() for data_line in data]
    # THE FOLLOWING DIDN'T WORK.
    # 
    # data = session.query(Eeo1_data_line.gender, func.sum(Eeo1_data_line.count_employees)).group_by(Eeo1_data_line.gender).all()
    # returns this query (it's not the right one): [SQL: SELECT eeo1_data_line.gender AS eeo1_data_line_gender, sum(eeo1_data_line.count_employees) AS sum_1 FROM eeo1_data_line GROUP BY eeo1_data_line.gender]
    return jsonify(response)

