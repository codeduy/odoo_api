import requests
import pandas as pd
import os

# Create test data
test_data = {
    'name': ['Test Product 1', 'Test Product 2'],
    'list_price': [100, 200],
    'type': ['consu', 'consu']
}
df = pd.DataFrame(test_data)

# Save test file
test_file = 'test_products.xlsx'
df.to_excel(test_file, sheet_name='Products', index=False)

try:
    # Test health endpoint
    health_response = requests.get('http://localhost:8000/health')
    print(f"Health check response: {health_response.json()}")

    # Test import endpoint
    with open(test_file, 'rb') as f:
        files = {'file': ('test_products.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        response = requests.post('http://localhost:8000/import/products', files=files)
        print(f"\nImport response: {response.json()}")

finally:
    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)
