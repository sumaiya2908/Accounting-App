# Copyright (c) 2013, Summayya and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


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
        "fieldname": "opening_dr",
        "label": _("Opening (Dr)"),
        "fieldtype": "Currency",
        "default": 0,
        "width": 150
    },
    {
        "fieldname": "opening_cr",
        "label": _("Opening (Cr)"),
        "fieldtype": "Currency",
        "default": 0,
        "width": 150
    },
    {
        "fieldname": "debit",
        "label": _("Debit"),
        "fieldtype": "Currency",
        "default": 0,
        "width": 150
    },
    {
        "fieldname": "credit",
        "label": _("Credit"),
        "fieldtype": "Currency",
        "default": 0,
    },
    
    {
        "fieldname": "closing_dr",
        "label": _("Closing (Dr)"),
        "fieldtype": "Currency",
        "default": 0,
        "width": 150
    },
    {
        "fieldname": "closing_cr",
        "label": _("Closing (Cr)"),
        "fieldtype": "Currency",
        "default": 0,
        "width": 150
    },]
    return columns


def get_accounts_with_desc(parent_accounts, child_accounts):
    accounts = []
    parent_credit_balance = parent_debit_balance = child_credit_balance = child_debit_balance = 0
    '''insert parent account'''
    for account in parent_accounts:
        account['indent'] = 0.0
        account['opening_dr'] = 0
        account['opening_cr'] = 0
        accounts.append(account)

        '''insert child account'''
        for child_account in child_accounts:
            if(child_account['parent_account'] == account['account']):
                '''get gl entries for child accounts'''
                gl_entry = frappe.get_all('GL Entry', fields=[
                    'name as account', 'debit', 'credit'], filters={'account': child_account['account']})
                '''calculate debit and credit of all gl entries'''
                for entry in gl_entry:
                    child_credit_balance += entry.credit
                    child_debit_balance += entry.debit
                ''''opening debit and credit'''
                child_account['opening_dr'] = 0
                child_account['opening_cr'] = 0
                child_account['debit'] = child_debit_balance
                child_account['credit'] = child_credit_balance
                '''closing debit and credit'''
                child_account['closing_dr'], child_account['closing_cr'] = get_closing_balance(child_debit_balance, child_credit_balance)
                child_account['indent'] = 1.0
                accounts.append(child_account)
                parent_credit_balance += child_credit_balance
                parent_debit_balance += child_debit_balance
                child_credit_balance = child_debit_balance = 0
        
        account['debit'] = parent_debit_balance
        account['credit'] = parent_credit_balance
        account['closing_dr'], account['closing_cr'] = get_closing_balance(parent_debit_balance, parent_credit_balance)
        parent_credit_balance = parent_debit_balance = 0
        
    return accounts


def get_closing_balance(debit, credit):
    cl_debit = cl_credit = 0
    diff = debit - credit
    if diff > 0:
        cl_debit = diff
    else:
        cl_credit = -diff

    return cl_debit, cl_credit