// Copyright (c) 2016, Summayya and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss"] = {
	"filters": [
		{
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
        },


	]
};
