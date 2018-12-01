from __future__ import unicode_literals
import frappe



def create_purchase_ledger_entry(items, submit=True):
    pl_list = [] 
    for item in items:
        purchase_ledger_entry = frappe.get_doc(item.parenttype, item.parent).get_purchase_ledger_entry(item, submit)
        frappe.get_doc(purchase_ledger_entry).insert()
        
        if purchase_ledger_entry['is_billing']:
            if purchase_ledger_entry['purchase_receipt']:
                frappe.get_doc("Purchase Receipt", purchase_ledger_entry['purchase_receipt']).update_billed_amt(item)
            if purchase_ledger_entry['purchase_order']:
                frappe.get_doc("Purchase Order", purchase_ledger_entry['purchase_order']).update_billed_amt(item)
        pl_list.append(purchase_ledger_entry)
    
    # set_qty(pl_list) 

def get_purchase_ledger_entry(item, submit, args):
    pl_dict = dict(
        doctype = 'Purchase Ledger Entry',
        item = item.item_code,
        qty = item.qty * (1 if submit else -1),
        amount = item.amount * (1 if submit else -1),
        material_request = None,
        purchase_order = None,
        purchase_order_item = None,
        purchase_receipt = None,
        purchase_receipt_item = None,
        purchase_invoice = None,
        is_request = 0,
        is_order = 0,
        is_receipt = 0,
        is_billing = 0)
    pl_dict.update(args)
    return pl_dict
