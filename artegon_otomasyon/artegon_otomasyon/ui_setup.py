from __future__ import annotations

import json

import frappe


WORKSPACE_NAME = "ARTEGON Merkez"
SIDEBAR_NAME = "ARTEGON"
MODULE_NAME = "ARTEGON Otomasyon"
APP_NAME = "artegon_otomasyon"
DEFAULT_APP_ROUTE = "desk/Workspaces/ARTEGON%20Merkez"

HIDDEN_DESKTOP_ICONS = [
	"Accounting",
	"Accounts Setup",
	"Assets",
	"Automation",
	"Banking",
	"Budget",
	"Build",
	"Buying",
	"CRM",
	"Data",
	"Email",
	"ERPNext",
	"ERPNext Settings",
	"Financial Reports",
	"Framework",
	"Home",
	"Invoicing",
	"Integrations",
	"Manufacturing",
	"My Workspaces",
	"Organization",
	"Payments",
	"Printing",
	"Projects",
	"Quality",
	"Selling",
	"Share Management",
	"Stock",
	"Subcontracting",
	"Subscription",
	"Support",
	"System",
	"Taxes",
	"Users",
	"Website",
]

WORKSPACE_SHORTCUTS = [
	{"label": "Müşteri Siparişleri", "type": "DocType", "link_to": "Sales Order", "icon": "shopping-cart", "color": "#1F6FEB", "doc_view": "List"},
	{"label": "Eksik Malzeme Talepleri", "type": "DocType", "link_to": "Material Request", "icon": "file-warning", "color": "#E5532C", "doc_view": "List"},
	{"label": "Satın Alma Siparişleri", "type": "DocType", "link_to": "Purchase Order", "icon": "receipt", "color": "#F59E0B", "doc_view": "List"},
	{"label": "İş Emirleri", "type": "DocType", "link_to": "Work Order", "icon": "tool", "color": "#0F766E", "doc_view": "List"},
	{"label": "Kalite Kontrol", "type": "DocType", "link_to": "Quality Inspection", "icon": "check-circle", "color": "#059669", "doc_view": "List"},
	{"label": "Depo Hareketleri", "type": "DocType", "link_to": "Stock Entry", "icon": "arrow-right-left", "color": "#4F46E5", "doc_view": "List"},
	{"label": "Sevkiyat Fişleri", "type": "DocType", "link_to": "Delivery Note", "icon": "truck", "color": "#2563EB", "doc_view": "List"},
	{"label": "Model ve Malzeme Kartları", "type": "DocType", "link_to": "Item", "icon": "package", "color": "#7C3AED", "doc_view": "List"},
	{"label": "Reçeteler", "type": "DocType", "link_to": "BOM", "icon": "git-branch", "color": "#7C2D12", "doc_view": "List"},
]

SIDEBAR_ITEMS = [
	{"type": "Link", "label": "Ana Sayfa", "link_type": "Workspace", "link_to": WORKSPACE_NAME},
	{"type": "Section Break", "label": "Günlük İşler", "indent": 1},
	{"type": "Link", "label": "Müşteri Siparişleri", "link_type": "DocType", "link_to": "Sales Order", "child": 1},
	{"type": "Link", "label": "Eksik Malzeme Talepleri", "link_type": "DocType", "link_to": "Material Request", "child": 1},
	{"type": "Link", "label": "Satın Alma Siparişleri", "link_type": "DocType", "link_to": "Purchase Order", "child": 1},
	{"type": "Link", "label": "İş Emirleri", "link_type": "DocType", "link_to": "Work Order", "child": 1},
	{"type": "Link", "label": "Kalite Kontrol", "link_type": "DocType", "link_to": "Quality Inspection", "child": 1},
	{"type": "Link", "label": "Depo Hareketleri", "link_type": "DocType", "link_to": "Stock Entry", "child": 1},
	{"type": "Link", "label": "Sevkiyat Fişleri", "link_type": "DocType", "link_to": "Delivery Note", "child": 1},
	{"type": "Section Break", "label": "Ana Kartlar", "indent": 1},
	{"type": "Link", "label": "Model ve Malzeme Kartları", "link_type": "DocType", "link_to": "Item", "child": 1},
	{"type": "Link", "label": "Reçeteler", "link_type": "DocType", "link_to": "BOM", "child": 1},
	{"type": "Link", "label": "Depolar", "link_type": "DocType", "link_to": "Warehouse", "child": 1},
	{"type": "Link", "label": "Onaylı Tedarikçiler", "link_type": "DocType", "link_to": "Supplier", "child": 1},
	{"type": "Link", "label": "Müşteriler", "link_type": "DocType", "link_to": "Customer", "child": 1},
	{"type": "Section Break", "label": "Yönetim", "indent": 1},
	{"type": "Link", "label": "Günlük Yapılacaklar", "link_type": "DocType", "link_to": "ToDo", "child": 1},
	{"type": "Link", "label": "Kullanıcılar", "link_type": "DocType", "link_to": "User", "child": 1},
	{"type": "Link", "label": "Şirket", "link_type": "DocType", "link_to": "Company", "child": 1},
]


def _get_or_new(doctype: str, filters: dict) -> frappe.model.document.Document:
	existing = frappe.get_all(doctype, filters=filters, pluck="name", limit=1)
	return frappe.get_doc(doctype, existing[0]) if existing else frappe.new_doc(doctype)


def _set_child_rows(doc, fieldname: str, rows: list[dict]) -> None:
	doc.set(fieldname, [])
	for idx, row in enumerate(rows, start=1):
		payload = dict(row)
		payload["idx"] = idx
		doc.append(fieldname, payload)


