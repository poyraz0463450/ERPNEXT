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

WORKSPACE_DEFINITIONS = [
	{
		"name": WORKSPACE_NAME,
		"title": WORKSPACE_NAME,
		"icon": "home",
		"description": "Savunma sanayi üretim akışında günlük operasyonları tek merkezden yönet.",
		"shortcuts": [
			{"label": "Satış Siparişleri", "type": "DocType", "link_to": "Sales Order", "icon": "shopping-cart", "color": "#0F62FE", "doc_view": "List"},
			{"label": "Üretim Planları", "type": "DocType", "link_to": "Production Plan", "icon": "calendar", "color": "#7C3AED", "doc_view": "List"},
			{"label": "Malzeme Talepleri", "type": "DocType", "link_to": "Material Request", "icon": "file-warning", "color": "#E5532C", "doc_view": "List"},
			{"label": "İş Emirleri", "type": "DocType", "link_to": "Work Order", "icon": "tool", "color": "#0F766E", "doc_view": "List"},
			{"label": "Kalite Kontrolleri", "type": "DocType", "link_to": "Quality Inspection", "icon": "check-circle", "color": "#059669", "doc_view": "List"},
			{"label": "Toplama Listeleri", "type": "DocType", "link_to": "Pick List", "icon": "list", "color": "#B45309", "doc_view": "List"},
			{"label": "Sevkiyat Fişleri", "type": "DocType", "link_to": "Delivery Note", "icon": "truck", "color": "#2563EB", "doc_view": "List"},
			{"label": "Tedarikçiler", "type": "DocType", "link_to": "Supplier", "icon": "users", "color": "#475569", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Ana Operasyon Belgeleri",
				"items": [
					{"label": "Teknik Veri Kartları", "link_type": "DocType", "link_to": "Item"},
					{"label": "Satış Siparişleri", "link_type": "DocType", "link_to": "Sales Order"},
					{"label": "Malzeme Talepleri", "link_type": "DocType", "link_to": "Material Request"},
					{"label": "Üretim Planları", "link_type": "DocType", "link_to": "Production Plan"},
					{"label": "Kalite Kontrolleri", "link_type": "DocType", "link_to": "Quality Inspection"},
					{"label": "Depo Hareketleri", "link_type": "DocType", "link_to": "Stock Entry"},
					{"label": "Montaj İş Kartları", "link_type": "DocType", "link_to": "Job Card"},
					{"label": "Dış Operasyon Siparişleri", "link_type": "DocType", "link_to": "Subcontracting Order"},
					{"label": "Muhasebe Fişleri", "link_type": "DocType", "link_to": "Payment Entry"},
					{"label": "Yönetim Kayıtları", "link_type": "DocType", "link_to": "User"},
				],
			},
			{
				"label": "Kritik Kartlar",
				"items": [
					{"label": "Parça ve Malzeme Kartları", "link_type": "DocType", "link_to": "Item"},
					{"label": "Reçeteler", "link_type": "DocType", "link_to": "BOM"},
					{"label": "Depolar", "link_type": "DocType", "link_to": "Warehouse"},
					{"label": "Müşteriler", "link_type": "DocType", "link_to": "Customer"},
				],
			},
		],
	},
	{
		"name": "Teknik Ekip",
		"title": "Teknik Ekip",
		"icon": "tool",
		"description": "Model, parça, reçete, operasyon ve teknik doküman yönetimi.",
		"shortcuts": [
			{"label": "Parça ve Malzeme Kartları", "type": "DocType", "link_to": "Item", "icon": "package", "color": "#7C3AED", "doc_view": "List"},
			{"label": "Reçeteler", "type": "DocType", "link_to": "BOM", "icon": "git-branch", "color": "#7C2D12", "doc_view": "List"},
			{"label": "Operasyonlar", "type": "DocType", "link_to": "Operation", "icon": "settings-2", "color": "#334155", "doc_view": "List"},
			{"label": "İş İstasyonları", "type": "DocType", "link_to": "Workstation", "icon": "factory", "color": "#0F766E", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Teknik Yapı",
				"items": [
					{"label": "Parça ve Malzeme Kartları", "link_type": "DocType", "link_to": "Item"},
					{"label": "Reçeteler", "link_type": "DocType", "link_to": "BOM"},
					{"label": "Operasyonlar", "link_type": "DocType", "link_to": "Operation"},
					{"label": "İş İstasyonları", "link_type": "DocType", "link_to": "Workstation"},
				],
			},
		],
	},
	{
		"name": "Satis ve Pazarlama",
		"title": "Satış ve Pazarlama",
		"icon": "shopping-cart",
		"description": "Müşteri, sözleşme, satış siparişi ve sevkiyat rotaları.",
		"shortcuts": [
			{"label": "Satış Siparişleri", "type": "DocType", "link_to": "Sales Order", "icon": "shopping-cart", "color": "#0F62FE", "doc_view": "List"},
			{"label": "Müşteriler", "type": "DocType", "link_to": "Customer", "icon": "users", "color": "#475569", "doc_view": "List"},
			{"label": "Sevkiyat Fişleri", "type": "DocType", "link_to": "Delivery Note", "icon": "truck", "color": "#2563EB", "doc_view": "List"},
			{"label": "Satış Faturaları", "type": "DocType", "link_to": "Sales Invoice", "icon": "receipt", "color": "#059669", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Satış Akışı",
				"items": [
					{"label": "Satış Siparişleri", "link_type": "DocType", "link_to": "Sales Order"},
					{"label": "Müşteriler", "link_type": "DocType", "link_to": "Customer"},
					{"label": "Sevkiyat Fişleri", "link_type": "DocType", "link_to": "Delivery Note"},
					{"label": "Satış Faturaları", "link_type": "DocType", "link_to": "Sales Invoice"},
				],
			},
		],
	},
	{
		"name": "Satin Alma ve Tedarik",
		"title": "Satın Alma ve Tedarik",
		"icon": "receipt",
		"description": "Malzeme talebi, teklif, sipariş ve tedarikçi yönetimi.",
		"shortcuts": [
			{"label": "Malzeme Talepleri", "type": "DocType", "link_to": "Material Request", "icon": "file-warning", "color": "#E5532C", "doc_view": "List"},
			{"label": "Teklif Talepleri", "type": "DocType", "link_to": "Request for Quotation", "icon": "mail", "color": "#0EA5E9", "doc_view": "List"},
			{"label": "Tedarikçi Teklifleri", "type": "DocType", "link_to": "Supplier Quotation", "icon": "file-text", "color": "#0284C7", "doc_view": "List"},
			{"label": "Satın Alma Siparişleri", "type": "DocType", "link_to": "Purchase Order", "icon": "receipt", "color": "#F59E0B", "doc_view": "List"},
			{"label": "Alış İrsaliyeleri", "type": "DocType", "link_to": "Purchase Receipt", "icon": "package-check", "color": "#0F766E", "doc_view": "List"},
			{"label": "Tedarikçiler", "type": "DocType", "link_to": "Supplier", "icon": "users", "color": "#475569", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Tedarik Akışı",
				"items": [
					{"label": "Malzeme Talepleri", "link_type": "DocType", "link_to": "Material Request"},
					{"label": "Teklif Talepleri", "link_type": "DocType", "link_to": "Request for Quotation"},
					{"label": "Tedarikçi Teklifleri", "link_type": "DocType", "link_to": "Supplier Quotation"},
					{"label": "Satın Alma Siparişleri", "link_type": "DocType", "link_to": "Purchase Order"},
					{"label": "Alış İrsaliyeleri", "link_type": "DocType", "link_to": "Purchase Receipt"},
					{"label": "Tedarikçiler", "link_type": "DocType", "link_to": "Supplier"},
				],
			},
		],
	},
	{
		"name": "Uretim Planlama",
		"title": "Üretim Planlama",
		"icon": "factory",
		"description": "MRP, iş emirleri, alt montajlar ve kapasite planlama ekranı.",
		"shortcuts": [
			{"label": "Üretim Planları", "type": "DocType", "link_to": "Production Plan", "icon": "calendar", "color": "#7C3AED", "doc_view": "List"},
			{"label": "İş Emirleri", "type": "DocType", "link_to": "Work Order", "icon": "tool", "color": "#0F766E", "doc_view": "List"},
			{"label": "İş Kartları", "type": "DocType", "link_to": "Job Card", "icon": "clipboard-list", "color": "#DC2626", "doc_view": "List"},
			{"label": "Reçeteler", "type": "DocType", "link_to": "BOM", "icon": "git-branch", "color": "#7C2D12", "doc_view": "List"},
			{"label": "Operasyonlar", "type": "DocType", "link_to": "Operation", "icon": "settings-2", "color": "#334155", "doc_view": "List"},
			{"label": "İş İstasyonları", "type": "DocType", "link_to": "Workstation", "icon": "factory", "color": "#1D4ED8", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Planlama ve Üretim",
				"items": [
					{"label": "Üretim Planları", "link_type": "DocType", "link_to": "Production Plan"},
					{"label": "İş Emirleri", "link_type": "DocType", "link_to": "Work Order"},
					{"label": "İş Kartları", "link_type": "DocType", "link_to": "Job Card"},
					{"label": "Reçeteler", "link_type": "DocType", "link_to": "BOM"},
				],
			},
		],
	},
	{
		"name": "Kalite Kontrol",
		"title": "Kalite Kontrol",
		"icon": "check-circle",
		"description": "Giriş, ara, final kalite ve uygunsuzluk takibi için merkez ekran.",
		"shortcuts": [
			{"label": "Kalite Kontrolleri", "type": "DocType", "link_to": "Quality Inspection", "icon": "check-circle", "color": "#059669", "doc_view": "List"},
			{"label": "Kalite Hedefleri", "type": "DocType", "link_to": "Quality Goal", "icon": "target", "color": "#0284C7", "doc_view": "List"},
			{"label": "Kalite İncelemeleri", "type": "DocType", "link_to": "Quality Review", "icon": "search-check", "color": "#7C3AED", "doc_view": "List"},
			{"label": "Uygunsuzluklar", "type": "DocType", "link_to": "Non Conformance", "icon": "triangle-alert", "color": "#DC2626", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Kalite Kayıtları",
				"items": [
					{"label": "Kalite Kontrolleri", "link_type": "DocType", "link_to": "Quality Inspection"},
					{"label": "Kalite Hedefleri", "link_type": "DocType", "link_to": "Quality Goal"},
					{"label": "Kalite İncelemeleri", "link_type": "DocType", "link_to": "Quality Review"},
					{"label": "Uygunsuzluklar", "link_type": "DocType", "link_to": "Non Conformance"},
				],
			},
		],
	},
	{
		"name": "Depo ve Sevkiyat",
		"title": "Depo ve Sevkiyat",
		"icon": "warehouse",
		"description": "Depolar, stok hareketleri, kitleme ve sevkiyat akışlarını yönet.",
		"shortcuts": [
			{"label": "Depolar", "type": "DocType", "link_to": "Warehouse", "icon": "warehouse", "color": "#475569", "doc_view": "List"},
			{"label": "Stok Hareketleri", "type": "DocType", "link_to": "Stock Entry", "icon": "arrow-right-left", "color": "#4F46E5", "doc_view": "List"},
			{"label": "Toplama Listeleri", "type": "DocType", "link_to": "Pick List", "icon": "list", "color": "#B45309", "doc_view": "List"},
			{"label": "Partiler", "type": "DocType", "link_to": "Batch", "icon": "layers-3", "color": "#7C2D12", "doc_view": "List"},
			{"label": "Seri Numaraları", "type": "DocType", "link_to": "Serial No", "icon": "hash", "color": "#0F62FE", "doc_view": "List"},
			{"label": "Sevkiyat Fişleri", "type": "DocType", "link_to": "Delivery Note", "icon": "truck", "color": "#2563EB", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Depo Akışı",
				"items": [
					{"label": "Depolar", "link_type": "DocType", "link_to": "Warehouse"},
					{"label": "Stok Hareketleri", "link_type": "DocType", "link_to": "Stock Entry"},
					{"label": "Toplama Listeleri", "link_type": "DocType", "link_to": "Pick List"},
					{"label": "Sevkiyat Fişleri", "link_type": "DocType", "link_to": "Delivery Note"},
				],
			},
		],
	},
	{
		"name": "Montaj ve Test",
		"title": "Montaj ve Test",
		"icon": "wrench",
		"description": "Montaj, toplama listesi teslimi ve test öncesi son kontroller.",
		"shortcuts": [
			{"label": "İş Emirleri", "type": "DocType", "link_to": "Work Order", "icon": "tool", "color": "#0F766E", "doc_view": "List"},
			{"label": "İş Kartları", "type": "DocType", "link_to": "Job Card", "icon": "clipboard-list", "color": "#DC2626", "doc_view": "List"},
			{"label": "Toplama Listeleri", "type": "DocType", "link_to": "Pick List", "icon": "list", "color": "#B45309", "doc_view": "List"},
			{"label": "Seri Numaraları", "type": "DocType", "link_to": "Serial No", "icon": "hash", "color": "#0F62FE", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Montaj Akışı",
				"items": [
					{"label": "İş Emirleri", "link_type": "DocType", "link_to": "Work Order"},
					{"label": "İş Kartları", "link_type": "DocType", "link_to": "Job Card"},
					{"label": "Toplama Listeleri", "link_type": "DocType", "link_to": "Pick List"},
					{"label": "Sevkiyat Fişleri", "link_type": "DocType", "link_to": "Delivery Note"},
				],
			},
		],
	},
	{
		"name": "Dis Operasyon",
		"title": "Dış Operasyon",
		"icon": "truck",
		"description": "Kaplama, ısıl işlem, boya ve fason takip rotaları.",
		"shortcuts": [
			{"label": "Fason Siparişleri", "type": "DocType", "link_to": "Subcontracting Order", "icon": "truck", "color": "#2563EB", "doc_view": "List"},
			{"label": "Fason Girişleri", "type": "DocType", "link_to": "Subcontracting Receipt", "icon": "package-check", "color": "#0F766E", "doc_view": "List"},
			{"label": "Tedarikçiler", "type": "DocType", "link_to": "Supplier", "icon": "users", "color": "#475569", "doc_view": "List"},
			{"label": "Satın Alma Siparişleri", "type": "DocType", "link_to": "Purchase Order", "icon": "receipt", "color": "#F59E0B", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Dış Kaynak Yönetimi",
				"items": [
					{"label": "Fason Siparişleri", "link_type": "DocType", "link_to": "Subcontracting Order"},
					{"label": "Fason Girişleri", "link_type": "DocType", "link_to": "Subcontracting Receipt"},
					{"label": "Tedarikçiler", "link_type": "DocType", "link_to": "Supplier"},
				],
			},
		],
	},
	{
		"name": "Muhasebe",
		"title": "Muhasebe",
		"icon": "wallet",
		"description": "Temel muhasebe, fatura ve ödeme ekranları.",
		"shortcuts": [
			{"label": "Satış Faturaları", "type": "DocType", "link_to": "Sales Invoice", "icon": "receipt", "color": "#059669", "doc_view": "List"},
			{"label": "Alış Faturaları", "type": "DocType", "link_to": "Purchase Invoice", "icon": "receipt", "color": "#B45309", "doc_view": "List"},
			{"label": "Ödeme Girişleri", "type": "DocType", "link_to": "Payment Entry", "icon": "wallet", "color": "#0F62FE", "doc_view": "List"},
			{"label": "Hesap Planı", "type": "DocType", "link_to": "Account", "icon": "book-open", "color": "#475569", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Muhasebe İşlemleri",
				"items": [
					{"label": "Satış Faturaları", "link_type": "DocType", "link_to": "Sales Invoice"},
					{"label": "Alış Faturaları", "link_type": "DocType", "link_to": "Purchase Invoice"},
					{"label": "Ödeme Girişleri", "link_type": "DocType", "link_to": "Payment Entry"},
					{"label": "Hesap Planı", "link_type": "DocType", "link_to": "Account"},
				],
			},
		],
	},
	{
		"name": "Yonetim ve Raporlar",
		"title": "Yönetim ve Raporlar",
		"icon": "settings",
		"description": "Kullanıcı, şirket, görev ve temel yönetim rotaları.",
		"shortcuts": [
			{"label": "Kullanıcılar", "type": "DocType", "link_to": "User", "icon": "users", "color": "#475569", "doc_view": "List"},
			{"label": "Şirket", "type": "DocType", "link_to": "Company", "icon": "building-2", "color": "#0F62FE", "doc_view": "List"},
			{"label": "Yapılacaklar", "type": "DocType", "link_to": "ToDo", "icon": "list-todo", "color": "#B45309", "doc_view": "List"},
			{"label": "Departmanlar", "type": "DocType", "link_to": "Department", "icon": "network", "color": "#7C3AED", "doc_view": "List"},
		],
		"cards": [
			{
				"label": "Yönetim",
				"items": [
					{"label": "Kullanıcılar", "link_type": "DocType", "link_to": "User"},
					{"label": "Şirket", "link_type": "DocType", "link_to": "Company"},
					{"label": "Yapılacaklar", "link_type": "DocType", "link_to": "ToDo"},
					{"label": "Departmanlar", "link_type": "DocType", "link_to": "Department"},
				],
			},
		],
	},
]

