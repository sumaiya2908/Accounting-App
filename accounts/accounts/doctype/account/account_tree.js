frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Account"] = {
	breadcrumbs: "Account",
	title: __("Charts of Accounts"),
	filters: [
		{
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			label: __("Company"),
			default: frappe.defaults.get_user_default("company")
		},
	  ],
	  root_label: "Accounts",
	  get_tree_nodes: 'accounts.accounts.doctype.account.account.get_accounts',

}