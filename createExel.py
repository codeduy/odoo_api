
import pandas as pd

# 1. Contacts/Customers data
contacts_data = {
    # Thông tin cơ bản
    'name': ['Công ty TNHH ABC', 'Nguyễn Văn A', 'Công ty CP XYZ'],
    'company_type': ['company', 'person', 'company'],
    'is_company': [True, False, True],
    'vat': ['0123456789', '', '0987654321'],  # Mã số thuế
    
    # Thông tin liên hệ
    'phone': ['0901234567', '0912345678', '0923456789'],
    'mobile': ['0909123456', '0918234567', '0927345678'],
    'email': ['contact@abc.com', 'nguyenvana@email.com', 'info@xyz.com'],
    'website': ['https://abc.com.vn', '', 'https://xyz.com.vn'],
    
    # Địa chỉ
    'street': ['123 Lê Lợi', '45 Nguyễn Huệ', '789 Đồng Khởi'],
    'street2': ['Phường Bến Nghé', 'Phường Bến Thành', 'Phường Đa Kao'],
    'city': ['TP.HCM', 'Hà Nội', 'Đà Nẵng'],
    'state_id': [1, 2, 3],  # ID của tỉnh/thành phố
    'zip': ['70000', '10000', '50000'],
    'country_id': [241, 241, 241],  # 241 là ID của Việt Nam trong Odoo
    
    # Tags & Phân loại
    'category_id': [[1], [2], [1,2]],  # Tags (B2B, VIP, etc.)
    'comment': ['Khách hàng tiềm năng', 'Khách hàng cá nhân', 'Đối tác chiến lược'],
    'user_id': [1, 1, 1],  # Người phụ trách (salesperson)
}
df_contacts = pd.DataFrame(contacts_data)
df_contacts.to_excel('sample_contacts.xlsx', sheet_name='Contacts', index=False)

# 2. Leads/Opportunities data
leads_data = {
    'name': ['Dự án phần mềm ABC', 'Cơ hội bán hàng XYZ', 'Khách hàng tiềm năng 123'],
    'contact_name': ['Trần Văn B', 'Lê Thị C', 'Phạm Văn D'],
    'partner_id': [1, 2, 3],  # IDs từ contacts đã tạo
    'email_from': ['tranb@email.com', 'lec@email.com', 'phamd@email.com'],
    'phone': ['0934567890', '0945678901', '0956789012'],
    'stage_id': [1, 2, 1],  # 1: New, 2: Qualified
    'expected_revenue': [100000000, 50000000, 75000000],
    'description': ['Dự án triển khai phần mềm quản lý', 'Cơ hội cung cấp giải pháp', 'Khách hàng cần tư vấn']
}
df_leads = pd.DataFrame(leads_data)
df_leads.to_excel('sample_leads.xlsx', sheet_name='Leads', index=False)

# 3. Sales Orders data
orders_data = {
    'partner_id': [1, 2, 3],  # IDs từ contacts đã tạo
    'order_line': [
        '[{\"product_id\": 1, \"product_uom_qty\": 2, \"price_unit\": 1000000}]',
        '[{\"product_id\": 2, \"product_uom_qty\": 1, \"price_unit\": 2000000}]',
        '[{\"product_id\": 1, \"product_uom_qty\": 3, \"price_unit\": 1000000}]'
    ]
}
df_orders = pd.DataFrame(orders_data)
df_orders.to_excel('sample_orders.xlsx', sheet_name='Orders', index=False)

print('Created sample Excel files successfully!')
