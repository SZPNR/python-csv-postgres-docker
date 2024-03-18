import pytest
from main import query_sales_report
from database import Database

@pytest.fixture
def setup_database():
    test_db = Database(dbname='database', user='postgres', password='password', host='db')
    test_db.connect()

    yield test_db

    test_db.close()

def test_sales_report_not_empty(setup_database):
    db = setup_database

    sales_report_result = query_sales_report(db)
    
    assert not sales_report_result.empty

def test_sales_report_columns(setup_database):
    db = setup_database
    
    sales_report_result = query_sales_report(db)
    
    expected_columns = ["category", "region", "month", "total_sales", "margin"]
    assert all(column in sales_report_result.columns for column in expected_columns)

def test_sales_report_months_count(setup_database):
    db = setup_database
    
    sales_report_result = query_sales_report(db)
    
    unique_months = sales_report_result["month"].unique()
    assert len(unique_months) == 12

def test_sales_report_no_null_values(setup_database):
    db = setup_database
    
    # Exécutez la requête de rapport de ventes
    sales_report_result = query_sales_report(db)
    
    relevant_columns = ["category", "region", "month", "total_sales", "margin"]
    for column in relevant_columns:
        assert not sales_report_result[column].isnull().any()

def test_sales_report_no_negative_total_sales(setup_database):
    db = setup_database
    
    sales_report_result = query_sales_report(db)
    
    assert (sales_report_result["total_sales"] >= 0).all()
