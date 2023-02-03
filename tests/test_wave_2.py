#tests for the advanced query route.

from app.models.Eeo1_data import Eeo1_data
import pytest
import urllib #this will help me convert params to urls.

def test_adv_query_gender_no_saved_rows(client):
    query_params = {
        'company': 'Amazon',
        'year': 2021,
        'sortBy1': 'gender',
        'sortBy2': 'job'
    }

    #parse params using urllib:
    param_url = urllib.parse.urlencode(query_params)

    response = client.get("/adv_query?" + param_url)
    response_body = response.get_json()

    assert len(response_body) == 2
    assert response_body == {'labelData': [], 'valueData': {}}
    

def test_adv_query_gender_2_saved_rows(client, two_rows):
    query_params = {
        'company': 'Amazon',
        'year': 2021,
        'sortBy1': 'gender',
        'sortBy2': 'job'
    }

    #parse params using urllib:
    param_url = urllib.parse.urlencode(query_params)

    response = client.get("/adv_query?" + param_url)
    response_body = response.get_json()

    assert len(response_body) == 2
    assert response_body == {'labelData': ['Male'], 'valueData': {"Exec/Sr. Officials & Mgrs": [100], "First/Mid Officials & Mgrs": [5000]}}
    