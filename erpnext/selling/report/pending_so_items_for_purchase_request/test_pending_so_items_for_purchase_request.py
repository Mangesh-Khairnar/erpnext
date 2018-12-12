# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import frappe.defaults
import unittest
from frappe.utils import nowdate, add_months
from erpnext.selling.report.pending_so_items_for_purchase_request.pending_so_items_for_purchase_request\
     import execute
from erpnext.selling.doctype.sales_order.sales_order import make_material_request
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order


class TestPendingSOItemsForPurchaseRequest(unittest.TestCase): 
    def test_result_for_partial_material_request(self):
        so = make_sales_order()
        mr=make_material_request(so.name)
        mr.items[0].qty = 4
        mr.schedule_date = add_months(nowdate(),1)
        mr.submit()
        report = execute()
        self.assertEqual((so.items[0].qty - mr.items[0].qty), report[1][0]['pending_qty'])
	
    def test_result_for_so_item(self):
        so = make_sales_order()
        report = execute()
        self.assertEqual(so.items[0].qty, report[1][0]['pending_qty'])

    def tearDown(self):
        frappe.db.sql("""delete from `TabSales Order`""")
        frappe.db.sql("""delete from `TabMaterial Request`""")
        


