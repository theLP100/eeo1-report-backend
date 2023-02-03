#this tests the routes /query , /query/get_all, /query/company_years ;

from app.models.Eeo1_data import Eeo1_data
import pytest
import urllib #this will help me convert params to urls.

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

#I'm not going to test or provide error messages for routes that have incorrect query params, 
#because front end is ensuring that they only use the correct params.  check with front end about this.

def test_company_years_no_saved_rows(client):
    response = client.get("/query/company_years")
    response_body = response.get_json()

    assert response_body == {}
    assert response.status_code == 200

def test_company_years_2_saved_rows(client, two_rows):
    response = client.get("/query/company_years")
    response_body = response.get_json()

    assert response_body == {'Amazon': [2021]}
    assert response.status_code == 200

def test_query_gender_no_saved_rows(client):
    query_params = {
        'company': 'Amazon',
        'year': 2021,
        'sortBy': 'gender'
    }

    #parse params using urllib:
    param_url = urllib.parse.urlencode(query_params)

    response = client.get("/query?" + param_url)
    response_body = response.get_json()

    assert len(response_body) == 2
    assert response_body == {'labelData': [], 'valueData': []}
    


def test_query_gender_2_saved_rows(client, two_rows):
    query_params = {
        'company': 'Amazon',
        'year': 2021,
        'sortBy': 'gender'
    }

    #parse params using urllib:
    param_url = urllib.parse.urlencode(query_params)

    response = client.get("/query?" + param_url)
    response_body = response.get_json()

    assert len(response_body) == 2
    assert response_body == {'labelData': ['Male'], 'valueData': [5100]}
    