# Copyright (c) 2021, Summayya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document




class JournalEntry(Document):
    def validate(self):
        set_total_debit_credit(self)

        if len(self.account_entries) < 2:
            frappe.throw("Entry is missing ! ")

        if self.total_credit != self.total_debit:
            frappe.throw("Total debit and Total credit must be equal !")
        for account in self.account_entries:
            if account.credit and account.debit:
                frappe.throw(
                    "You cannot credit and debit same account at the same time")

    def on_submit(self):
        create_gl_entry(self)

    def on_cancel(self):
        create_gl_entry(self, True)


def create_gl_entry(self, is_reverse=False):
    debit_accounts = []
    credit_accounts = []
    against_account = None
    for entry in self.account_entries:
        if entry.debit != 0:
            debit_accounts.append(entry.account)
        if entry.credit != 0:
            credit_accounts.append(entry.account)

    debit_accounts = ', '.join(str(account) for account in debit_accounts)
    credit_accounts = ', '.join(str(account) for account in credit_accounts)

    for entry in self.account_entries:
        debit, credit = entry.debit, entry.credit
        if is_reverse:
            debit, credit = entry.credit, entry.debit

        if entry.debit == 0:
            against_account = debit_accounts
        else:
            against_account = credit_accounts

        frappe.get_doc({
            "doctype": "GL Entry",
            "posting_date": self.posting_date,
            "company": self.company,
            "account": entry.account,
            "credit": credit,
            "debit": debit,
            "against_account": against_account,
            "voucher_type": "Journal Entry",
            "voucher_no": self.name,
        }).submit()


def set_total_debit_credit(self):
        self.total_debit = 0
        self.total_credit = 0
        self.total_debit = sum(account.debit for account in self.account_entries)
        self.total_credit = sum(account.credit for account in self.account_entries)