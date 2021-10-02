# Copyright (c) 2013, Summayya and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        columns, data = [], []
        return columns, data
    if filters:
        return get_columns(), get_data(filters)


def get_columns():
    columns = [
        {
            "label": _("GL Entry"),
            "fieldname": "gl_entry",
            "fieldtype": "Link",
            "options": "GL Entry",
            "hidden": 1,
            'width': 150
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            'width': 150
        },
        {
            "label": _("Account"),
            "fieldname": "account",
            "fieldtype": "Link",
            "options": "Account",
            'width': 120
        },
        {
            "label": _("Debit"),
            "fieldname": "debit",
            "fieldtype": "Float",
            'width': 120
        },
        {
            "label": _("Credit"),
            "fieldname": "credit",
            "fieldtype": "Float",
            'width': 120
        },
        {
            "label": _("Balance"),
            "fieldname": "balance",
            "fieldtype": "Currency",
            'width': 120
        },
        {
            "label": _("Against Account"),
            "fieldname": "against_account",
            "fieldtype": "Link",
            "options": "Account",
            'width': 120
        },
        {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "data",
            "width": 120
        },
        {
            "label": _("Voucher Number"),
            "fieldname": "voucher_no",
            "fieldtype": "data",
            "width": 150
        }
    ]
    return columns


def get_data(filter):
    filters = []
    balance = 0
    if filter.company:
        filters.append(f"company=\"{filter.company}\"")
    if(filter.account):
        filters.append(f"account=\"{filter.account}\"")
    if(filter.posting_date):
        filters.append(f"posting_date=\"{filter.posting_date}\"")

    filters = "{}".format(" and ".join(filters)) if filters else ""
    gl_entries = frappe.db.sql(f"select name, posting_date, account, debit, credit, against_account, voucher_type, voucher_no FROM `tabGL Entry` where {filters} order by account", as_dict=1)

    for entry in gl_entries:
        balance = balance - entry.credit
        balance = balance + entry.debit
        entry['balance'] = balance

    return gl_entries