def _workspace_content() -> str:
	blocks = [
		{
			"id": "artegon-header-1",
			"type": "header",
			"data": {"text": '<span class="h4"><b>Günlük Operasyon</b></span>', "col": 12},
		},
		{
			"id": "artegon-text-1",
			"type": "paragraph",
			"data": {
				"text": "Günlük kullanımda gereken ana ekranlar burada toplandı. Geri kalan teknik alanlar arka planda bırakıldı.",
				"col": 12,
			},
		},
	]

	for idx, shortcut in enumerate(WORKSPACE_SHORTCUTS[:6], start=1):
		blocks.append(
			{
				"id": f"artegon-shortcut-a-{idx}",
				"type": "shortcut",
				"data": {"shortcut_name": shortcut["label"], "col": 4},
			}
		)

	blocks.extend(
		[
			{"id": "artegon-space-1", "type": "spacer", "data": {"col": 12}},
			{
				"id": "artegon-header-2",
				"type": "header",
				"data": {"text": '<span class="h4"><b>Teknik ve Ana Kartlar</b></span>', "col": 12},
			},
		]
	)

	for idx, shortcut in enumerate(WORKSPACE_SHORTCUTS[6:], start=1):
		blocks.append(
			{
				"id": f"artegon-shortcut-b-{idx}",
				"type": "shortcut",
				"data": {"shortcut_name": shortcut["label"], "col": 4},
			}
		)

	return json.dumps(blocks, ensure_ascii=False)


def ensure_workspace() -> None:
	doc = _get_or_new("Workspace", {"title": WORKSPACE_NAME})
	doc.title = WORKSPACE_NAME
	doc.label = WORKSPACE_NAME
	doc.icon = "home"
	doc.module = MODULE_NAME
	doc.app = APP_NAME
	doc.type = "Workspace"
	doc.public = 1
	doc.is_hidden = 0
	doc.hide_custom = 1
	doc.content = _workspace_content()

	_set_child_rows(doc, "shortcuts", WORKSPACE_SHORTCUTS)
	_set_child_rows(
		doc,
		"links",
		[
			{"type": "Card Break", "label": "Teknik"},
			{"type": "Link", "label": "Model ve Malzeme Kartları", "link_type": "DocType", "link_to": "Item"},
			{"type": "Link", "label": "Reçeteler", "link_type": "DocType", "link_to": "BOM"},
			{"type": "Card Break", "label": "Operasyon"},
			{"type": "Link", "label": "Müşteri Siparişleri", "link_type": "DocType", "link_to": "Sales Order"},
			{"type": "Link", "label": "Eksik Malzeme Talepleri", "link_type": "DocType", "link_to": "Material Request"},
			{"type": "Link", "label": "İş Emirleri", "link_type": "DocType", "link_to": "Work Order"},
			{"type": "Link", "label": "Kalite Kontrol", "link_type": "DocType", "link_to": "Quality Inspection"},
			{"type": "Link", "label": "Sevkiyat Fişleri", "link_type": "DocType", "link_to": "Delivery Note"},
		],
	)

	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def ensure_sidebar() -> None:
	doc = _get_or_new("Workspace Sidebar", {"title": SIDEBAR_NAME})
	doc.title = SIDEBAR_NAME
	doc.header_icon = "home"
	doc.app = APP_NAME
	doc.module = MODULE_NAME
	doc.standard = 0
	doc.for_user = None
	_set_child_rows(doc, "items", SIDEBAR_ITEMS)

	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def ensure_desktop_icon() -> None:
	doc = _get_or_new("Desktop Icon", {"label": SIDEBAR_NAME})
	doc.label = SIDEBAR_NAME
	doc.icon_type = "Link"
	doc.link_type = "Workspace Sidebar"
	doc.link_to = SIDEBAR_NAME
	doc.app = APP_NAME
	doc.icon = "home"
	doc.bg_color = "blue"
	doc.hidden = 0
	doc.idx = 0
	doc.restrict_removal = 1
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def hide_standard_desktop_icons() -> None:
	for icon_name in HIDDEN_DESKTOP_ICONS:
		for record_name in frappe.get_all("Desktop Icon", filters={"label": icon_name}, pluck="name"):
			frappe.db.set_value("Desktop Icon", record_name, "hidden", 1, update_modified=False)


def set_default_workspace_for_users() -> None:
	for user_name in frappe.get_all(
		"User",
		filters={"enabled": 1, "user_type": "System User", "name": ("!=", "Guest")},
		pluck="name",
	):
		frappe.db.set_value("User", user_name, "default_workspace", WORKSPACE_NAME, update_modified=False)
		frappe.db.set_value("User", user_name, "default_app", APP_NAME, update_modified=False)


def set_default_app() -> None:
	frappe.db.set_single_value("System Settings", "default_app", APP_NAME, update_modified=False)


def apply_simplified_ui() -> dict[str, str]:
	ensure_workspace()
	ensure_sidebar()
	ensure_desktop_icon()
	hide_standard_desktop_icons()
	set_default_app()
	set_default_workspace_for_users()
	frappe.clear_cache()
	return {"workspace": WORKSPACE_NAME, "sidebar": SIDEBAR_NAME}


def get_website_user_home_page(user: str) -> str:
	user_type = frappe.get_cached_value("User", user, "user_type")
	if user_type == "System User":
		return DEFAULT_APP_ROUTE
	return "login"
