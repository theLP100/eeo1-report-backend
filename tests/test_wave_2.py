#tests for the advanced query route.

from app.models.Eeo1_data import Eeo1_data
import pytest
import urllib #this will help me convert params to urls.

def test_adv_query_gender_no_saved_rows(client):
    query_params = {
        'company': 'Amazon',
        'year': 2021,
        'sortBy1[]': 'Exec/Sr. Officials & Mgrs',
        'sortBy1[]': "First/Mid Officials & Mgrs",
        'sortBy2': 'gender'
    }

    #parse params using urllib:
    param_url = urllib.parse.urlencode(query_params)

    response = client.get("/adv_query?" + param_url)
    response_body = response.get_json()

    assert len(response_body) == 2
    assert response_body == {'labelData': [], 'valueData': {}}
    

def test_adv_query_gender_4_saved_rows_1_job_cat(client, four_rows):
    query_params = {
        'company': 'Amazon',
        'year': 2021,
        'sortBy1[]': "First/Mid Officials & Mgrs",
        'sortBy2': 'gender'
    }

    #parse params using urllib:
    param_url = urllib.parse.urlencode(query_params)

    response = client.get("/adv_query?" + param_url)
    response_body = response.get_json()

    assert len(response_body) == 2
    assert response_body == {'labelData': ["First/Mid Officials & Mgrs"], 'valueData': {"Female": [2000], "Male": [5000]}}
    
#I had trouble making tests for multiple job cats (because the query_param dict could only hold one sortby1[])
#but I've verified in postman. 
#if extra time, add a test here.