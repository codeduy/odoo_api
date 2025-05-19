from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import os
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path
from .odoo_connection import OdooConnection
from .data_importer import DataImporter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Odoo Data Import API",
    description="API để nhập liệu vào hệ thống Odoo ERP - CRM",
    version="1.0.0"
)

# Initialize Odoo connection
odoo = OdooConnection()
importer = DataImporter(odoo)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Trang chủ với hướng dẫn sử dụng API"""
    return """
    <html>
        <head>
            <title>Odoo Data Import API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #2c3e50; }
                .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Odoo CRM Data Import API</h1>
            <p>API để nhập liệu vào hệ thống Odoo ERP. Các endpoint có sẵn:</p>
            
            <div class="endpoint">
                <h3>Kiểm tra kết nối</h3>
                <p><code>GET /health</code></p>
            </div>
            
            <div class="endpoint">
                <h3>Nhập dữ liệu khách hàng</h3>
                <p><code>POST /import/contacts</code></p>
                <p>File Excel cần có các cột: name, email, phone, company_type, street, city, zip, country_id, is_company</p>
            </div>
            
            <div class="endpoint">
                <h3>Nhập dữ liệu Lead/Opportunity</h3>
                <p><code>POST /import/leads</code></p>
                <p>File Excel cần có các cột: name, contact_name, partner_id, email_from, phone, stage_id, expected_revenue, description</p>
            </div>
            
            <div class="endpoint">
                <h3>Nhập dữ liệu đơn hàng</h3>
                <p><code>POST /import/sales</code></p>
                <p>File Excel cần có các cột: partner_id, order_line (JSON format)</p>
            </div>
            
            <p>Để xem documentation đầy đủ và test API, truy cập <a href="/docs">/docs</a></p>
        </body>
    </html>
    """

@app.on_event("startup")
async def startup_event():
    """Connect to Odoo when the application starts"""
    logger.info("Starting up API server...")
    if not odoo.connect():
        logger.error("Failed to connect to Odoo server")
        raise Exception("Failed to connect to Odoo server")
    logger.info("Successfully connected to Odoo server")

@app.post("/import/{data_type}")
async def import_data(
    data_type: str,
    file: UploadFile = File(...),
    sheet_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Import data from Excel file into Odoo
    data_type can be: contacts, leads, or sales
    """
    logger.info(f"Received request to import {data_type}")
    
    if not file.filename.endswith(('.xls', '.xlsx')):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(400, "File must be an Excel file")
        
    # Save uploaded file temporarily
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / f"temp_{file.filename}"
    
    try:
        logger.info(f"Saving temporary file to {temp_path}")
        contents = await file.read()
        temp_path.write_bytes(contents)
            
        # Import data based on type
        if data_type == "contacts":
            record_ids = importer.import_contacts(str(temp_path), sheet_name)
            model = 'res.partner'
        elif data_type == "leads":
            record_ids = importer.import_leads(str(temp_path), sheet_name)
            model = 'crm.lead'
        elif data_type == "sales":
            record_ids = importer.import_sales_orders(str(temp_path), sheet_name)
            model = 'sale.order'
        else:
            logger.error(f"Unsupported data type: {data_type}")
            raise HTTPException(400, f"Unsupported data type: {data_type}. Use: contacts, leads, or sales")
            
        # Verify the import
        verified_records = importer.verify_import(model, record_ids)
        logger.info(f"Successfully imported {len(record_ids)} {data_type}")
        
        return {
            "message": f"Successfully imported {len(record_ids)} {data_type}",
            "record_ids": record_ids,
            "verified_records": verified_records
        }
        
    except Exception as e:
        logger.error(f"Import failed: {str(e)}")
        raise HTTPException(500, f"Import failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_path.exists():
            temp_path.unlink()
            
@app.get("/health")
async def health_check():
    """Check if the API and Odoo connection are working"""
    try:
        if not odoo.uid:
            if not odoo.connect():
                logger.error("Not connected to Odoo server")
                raise HTTPException(503, "Not connected to Odoo server")
        return {"status": "healthy", "odoo_connected": True}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(503, str(e))