SIDEBAR_ITEMS = [
	{"type": "Link", "label": "Ana Ekran", "link_type": "Workspace", "link_to": WORKSPACE_NAME},
	{"type": "Section Break", "label": "Operasyon Bölümleri", "indent": 1},
	{"type": "Link", "label": "Teknik Ekip", "link_type": "Workspace", "link_to": "Teknik Ekip", "child": 1},
	{"type": "Link", "label": "Satış ve Pazarlama", "link_type": "Workspace", "link_to": "Satis ve Pazarlama", "child": 1},
	{"type": "Link", "label": "Satın Alma ve Tedarik", "link_type": "Workspace", "link_to": "Satin Alma ve Tedarik", "child": 1},
	{"type": "Link", "label": "Üretim Planlama", "link_type": "Workspace", "link_to": "Uretim Planlama", "child": 1},
	{"type": "Link", "label": "Kalite Kontrol", "link_type": "Workspace", "link_to": "Kalite Kontrol", "child": 1},
	{"type": "Link", "label": "Depo ve Sevkiyat", "link_type": "Workspace", "link_to": "Depo ve Sevkiyat", "child": 1},
	{"type": "Link", "label": "Montaj ve Test", "link_type": "Workspace", "link_to": "Montaj ve Test", "child": 1},
	{"type": "Link", "label": "Dış Operasyon", "link_type": "Workspace", "link_to": "Dis Operasyon", "child": 1},
	{"type": "Link", "label": "Muhasebe", "link_type": "Workspace", "link_to": "Muhasebe", "child": 1},
	{"type": "Link", "label": "Yönetim ve Raporlar", "link_type": "Workspace", "link_to": "Yonetim ve Raporlar", "child": 1},
	{"type": "Section Break", "label": "Hızlı Belgeler", "indent": 1},
	{"type": "Link", "label": "Satış Siparişleri", "link_type": "DocType", "link_to": "Sales Order", "child": 1},
	{"type": "Link", "label": "Üretim Planları", "link_type": "DocType", "link_to": "Production Plan", "child": 1},
	{"type": "Link", "label": "İş Emirleri", "link_type": "DocType", "link_to": "Work Order", "child": 1},
	{"type": "Link", "label": "Kalite Kontrolleri", "link_type": "DocType", "link_to": "Quality Inspection", "child": 1},
	{"type": "Link", "label": "Toplama Listeleri", "link_type": "DocType", "link_to": "Pick List", "child": 1},
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


def _is_valid_target(link_type: str | None, link_to: str | None) -> bool:
	if not link_to:
		return False
	if link_type == "DocType":
		return bool(frappe.db.exists("DocType", link_to))
	if link_type == "Report":
		return bool(frappe.db.exists("Report", link_to))
	if link_type == "Page":
		return bool(frappe.db.exists("Page", link_to))
	if link_type == "Workspace":
		return bool(frappe.db.exists("Workspace", link_to))
	return True


def _filter_shortcuts(rows: list[dict]) -> list[dict]:
	return [row for row in rows if _is_valid_target(row.get("type"), row.get("link_to"))]


def _workspace_links(cards: list[dict]) -> list[dict]:
	rows = []
	for card in cards:
		items = [
			item for item in card.get("items", []) if _is_valid_target(item.get("link_type"), item.get("link_to"))
		]
		if not items:
			continue
		rows.append({"type": "Card Break", "label": card["label"]})
		for item in items:
			rows.append(
				{
					"type": "Link",
					"label": item["label"],
					"link_type": item["link_type"],
					"link_to": item["link_to"],
				}
			)
	return rows


def _workspace_content(definition: dict, shortcuts: list[dict]) -> str:
	blocks = [
		{
			"id": f"{definition['title']}-header",
			"type": "header",
			"data": {"text": f"<span class='h4'><b>{definition['title']}</b></span>", "col": 12},
		},
		{
			"id": f"{definition['title']}-description",
			"type": "paragraph",
			"data": {"text": definition["description"], "col": 12},
		},
	]

	for idx, shortcut in enumerate(shortcuts, start=1):
		blocks.append(
			{
				"id": f"{definition['title']}-shortcut-{idx}",
				"type": "shortcut",
				"data": {"shortcut_name": shortcut["label"], "col": 4},
			}
		)

	return json.dumps(blocks, ensure_ascii=False)


def ensure_workspace(definition: dict) -> None:
	workspace_name = definition.get("name") or definition["title"]
	doc = _get_or_new("Workspace", {"name": workspace_name})
	shortcuts = _filter_shortcuts(definition.get("shortcuts", []))
	links = _workspace_links(definition.get("cards", []))

	if doc.is_new():
		doc.name = workspace_name
	doc.title = definition["title"]
	doc.label = definition["title"]
	doc.icon = definition["icon"]
	doc.module = MODULE_NAME
	doc.app = APP_NAME
	doc.type = "Workspace"
	doc.public = 1
	doc.is_hidden = 0
	doc.hide_custom = 1
	doc.content = _workspace_content(definition, shortcuts)

	_set_child_rows(doc, "shortcuts", shortcuts)
	_set_child_rows(doc, "links", links)

	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def ensure_workspaces() -> None:
	for definition in sorted(WORKSPACE_DEFINITIONS, key=lambda row: row["title"] == WORKSPACE_NAME):
		ensure_workspace(definition)


def ensure_sidebar() -> None:
	doc = _get_or_new("Workspace Sidebar", {"title": SIDEBAR_NAME})
	doc.title = SIDEBAR_NAME
	doc.header_icon = "home"
	doc.app = APP_NAME
	doc.module = MODULE_NAME
	doc.standard = 0
	doc.for_user = None
	_set_child_rows(
		doc,
		"items",
		[
			item
			for item in SIDEBAR_ITEMS
			if item["type"] != "Link" or _is_valid_target(item.get("link_type"), item.get("link_to"))
		],
	)

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


def _set_single_if_present(doctype: str, fieldname: str, value: str) -> None:
	try:
		if frappe.get_meta(doctype).get_field(fieldname):
			frappe.db.set_single_value(doctype, fieldname, value, update_modified=False)
	except Exception:
		pass


def apply_artegon_defaults() -> None:
	defaults = {
		"lang": "tr",
		"language": "tr",
		"country": "Türkiye",
		"currency": "TRY",
		"time_zone": "Europe/Istanbul",
		"number_format": "#.###,##",
		"desktop:home_page": "workspace",
		"company": "ARTEGON",
	}

	for key, value in defaults.items():
		frappe.db.set_default(key, value)

	_set_single_if_present("System Settings", "language", "tr")
	_set_single_if_present("System Settings", "time_zone", "Europe/Istanbul")
	_set_single_if_present("Global Defaults", "default_currency", "TRY")
	_set_single_if_present("Global Defaults", "country", "Türkiye")
	_set_single_if_present("Global Defaults", "default_company", "ARTEGON")


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
	apply_artegon_defaults()
	ensure_workspaces()
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
