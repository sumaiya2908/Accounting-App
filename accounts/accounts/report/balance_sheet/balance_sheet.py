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


def get_data(filters):

    parent_accounts = frappe.get_all('Account', fields=['name as account', 'root_type'], filters={
                                     'company': filters.get('company'), 'is_group': 1}, order_by='name')
    child_accounts = frappe.get_all('Account', fields=['name as account', 'parent_account', 'root_type'], filters={
                                    'company': filters.get('company'), 'is_group': 0}, order_by='parent_account')
    
    return get_accounts_with_desc(parent_accounts, child_accounts)


def get_columns():
    columns = [{
        "fieldname": "account",
        "label": _("Account"),
        "fieldtype": "Link",
        "options": "Account",
        "width": 300
    }, {
        "fieldname": "balance",
        "label": _("Balance"),
        "fieldtype": "Currency",
        "width": 300
    }]

    return columns



def get_accounts_with_desc(parent_accounts, child_accounts):
    accounts = []
    balance = 0
    account_in = ['Assest', 'Liability']
    parent_credit_balance = parent_debit_balance = child_credit_balance = child_debit_balance = 0
    for account in parent_accounts:
        if(account['root_type'] in account_in):
            account['indent'] = 0.0
            accounts.append(account)
            for child_account in child_accounts:
                if(child_account['parent_account'] == account['account'] and child_account['root_type'] in account_in):
                    gl_entry = frappe.get_all('GL Entry', fields=[
                        'name as account', 'debit', 'credit'], filters={'account': child_account['account']})
                    for entry in gl_entry:
                        child_credit_balance += entry.credit
                        child_debit_balance += entry.debit

                    child_account['indent'] = 1.0
                    if child_account['root_type'] == 'Assest':
                        child_account['balance'] = child_debit_balance - child_credit_balance
                    if child_account['root_type'] == 'Liability':
                        child_account['balance'] = child_credit_balance - child_debit_balance
                    accounts.append(child_account)
                    parent_credit_balance += child_credit_balance
                    parent_debit_balance += child_debit_balance
                    child_credit_balance = child_debit_balance = 0

            if account['root_type'] == 'Assest':
                account['balance'] = parent_debit_balance - parent_credit_balance
                accounts.append(["Total (Debit) ",  parent_debit_balance - parent_credit_balance])

            if account['root_type'] == 'Liability':
                account['balance'] = parent_credit_balance - parent_debit_balance
                accounts.append(["Total (Credit)",  parent_credit_balance - parent_debit_balance])
            balance += account['balance']
            parent_credit_balance = parent_debit_balance = 0
    accounts.append(["Profit or Loss", balance])
        
    return accounts
