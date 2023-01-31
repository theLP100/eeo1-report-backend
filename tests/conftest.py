import pytest
from app import create_app
from app.models.Eeo1_data import Eeo1_data
from app import db
from flask.signals import request_finished

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# @pytest.fixture
# def two_rows(app):
#     new_row1 = Eeo1_data(
#         company= "Amazon",
#         count_employees= 100,
#         gender= "Male",
#         id= 0,
#         job_category= "Exec/Sr. Officials & Mgrs",
#         race="Hispanic or Latino",
#         year= 2021)
#     new_row2 = Eeo1_data(
#         company= "Amazon",
#         count_employees= 5000,
#         gender= "Male",
#         id= 1,
#         job_category= "First/Mid Officials & Mgrs",
#         race="Hispanic or Latino",
#         year= 2021)
#     db.session.add_all([new_row1, new_row2])
#     db.session.commit()