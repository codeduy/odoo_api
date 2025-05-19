import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import json
import os
from odoo_connection import OdooConnection

class DataImporter:
    def __init__(self, odoo_connection: OdooConnection):
        self.odoo = odoo_connection
        
    def clean_record(self, record: Dict) -> Dict:
        """Clean up record data before importing"""
        # Remove NaN values
        clean_data = {}
        for key, value in record.items():
            if pd.isna(value):
                continue
            elif isinstance(value, np.bool_):
                clean_data[key] = bool(value)
            elif isinstance(value, np.int64):
                clean_data[key] = int(value)
            elif isinstance(value, np.float64):
                clean_data[key] = float(value)
            elif isinstance(value, str) and value.strip() == "":
                continue
            else:
                clean_data[key] = value
        return clean_data

    def import_excel_data(self, file_path: str, sheet_name: Optional[str] = None, model: str = "", process_func = None) -> List[int]:
        """
        Import data from Excel file into Odoo
        process_func: Optional function to process records before import
        """
        try:
            # Read Excel file
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                dfs = {sheet_name: df}
            else:
                # Read all sheets
                dfs = pd.read_excel(file_path, sheet_name=None)
            
            all_created_ids = []
            
            # Process each sheet
            for sheet_name, df in dfs.items():
                print(f"Processing sheet: {sheet_name}")
                # Convert DataFrame to list of dictionaries and clean data
                records = df.replace({np.nan: None}).to_dict("records")
                
                # Create records in Odoo
                for record in records:
                    # Clean up record
                    clean_record = self.clean_record(record)
                    
                    # Process record if needed
                    if process_func:
                        clean_record = process_func(clean_record)
                    
                    if clean_record:  # Only create if record is not empty
                        try:
                            record_id = self.odoo.create_record(model, clean_record)
                            all_created_ids.append(record_id)
                            print(f"Created record with ID: {record_id}")
                        except Exception as e:
                            print(f"Error creating record: {clean_record}")
                            print(f"Error details: {str(e)}")
                
            return all_created_ids
            
        except Exception as e:
            print(f"Error importing data: {str(e)}")
            raise
            
    def process_order_line(self, record: Dict) -> Dict:
        """Process order_line field from string to list"""
        if "order_line" in record and isinstance(record["order_line"], str):
            try:
                record["order_line"] = json.loads(record["order_line"])
            except json.JSONDecodeError:
                raise ValueError("Invalid order_line JSON format")
        return record
    
    def import_contacts(self, file_path: str, sheet_name: Optional[str] = None) -> List[int]:
        """Import contacts/customers from Excel file"""
        return self.import_excel_data(file_path, sheet_name, "res.partner")
        
    def import_leads(self, file_path: str, sheet_name: Optional[str] = None) -> List[int]:
        """Import leads/opportunities from Excel file"""
        return self.import_excel_data(file_path, sheet_name, "crm.lead")
        
    def import_sales_orders(self, file_path: str, sheet_name: Optional[str] = None) -> List[int]:
        """Import sales orders from Excel file"""
        return self.import_excel_data(
            file_path, 
            sheet_name, 
            "sale.order",
            process_func=self.process_order_line
        )
        
    def verify_import(self, model: str, record_ids: List[int]) -> List[Dict]:
        """Verify that records were correctly imported"""
        fields_map = {
            "res.partner": ["id", "name", "email", "phone", "company_type"],
            "crm.lead": ["id", "name", "contact_name", "email_from", "stage_id"],
            "sale.order": ["id", "name", "partner_id", "amount_total"]
        }
        
        return self.odoo.search_read(
            model,
            [("id", "in", record_ids)],
            fields_map.get(model, ["id", "name", "create_date"])
        )