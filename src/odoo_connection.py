import xmlrpc.client
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class OdooConnection:
    def __init__(self):
        # Load configuration from environment variables
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'odoo')
        self.username = os.getenv('ODOO_USERNAME', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', 'admin')
        
        # Initialize connection
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = None
        self.uid = None
        
    def connect(self) -> bool:
        """Establish connection with Odoo server"""
        try:
            # Authenticate and get user ID
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if not self.uid:
                return False
            
            # Set up models endpoint
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
            
    def create_record(self, model: str, values: Dict[str, Any]) -> int:
        """Create a new record in Odoo"""
        if not self.uid or not self.models:
            raise ConnectionError("Not connected to Odoo")
            
        try:
            record_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                model, 'create',
                [values]
            )
            return record_id
        except Exception as e:
            print(f"Error creating record: {str(e)}")
            raise
            
    def search_read(self, model: str, domain: list, fields: list) -> list:
        """Search and read records from Odoo"""
        if not self.uid or not self.models:
            raise ConnectionError("Not connected to Odoo")
            
        try:
            records = self.models.execute_kw(
                self.db, self.uid, self.password,
                model, 'search_read',
                [domain],
                {'fields': fields}
            )
            return records
        except Exception as e:
            print(f"Error searching records: {str(e)}")
            raise
