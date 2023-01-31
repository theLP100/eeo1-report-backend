#this tests the routes /query , /query/get_all, /query/company_years ;

from app.models.Eeo1_data import Eeo1_data
import pytest

def test_dummy(client):
    assert True

def test_get_all_no_saved_rows(client):
    response = client.get("/query")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []