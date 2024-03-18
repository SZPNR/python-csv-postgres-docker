import pytest
from main import query_customer_analysis
from database import Database

@pytest.fixture
def setup_database():
    test_db = Database(dbname='database', user='postgres', password='password', host='db')
    test_db.connect()

    yield test_db

    test_db.close()

def test_customer_analysis_not_empty(setup_database):
    db = setup_database
    
    customer_analysis_result = query_customer_analysis(db)
    
    assert not customer_analysis_result.empty

def test_customer_analysis_columns(setup_database):
    db = setup_database

    customer_analysis_result = query_customer_analysis(db)
    
    expected_columns = ["customer_id", "region", "favorite_category", "total_spent", "favorite_product", "purchase_frequency"]
    assert all(column in customer_analysis_result.columns for column in expected_columns)

def test_customer_analysis_no_null_values(setup_database):
    db = setup_database
    
    customer_analysis_result = query_customer_analysis(db)
    
    relevant_columns = ["customer_id", "region", "favorite_category", "total_spent", "favorite_product", "purchase_frequency"]
    for column in relevant_columns:
        assert not customer_analysis_result[column].isnull().any()

def test_customer_analysis_no_zero_total_spent(setup_database):
    db = setup_database
    
    customer_analysis_result = query_customer_analysis(db)
    
    assert (customer_analysis_result["total_spent"] != 0).all()

def test_customer_analysis_purchase_frequency_non_negative(setup_database):
    db = setup_database
    
    customer_analysis_result = query_customer_analysis(db)
    
    assert (customer_analysis_result["purchase_frequency"] >= 0).all()

def test_customer_analysis_row_count(setup_database):
    db = setup_database
    
    customer_analysis_result = query_customer_analysis(db)
    
    customers_count_query = "SELECT COUNT(*) FROM customers;"
    customers_count = db.execute_query(customers_count_query).iloc[0, 0]
    
    assert len(customer_analysis_result) == customers_count
