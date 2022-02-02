from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hotset_customizations"
app_title = "hotset_customizations"
app_publisher = "hotset_customizations"
app_description = "hotset_customizations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hotset_customizations@gmail.com"
app_license = "MIT"

fixtures = [
{"dt": "Custom Field",
	"filters": [
	[
             "name", "in", [
		"BOM Item-input_source",
		"Workstation-section_break_13",
		"Workstation-wip_warehouse",
		"Workstation-input_sources",
		"Serial No-stock_warehouse",
		"Serial No-secondary_uom",
		"Serial No-available_qty"
		]
	]
	]
}	
]

doctype_js = {
	"BOM" : "hotset_customizations/doctype/bom/bom.js",
	"Workstation": "hotset_customizations/doctype/workstation/workstation.js",
	"Work Order": "hotset_customizations/doctype/work_order/work_order.js",
	"Stock Entry": "hotset_customizations/doctype/stock_entry/stock_entry.js"
}

doc_events = {
    	"Stock Entry": {
		"on_submit": ["hotset_customizations.hotset_customizations.doctype.stock_entry.stock_entry.set_serial_no_status"],
		"before_cancel": ["hotset_customizations.hotset_customizations.doctype.stock_entry.stock_entry.set_serial_no_status"],
		"before_save": ["hotset_customizations.hotset_customizations.doctype.stock_entry.stock_entry.before_save"]

	},
	"Serial No": {
		"before_insert": ["hotset_customizations.hotset_customizations.doctype.serial_no.serial_no.before_insert"],
		"on_save":["hotset_customizations.hotset_customizations.doctype.serial_no.serial_no.on_save"]
	},
	"Purchase Receipt": {
		"on_submit": ["hotset_customizations.hotset_customizations.doctype.purchase_receipt.purchase_receipt.after_submit"]
	}
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hotset_customizations/css/hotset_customizations.css"
# app_include_js = "/assets/hotset_customizations/js/hotset_customizations.js"

# include js, css files in header of web template
# web_include_css = "/assets/hotset_customizations/css/hotset_customizations.css"
# web_include_js = "/assets/hotset_customizations/js/hotset_customizations.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hotset_customizations/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hotset_customizations.install.before_install"
# after_install = "hotset_customizations.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "hotset_customizations.uninstall.before_uninstall"
# after_uninstall = "hotset_customizations.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hotset_customizations.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"hotset_customizations.tasks.all"
# 	],
# 	"daily": [
# 		"hotset_customizations.tasks.daily"
# 	],
# 	"hourly": [
# 		"hotset_customizations.tasks.hourly"
# 	],
# 	"weekly": [
# 		"hotset_customizations.tasks.weekly"
# 	]
# 	"monthly": [
# 		"hotset_customizations.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "hotset_customizations.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hotset_customizations.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "hotset_customizations.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"hotset_customizations.auth.validate"
# ]

