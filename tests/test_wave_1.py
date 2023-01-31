#this tests the routes /query , /query/get_all, /query/company_years ;

from app.models.Eeo1_data import Eeo1_data
import pytest

def test_dummy(client):
    assert True

def test_get_all_no_saved_rows(client):
    response = client.get("/query/get_all")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_two_saved_rows(client, two_rows):
    response = client.get("/query/get_all")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
    {
        "company": "Amazon",
        "count_employees": 100,
        "gender": "Male",
        "id": 0,
        "job_category": "Exec/Sr. Officials & Mgrs",
        "race": "Hispanic or Latino",
        "year": 2021
    },
    {
        "company": "Amazon",
        "count_employees": 5000,
        "gender": "Male",
        "id": 1,
        "job_category": "First/Mid Officials & Mgrs",
        "race": "Hispanic or Latino",
        "year": 2021
    }]