import pytest
from fastapi.testclient import TestClient
import os
from src.api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_import_products():
    # Create a test Excel file
    import pandas as pd
    test_data = {
        'name': ['Test Product 1', 'Test Product 2'],
        'list_price': [100, 200],
        'type': ['consu', 'consu']
    }
    df = pd.DataFrame(test_data)
    test_file = 'test_products.xlsx'
    df.to_excel(test_file, sheet_name='Products', index=False)
    
    try:
        # Test file upload
        with open(test_file, 'rb') as f:
            response = client.post(
                "/import/products",
                files={"file": ("test_products.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        assert response.status_code == 200
        result = response.json()
        assert "record_ids" in result
        assert len(result["record_ids"]) == 2
        assert "verified_records" in result
        
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
