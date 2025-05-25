# Odoo Data Import API

This project provides an API for importing data into Odoo ERP from Excel files. It supports importing products, customers, and sales orders.

## Features

- Import data from Excel files into Odoo
- Support for products, customers, and sales orders
- Data validation and verification
- Simple REST API interface
- Automatic Excel file parsing
- Error handling and reporting

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Odoo connection:
Copy `.env.example` to `.env` and update with your Odoo settings:
```
ODOO_URL=http://your-odoo-server:8069
ODOO_DB=your-database  # Database name can be found at http://localhost:8069/web/database/manager
ODOO_USERNAME=your-username
ODOO_PASSWORD=your-password
```



3. Run the API:
```bash
uvicorn src.api:app --reload
```

## API Endpoints

### Health Check
```
GET /health
```
Checks if the API and Odoo connection are working.

### Import Data
```
POST /import/{data_type}
```
Import data from an Excel file. `data_type` can be:
- products
- contacts
- sales

Parameters:
- `file`: Excel file (required)
- `sheet_name`: Sheet name in Excel file (optional) - Leave empty to import all sheets

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 400: Invalid request (wrong file type, missing data)
- 500: Server error (Odoo connection issues, processing errors)

## Response Format

Successful import response:
```json
{
    "message": "Successfully imported X records",
    "record_ids": [1, 2, 3],
    "verified_records": [
        {
            "id": 1,
            "name": "Record name",
            "create_date": "2025-05-17 10:00:00"
        }
    ]
}
```
