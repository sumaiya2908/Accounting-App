# Copyright (c) 2021, Summayya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
import json
from ..gl_entry.gl_entry import create_gl_entry

class SalesInvoice(Document):

    def validate(self):
        self.set_status()
        self.set_total_amount()


    def set_total_amount(self):
        self.amount = 0
        self.amount = sum(flt(item.amount, 3) for item in self.item)
        self.total_quantity = 0
        self.total_quantity = sum(item.quantity for item in self.item)


    def set_status(self):
        '''
        Draft: 0
        Submitted: 1, Paid or Unpaid or Overdue
        Cancelled: 2
        '''
        if self.is_new():
            if self.get('amended_form'):
                self.status = 'Draft'
            return

        if self.docstatus == 1:
            self.status = 'Unpaid'


    def on_submit(self):
        create_gl_entry(self, 'Sales Invoice',
                        self.credit_account, self.debit_account)

    def on_cancel(self):
        create_gl_entry(self, 'Sales Invoice',
                        self.debit_account, self.credit_account)

@frappe.whitelist(allow_guest=True)
def generate_sales_invoice(data, company):  
    data = json.loads(data)
    items = []
    for item in data:
        items.append(frappe._dict(
			{"item_name": item['name'], "quantity": item['quantity'], "rate": item['price'], "amount": item['total_price']}
		))
    doc = frappe.get_doc({
        'doctype': 'Sales Invoice',
        'customer': 'Ecom customer',
        'company': company,
        'item': items,
        'debit_account': 'Debitors - GE',
        'credit_account': 'Sales - GE'
    })
 

    doc.submit()
    return doc.name
