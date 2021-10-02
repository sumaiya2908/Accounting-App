# Copyright (c) 2021, Summayya and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

from ..gl_entry.gl_entry import create_gl_entry


class PurchaseInvoice(Document):
    def validate(self):
        self.set_status()
        self.set_total_amount()


    def set_total_amount(self):
        self.amount = 0
        self.total_quantity = 0
        self.amount = sum(item.amount for item in self.item)
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
        create_gl_entry(self, "Purchase Invoice",
                        self.credit_account, self.debit_account)

    def on_cancel(self):
        create_gl_entry(self, "Purchase Invoice",
                        self.debit_account, self.credit_account)