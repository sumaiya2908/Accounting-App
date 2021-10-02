# Copyright (c) 2021, Summayya and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from ..gl_entry.gl_entry import create_gl_entry

class PaymentEntry(Document):
    def on_submit(self):
        create_gl_entry(self, "Payment Entry", self.pay_from_account, self.pay_to_account)

    def on_cancel(self):
        create_gl_entry(self, "Payment Entry", self.pay_to_account, self.pay_from_account)
