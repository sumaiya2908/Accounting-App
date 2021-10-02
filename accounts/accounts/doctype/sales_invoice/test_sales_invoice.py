# Copyright (c) 2021, Summayya and Contributors
# See license.txt

import frappe
import unittest


def create_sales_invoice():
	items = frappe.get_all('Item', fields=['name', 'price'])	
	amount = 0
	sales_invoice_items = []

	for item in items:
		sales_invoice_item = frappe.get_doc({
			'doctype': 'Item',
			'item': item.name,
			'quantity': 1,
			'rate': item.price
		})
		amount += item.price
		sales_invoice_items.append(sales_invoice_item)

		sales_invoice = frappe.get_doc({
		'doctype': 'Sales Invoice',
		'company': 'Gada Electronics',
		'customer': 'CBC retails',
		'item': sales_invoice_items,
		'debit_account': 'Debitors - GE',
        'credit_account': 'Sales - GE'
	})

	sales_invoice.submit()
	return sales_invoice.name, amount

class TestSalesInvoice(unittest.TestCase):
	
	def test_gl_entry(self):
		gl_entry_count_before = frappe.db.count('GL Entry')
		create_sales_invoice()
		gl_entry_count_after = frappe.db.count('GL Entry')

		gl_entries_created = gl_entry_count_after - gl_entry_count_before

		self.assertEqual(gl_entries_created, 2, f"Expected 2 gl entries for each invoice, got {gl_entries_created}")

	def test_total_amount(self):
		doc, total_amount = create_sales_invoice()
		sales_invoice = frappe.get_doc("Sales Invoice", doc)

		self.assertEqual(sales_invoice.amount, total_amount, f"Expected total {total_amount}, got {sales_invoice.amount}")
