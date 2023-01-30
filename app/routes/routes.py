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
    if queryParam: #I'm not sure how to make it only filter by the ones that are included?
        
        company_query = queryParam.get('company', type=str) #you could put default = "amazon" in this 
        year_query = queryParam.get('year', type= int) #you could put default = 2021 in this
        #sortBy_query = queryParam.get('sortBy', type= str) #you could put default = "gender" in this #make this an enum? nah handle that on front end.

        data = Eeo1_data.query.filter_by(company = company_query, year = year_query).all()
        
    else:
        data = Eeo1_data.query.all()
    response = [data_line.to_dict() for data_line in data]
    # THE FOLLOWING DIDN'T WORK.
    # 
    # data = session.query(Eeo1_data_line.gender, func.sum(Eeo1_data_line.count_employees)).group_by(Eeo1_data_line.gender).all()
    # returns this query (it's not the right one): [SQL: SELECT eeo1_data_line.gender AS eeo1_data_line_gender, sum(eeo1_data_line.count_employees) AS sum_1 FROM eeo1_data_line GROUP BY eeo1_data_line.gender]
    return jsonify(response)

#for now, I'm going to try to make a different route

