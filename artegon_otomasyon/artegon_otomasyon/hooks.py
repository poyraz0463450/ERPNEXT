app_name = "artegon_otomasyon"
app_title = "ARTEGON Otomasyon"
app_publisher = "ARTEGON"
app_description = "ARTEGON üretim süreç otomasyonu"
app_email = "mehmet.poyraz@artegon.com.tr"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "artegon_otomasyon",
# 		"logo": "/assets/artegon_otomasyon/logo.png",
# 		"title": "ARTEGON Otomasyon",
# 		"route": "/artegon_otomasyon",
# 		"has_permission": "artegon_otomasyon.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/artegon_otomasyon/css/artegon_otomasyon.css"
# app_include_js = "/assets/artegon_otomasyon/js/artegon_otomasyon.js"

# include js, css files in header of web template
# web_include_css = "/assets/artegon_otomasyon/css/artegon_otomasyon.css"
# web_include_js = "/assets/artegon_otomasyon/js/artegon_otomasyon.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "artegon_otomasyon/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "artegon_otomasyon/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "artegon_otomasyon.utils.jinja_methods",
# 	"filters": "artegon_otomasyon.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "artegon_otomasyon.install.before_install"
# after_install = "artegon_otomasyon.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "artegon_otomasyon.uninstall.before_uninstall"
# after_uninstall = "artegon_otomasyon.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "artegon_otomasyon.utils.before_app_install"
# after_app_install = "artegon_otomasyon.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "artegon_otomasyon.utils.before_app_uninstall"
# after_app_uninstall = "artegon_otomasyon.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "artegon_otomasyon.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Order": {
		"on_submit": "artegon_otomasyon.automation.handle_sales_order_submit",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"artegon_otomasyon.tasks.all"
# 	],
# 	"daily": [
# 		"artegon_otomasyon.tasks.daily"
# 	],
# 	"hourly": [
# 		"artegon_otomasyon.tasks.hourly"
# 	],
# 	"weekly": [
# 		"artegon_otomasyon.tasks.weekly"
# 	],
# 	"monthly": [
# 		"artegon_otomasyon.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "artegon_otomasyon.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "artegon_otomasyon.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "artegon_otomasyon.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "artegon_otomasyon.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["artegon_otomasyon.utils.before_request"]
# after_request = ["artegon_otomasyon.utils.after_request"]

# Job Events
# ----------
# before_job = ["artegon_otomasyon.utils.before_job"]
# after_job = ["artegon_otomasyon.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"artegon_otomasyon.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
