# Copyright (c) 2013, Summayya and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	columns = get_columns()
	income_accounts = frappe.get_list("Account", pluck = "name", filters = {"root_type": "Income", "is_group": 0, "company": filters.company})
	expense_accounts = frappe.get_list("Account", pluck = "name", filters = {"root_type": "Expense", "is_group": 0, "company": filters.company})
	data, chart, report_summary = get_pnl_data(income_accounts, expense_accounts, columns)
	return columns, data, None, chart, report_summary


def get_pnl_data(income_accounts, expense_accounts, columns):
	incomes = frappe.get_list(
		"GL Entry",
		filters={
			"account": ["in", income_accounts]
		},
		fields=['account', 'sum(credit) - sum(debit) as amount'],
		group_by='account')

	expenses = frappe.get_list(
		"GL Entry",
		filters={
			"account": ["in", expense_accounts],

		},
		fields=['account', 'sum(debit) - sum(credit) as amount'],
		group_by='account')
	if incomes:
		print(incomes )
	total_income = {
		'account': "Total Income",
		'balance': incomes[0]['amount'] if incomes else 0
	}
	total_expense = {
		'account': "Total Expense",
		'balance': expenses[0]['amount'] if expenses else 0
	}
	net_profit_loss = flt(total_income['balance'], 3) - flt(total_expense['balance'], 3)
	net_profit_or_loss = {
		'account': 'Net Profit' if net_profit_loss else 'Net Loss',
		'balance': net_profit_loss
	}

	chart = get_chart_data(net_profit_loss, total_income['balance'], total_expense['balance'], columns)
	report_summary = get_report_summary(total_income['balance'], total_expense['balance'], net_profit_loss)

	return [net_profit_or_loss, total_income, total_expense], chart, report_summary

def get_chart_data(net_pnl, income, expense, columns):
	data = []

	data.append({'name': 'Income', 'values': [income]})
	data.append({'name': 'Expense', 'values': [expense]})
	data.append({'name': 'Net Profit or Loss', 'values': [net_pnl]})
	chart = {
		"data": {
			'labels': ['Income', 'Expense', 'Net Profit or Loss'],
			'datasets': data
		}
	}

	chart["type"] = "bar"
	chart["fieldtype"] = "Currency"

	return chart


def get_report_summary(income, expense, net_profit_loss):
    net_income, net_expense, net_profit = 0.0, 0.0, 0.0

    net_income = flt(income, 3)
    net_expense = flt(expense, 3)
    net_profit = flt(net_profit_loss, 3)

    profit_label = _('Net Profit')
    income_label = _('Total Income')
    expense_label = _('Total Expense')

    return [
        {
            'value': net_income,
            'label': income_label,
            'datatype': 'Currency'
        },
        { 'type': 'separator', 'value': '-' },
        {
            'value': net_expense,
            'label': expense_label,
            'datatype': 'Currency'
        },
        { 'type': 'separator', 'value': '=', 'color': 'blue' },
        {
            'value': net_profit,
            'indicator': 'Green' if net_profit > 0 else 'Red',
            'label': profit_label,
            'datatype': 'Currency'
        }
    ]


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
		"fieldtype": "data",
		"width": 300
	}]

	return columns
