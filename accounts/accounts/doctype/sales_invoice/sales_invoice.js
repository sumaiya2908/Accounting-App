// Copyright (c) 2021, Summayya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Invoice", {
	refresh: function (frm) {
		frm.trigger("set_total");
	},

	company: function (frm) {
		console.log('Sales - '+ frm.doc.abbr)
		frm.set_value("credit_account", 'Sales - ' + frm.doc.abbr)
		frm.set_value("debit_account", 'Debitors - ' + frm.doc.abbr )
	},

	set_total: function (frm) {
		let total_amount = 0;
		let total_quantity = 0;
		if (frm.doc.item) {
			frm.doc.item.forEach((item) => {
				total_amount += item.amount;
				total_quantity += item.quantity;
			});
		}
		frm.set_value("amount", total_amount);
		frm.set_value("total_quantity", total_quantity);
		frm.refresh_fields();
	},
});

frappe.ui.form.on("Invoice Item", {
	rate: function (frm, cdn, cdt) {
		let item = frappe.get_doc(cdn, cdt);
		item.amount = item.rate * item.quantity;
		frm.trigger("set_total");
		frm.refresh_field("item");
	},
	quantity: function (frm, cdn, cdt) {
		let item = frappe.get_doc(cdn, cdt);
		item.amount = item.rate * item.quantity;
		frm.trigger("set_total");
		frm.refresh_field("item");
	},
});
