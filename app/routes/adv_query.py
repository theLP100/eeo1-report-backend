from flask import Blueprint, jsonify, request, abort, make_response
from app.models.Eeo1_data import Eeo1_data
from app import db
from sqlalchemy import func

adv_query_bp = Blueprint("adv_query_bp", __name__, url_prefix = "/adv_query")


#-----------A double groupby query.  required params: company, year, sortBy1, sortBy2"
#I'm choosing to make this a separate query for now. there may be a better way to combine these later. 
@adv_query_bp.route("", method = ["GET"])
def adv_query():
    #   THIS ROUTE NEEDS TESTING.
    pass
