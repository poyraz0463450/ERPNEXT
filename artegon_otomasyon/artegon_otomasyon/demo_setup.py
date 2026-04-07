from __future__ import annotations

from pathlib import Path

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils import flt, nowdate
from frappe.utils.file_manager import save_file
from pypdf import PdfWriter

from artegon_otomasyon.ui_setup import apply_simplified_ui


COMPANY = "ARTEGON"
BUYING_PRICE_LIST = "ART Satın Alma TL"
SELLING_PRICE_LIST = "ART Satış TL"
BENCH_PATH = Path("/home/mehmet/frappe-develop-bench")
PDF_DIR = BENCH_PATH / "sites" / "erpnext.localhost" / "private" / "files" / "artegon_teknik_resimler"

DEPARTMENTS = [
	"Teknik Ekip",
	"Satış ve Pazarlama",
	"Depo",
	"Satın Alma",
	"Üretim",
	"Giriş Kalite Kontrol",
	"Montaj",
	"Paketleme ve Sevkiyat",
]

DEMO_USERS = [
	{"email": "teknik@artegon.com.tr", "first_name": "Teknik", "last_name": "Ekip", "department": "Teknik Ekip", "roles": ["System Manager", "Manufacturing User", "Stock User"]},
	{"email": "satis@artegon.com.tr", "first_name": "Satış", "last_name": "Pazarlama", "department": "Satış ve Pazarlama", "roles": ["Sales User", "Sales Manager"]},
	{"email": "depo@artegon.com.tr", "first_name": "Depo", "last_name": "Sorumlusu", "department": "Depo", "roles": ["Stock User", "Stock Manager"]},
	{"email": "satinalma@artegon.com.tr", "first_name": "Satın Alma", "last_name": "Uzmanı", "department": "Satın Alma", "roles": ["Purchase User", "Purchase Manager"]},
	{"email": "uretim@artegon.com.tr", "first_name": "Üretim", "last_name": "Planlama", "department": "Üretim", "roles": ["Manufacturing User", "Manufacturing Manager", "Stock User"]},
	{"email": "kalite@artegon.com.tr", "first_name": "Kalite", "last_name": "Kontrol", "department": "Giriş Kalite Kontrol", "roles": ["Quality Manager", "Stock User"]},
	{"email": "montaj@artegon.com.tr", "first_name": "Montaj", "last_name": "Sorumlusu", "department": "Montaj", "roles": ["Manufacturing User", "Stock User"]},
	{"email": "paketleme@artegon.com.tr", "first_name": "Paketleme", "last_name": "Sevkiyat", "department": "Paketleme ve Sevkiyat", "roles": ["Stock User"]},
]

WORKSTATIONS = [
	("Teknik Ofis", 1, 250.0),
	("Lazer Kesim Hattı", 2, 325.0),
	("CNC İşleme Hattı", 2, 420.0),
	("Montaj Hattı", 4, 280.0),
	("Kalite Kontrol Alanı", 2, 220.0),
	("Paketleme Alanı", 2, 180.0),
]

OPERATIONS = {
	"Teknik Dokümantasyon": "Teknik Ofis",
	"Lazer Kesim": "Lazer Kesim Hattı",
	"CNC İşleme": "CNC İşleme Hattı",
	"Montaj": "Montaj Hattı",
	"Giriş Kalite Kontrol": "Kalite Kontrol Alanı",
	"Fonksiyon Testi": "Kalite Kontrol Alanı",
	"Paketleme": "Paketleme Alanı",
}

SUPPLIERS = ["Anadolu Metal Sanayi", "Marmara Endüstriyel Tedarik", "Eksen Dış Operasyon"]
CUSTOMERS = ["Delta Makina A.Ş.", "Yıldız Endüstri Ltd."]

PURCHASED_MATERIALS = [
	("MAT-001", "Şase Sacı 2 mm", 125.0), ("MAT-002", "Üst Kapak Sacı", 118.0), ("MAT-003", "Bağlantı Pimi 8 mm", 38.0),
	("MAT-004", "Kılavuz Mil", 64.0), ("MAT-005", "Bronz Burç", 42.0), ("MAT-006", "Basınç Yayı", 21.0),
	("MAT-007", "M5 Civata", 4.5), ("MAT-008", "M6 Civata", 5.2), ("MAT-009", "Rondela 6 mm", 1.4),
	("MAT-010", "Kilit Somunu M6", 2.1), ("MAT-011", "Alüminyum Profil 20x20", 92.0), ("MAT-012", "Poliüretan Tampon", 14.0),
	("MAT-013", "Sensör Yuvası", 39.0), ("MAT-014", "Kontrol Kartı", 285.0), ("MAT-015", "Kablo Seti", 57.0),
	("MAT-016", "Paslanmaz Mil 10 mm", 71.0), ("MAT-017", "Lineer Rulman", 95.0), ("MAT-018", "Destek Sacı", 49.0),
	("MAT-019", "Ayar Vidası", 9.0), ("MAT-020", "Emniyet Klipsi", 3.5), ("MAT-021", "Yan Kapak Sol", 53.0),
	("MAT-022", "Yan Kapak Sağ", 53.0), ("MAT-023", "Teflon Burç", 28.0), ("MAT-024", "Kablo Rakoru", 17.0),
	("MAT-025", "Mikro Anahtar", 46.0), ("MAT-026", "Etiket Plakası", 8.0), ("MAT-027", "Conta Seti", 13.0),
	("MAT-028", "Yalıtım Keçesi", 15.0), ("MAT-029", "Sabitleme Kelepçesi", 11.0), ("MAT-030", "Seviye Pulu", 7.0),
]

PACKAGING_MATERIALS = [
	("AMB-001", "İç Kutu", 18.0), ("AMB-002", "Dış Koli", 24.0), ("AMB-003", "Köpük Destek", 8.0), ("AMB-004", "Koruyucu Poşet", 3.0),
	("AMB-005", "Koli Bandı", 2.0), ("AMB-006", "Sevkiyat Etiketi", 1.2), ("AMB-007", "Nem Alıcı Poşet", 0.8), ("AMB-008", "Kullanım Kılavuzu", 4.0),
	("AMB-009", "Kalite Kartı", 2.5), ("AMB-010", "Palet Etiketi", 1.0),
]

SEMI_FINISHED = [
	("YRM-001", "Ana Şase Modülü", 0.0, "İç Üretim", "Kaplama\nIsıl İşlem"),
	("YRM-002", "Kilit Modülü", 0.0, "İç Üretim", "Isıl İşlem"),
	("YRM-003", "Kontrol Bloğu", 0.0, "İç Üretim", ""),
	("YRM-004", "Üst Kapak Grubu", 0.0, "İç Üretim", "Boya"),
	("YRM-005", "Hareket Aktarma Grubu", 0.0, "İç Üretim", "Kaplama"),
	("YRM-006", "Gövde Ara Plakası", 0.0, "İç Üretim", ""),
	("YRM-007", "Ön Bağlantı Grubu", 0.0, "İç Üretim", ""),
	("YRM-008", "Arka Bağlantı Grubu", 0.0, "İç Üretim", ""),
	("YRM-009", "Montaj Kızak Takımı", 0.0, "İç Üretim", ""),
	("YRM-010", "Test Mekanizması", 0.0, "İç Üretim", ""),
]

MODELS = [
	("MDL-A100", "Kompakt Seri", 17500.0), ("MDL-A200", "Standart Seri", 19800.0), ("MDL-B100", "Dayanım Serisi", 21500.0),
	("MDL-B200", "Hassas Seri", 24800.0), ("MDL-C300", "Özel Seri", 28900.0),
]

BOM_COMPONENTS = {
	"YRM-001": [("MAT-001", 1), ("MAT-003", 2), ("MAT-007", 4), ("MAT-018", 1)],
	"YRM-002": [("MAT-004", 1), ("MAT-006", 2), ("MAT-016", 1), ("MAT-020", 2)],
	"YRM-003": [("MAT-014", 1), ("MAT-015", 1), ("MAT-025", 1), ("MAT-026", 1)],
	"YRM-004": [("MAT-002", 1), ("MAT-007", 6), ("MAT-021", 1), ("MAT-022", 1)],
	"YRM-005": [("MAT-011", 1), ("MAT-017", 2), ("MAT-019", 2), ("MAT-027", 1)],
	"YRM-006": [("MAT-018", 1), ("MAT-023", 2), ("MAT-008", 4)],
	"YRM-007": [("MAT-016", 1), ("MAT-017", 1), ("MAT-030", 2), ("MAT-009", 4)],
	"YRM-008": [("MAT-016", 1), ("MAT-028", 2), ("MAT-010", 2), ("MAT-009", 4)],
	"YRM-009": [("MAT-011", 1), ("MAT-024", 1), ("MAT-029", 2), ("MAT-008", 2)],
	"YRM-010": [("MAT-013", 1), ("MAT-014", 1), ("MAT-006", 1), ("MAT-025", 1)],
	"MDL-A100": [("YRM-001", 1), ("YRM-002", 1), ("YRM-003", 1), ("YRM-007", 1), ("AMB-001", 1), ("AMB-003", 1), ("MAT-027", 1), ("MAT-029", 2)],
	"MDL-A200": [("YRM-001", 1), ("YRM-004", 1), ("YRM-005", 1), ("YRM-008", 1), ("AMB-001", 1), ("AMB-004", 1), ("MAT-012", 2), ("MAT-015", 1)],
	"MDL-B100": [("YRM-002", 1), ("YRM-004", 1), ("YRM-006", 1), ("YRM-009", 1), ("AMB-002", 1), ("AMB-005", 1), ("MAT-019", 2), ("MAT-030", 2)],
	"MDL-B200": [("YRM-001", 1), ("YRM-003", 1), ("YRM-005", 1), ("YRM-010", 1), ("AMB-002", 1), ("AMB-006", 1), ("MAT-024", 1), ("MAT-028", 1)],
	"MDL-C300": [("YRM-004", 1), ("YRM-006", 1), ("YRM-008", 1), ("YRM-010", 1), ("AMB-002", 1), ("AMB-007", 1), ("MAT-013", 1), ("MAT-014", 1)],
}

BOM_OPERATIONS = {
	"YRM-001": [("Lazer Kesim", 20), ("CNC İşleme", 25), ("Giriş Kalite Kontrol", 10)],
	"YRM-002": [("CNC İşleme", 30), ("Giriş Kalite Kontrol", 8)],
	"YRM-003": [("Montaj", 15), ("Giriş Kalite Kontrol", 6)],
	"YRM-004": [("Lazer Kesim", 18), ("Montaj", 10), ("Giriş Kalite Kontrol", 8)],
	"YRM-005": [("CNC İşleme", 24), ("Montaj", 12), ("Giriş Kalite Kontrol", 8)],
	"YRM-006": [("Lazer Kesim", 12), ("Montaj", 6)],
	"YRM-007": [("Montaj", 10), ("Giriş Kalite Kontrol", 5)],
	"YRM-008": [("Montaj", 10), ("Giriş Kalite Kontrol", 5)],
	"YRM-009": [("Montaj", 12), ("Giriş Kalite Kontrol", 5)],
	"YRM-010": [("Montaj", 10), ("Fonksiyon Testi", 10)],
	"MDL-A100": [("Montaj", 20), ("Fonksiyon Testi", 12), ("Paketleme", 8)],
	"MDL-A200": [("Montaj", 22), ("Fonksiyon Testi", 12), ("Paketleme", 8)],
	"MDL-B100": [("Montaj", 24), ("Fonksiyon Testi", 14), ("Paketleme", 8)],
	"MDL-B200": [("Montaj", 28), ("Fonksiyon Testi", 16), ("Paketleme", 8)],
	"MDL-C300": [("Montaj", 32), ("Fonksiyon Testi", 20), ("Paketleme", 10)],
}

OPENING_STOCK = {
	"MAT-001": 60, "MAT-002": 50, "MAT-003": 8, "MAT-004": 24, "MAT-005": 40, "MAT-006": 6, "MAT-007": 300, "MAT-008": 250,
	"MAT-009": 400, "MAT-010": 200, "MAT-011": 25, "MAT-012": 60, "MAT-013": 15, "MAT-014": 2, "MAT-015": 20, "MAT-016": 18,
	"MAT-017": 3, "MAT-018": 22, "MAT-019": 90, "MAT-020": 70, "MAT-021": 1, "MAT-022": 4, "MAT-023": 30, "MAT-024": 12,
	"MAT-025": 12, "MAT-026": 40, "MAT-027": 35, "MAT-028": 16, "MAT-029": 80, "MAT-030": 55, "AMB-001": 3, "AMB-002": 10,
	"AMB-003": 12, "AMB-004": 20, "AMB-005": 30, "AMB-006": 40, "AMB-007": 25, "AMB-008": 20, "AMB-009": 20, "AMB-010": 20,
	"YRM-001": 4, "YRM-002": 1, "YRM-003": 2, "YRM-004": 0, "YRM-005": 1, "YRM-006": 2, "YRM-007": 3, "YRM-008": 2, "YRM-009": 2,
	"YRM-010": 1, "MDL-A100": 2, "MDL-B200": 1,
}


def _abbr() -> str:
	return frappe.db.get_value("Company", COMPANY, "abbr") or "ART"


def _wh(label: str) -> str:
	return f"{label} - {_abbr()}"


def _ensure_account_currency(account_name: str | None, currency: str) -> str | None:
	if not account_name or not frappe.db.exists("Account", account_name):
		return None
	account = frappe.get_doc("Account", account_name)
	if account.account_currency != currency:
		account.account_currency = currency
		account.save(ignore_permissions=True)
	return account.name


def _set_single(doctype: str, values: dict) -> None:
	doc = frappe.get_single(doctype)
	changed = False
	for key, value in values.items():
		if hasattr(doc, key) and getattr(doc, key) != value:
			setattr(doc, key, value)
			changed = True
	if changed:
		doc.save(ignore_permissions=True)


def _ensure_uom(name: str) -> None:
	if not frappe.db.exists("UOM", name):
		frappe.get_doc({"doctype": "UOM", "uom_name": name}).insert(ignore_permissions=True)


def _ensure_department(name: str) -> None:
	if frappe.get_all("Department", filters={"department_name": name, "company": COMPANY}, pluck="name"):
		return
	if not frappe.db.exists("Department", name):
		frappe.get_doc({"doctype": "Department", "department_name": name, "company": COMPANY}).insert(ignore_permissions=True)


def _department_docname(name: str) -> str:
	return frappe.db.get_value("Department", {"department_name": name, "company": COMPANY}, "name") or name


def _party_docname(doctype: str, display_name: str) -> str:
	fieldname = "supplier_name" if doctype == "Supplier" else "customer_name"
	return frappe.db.get_value(doctype, {fieldname: display_name}, "name") or display_name


def _ensure_user(row: dict) -> None:
	email = row["email"]
	if frappe.db.exists("User", email):
		user = frappe.get_doc("User", email)
	else:
		user = frappe.get_doc({"doctype": "User", "email": email, "first_name": row["first_name"], "last_name": row["last_name"], "send_welcome_email": 0, "user_type": "System User"}).insert(ignore_permissions=True)
	user.language = "tr"
	user.enabled = 1
	user.save(ignore_permissions=True)
	for role in row["roles"]:
		if frappe.db.exists("Role", role):
			user.add_roles(role)
	if not frappe.db.exists("Employee", {"user_id": email}):
		frappe.get_doc({"doctype": "Employee", "first_name": row["first_name"], "last_name": row["last_name"], "employee_name": f"{row['first_name']} {row['last_name']}", "company": COMPANY, "department": _department_docname(row["department"]), "user_id": email, "date_of_joining": nowdate(), "date_of_birth": "1990-01-01", "status": "Active", "gender": "Male"}).insert(ignore_permissions=True)


def _ensure_price_list(name: str, buying: int, selling: int) -> None:
	if frappe.db.exists("Price List", name):
		doc = frappe.get_doc("Price List", name)
	else:
		doc = frappe.get_doc({"doctype": "Price List", "price_list_name": name})
	doc.currency = "TRY"
	doc.enabled = 1
	doc.buying = buying
	doc.selling = selling
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _ensure_party(doctype: str, name: str) -> None:
	if doctype == "Supplier":
		existing = frappe.get_all("Supplier", filters={"supplier_name": name}, pluck="name")
		doc = frappe.get_doc("Supplier", existing[0]) if existing else frappe.get_doc({"doctype": "Supplier"})
		doc.supplier_name = name
		doc.supplier_group = "Raw Material"
	else:
		existing = frappe.get_all("Customer", filters={"customer_name": name}, pluck="name")
		doc = frappe.get_doc("Customer", existing[0]) if existing else frappe.get_doc({"doctype": "Customer"})
		doc.customer_name = name
		doc.customer_group = "Commercial"
		doc.territory = "Türkiye"
	doc.default_currency = "TRY"
	doc.language = "tr"
	doc.country = "Türkiye"
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _ensure_item_group(name: str, parent: str) -> None:
	if not frappe.db.exists("Item Group", name):
		frappe.get_doc({"doctype": "Item Group", "item_group_name": name, "parent_item_group": parent, "is_group": 0}).insert(ignore_permissions=True)


def _ensure_warehouse(label: str, parent: str) -> None:
	if not frappe.db.exists("Warehouse", _wh(label)):
		frappe.get_doc({"doctype": "Warehouse", "warehouse_name": label, "parent_warehouse": parent, "company": COMPANY, "is_group": 0}).insert(ignore_permissions=True)


def _ensure_workstation(name: str, capacity: int, rate: float) -> None:
	if frappe.db.exists("Workstation", name):
		doc = frappe.get_doc("Workstation", name)
	else:
		doc = frappe.get_doc({"doctype": "Workstation", "workstation_name": name})
	doc.production_capacity = capacity
	doc.hour_rate = rate
	doc.warehouse = _wh("Devam Eden İşler")
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _ensure_operation(name: str, workstation: str) -> None:
	if frappe.db.exists("Operation", name):
		doc = frappe.get_doc("Operation", name)
	else:
		doc = frappe.new_doc("Operation")
		doc.name = name
	doc.workstation = workstation
	doc.description = f"{name} operasyonu"
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _ensure_custom_fields() -> None:
	create_custom_fields(
		{
			"Item": [
				{"fieldname": "artegon_urun_tipi", "label": "ARTEGON Ürün Tipi", "fieldtype": "Select", "options": "Model\nYarı Mamul\nMalzeme\nAmbalaj\nHizmet", "insert_after": "item_group"},
				{"fieldname": "artegon_tedarik_yontemi", "label": "Tedarik Yöntemi", "fieldtype": "Select", "options": "Satın Alma\nİç Üretim\nDış Operasyon", "insert_after": "default_material_request_type"},
				{"fieldname": "artegon_dis_operasyonlar", "label": "Dış Operasyonlar", "fieldtype": "Small Text", "insert_after": "artegon_tedarik_yontemi"},
				{"fieldname": "artegon_teknik_resim_pdf", "label": "Teknik Resim PDF", "fieldtype": "Attach", "insert_after": "image"},
			],
			"Sales Order": [
				{"fieldname": "artegon_otomasyon_ozeti", "label": "Otomasyon Özeti", "fieldtype": "Small Text", "read_only": 1, "insert_after": "set_warehouse"}
			],
			"Material Request": [
				{"fieldname": "custom_artegon_kaynak_siparis", "label": "Kaynak Sipariş", "fieldtype": "Link", "options": "Sales Order", "insert_after": "customer"}
			],
		},
		update=True,
	)


def _ensure_item(item_code: str, item_name: str, item_group: str, standard_rate: float, product_type: str, supply_mode: str, is_sales_item: int, is_purchase_item: int, external_ops: str = "") -> None:
	if frappe.db.exists("Item", item_code):
		doc = frappe.get_doc("Item", item_code)
	else:
		doc = frappe.get_doc({"doctype": "Item", "item_code": item_code, "item_name": item_name})
	doc.item_name = item_name
	doc.item_group = item_group
	doc.stock_uom = "Adet"
	doc.standard_rate = standard_rate
	doc.is_stock_item = 1
	doc.is_sales_item = is_sales_item
	doc.is_purchase_item = is_purchase_item
	doc.include_item_in_manufacturing = 1
	doc.default_material_request_type = "Purchase" if supply_mode == "Satın Alma" else "Manufacture"
	doc.description = f"{item_name} demo kaydı"
	doc.artegon_urun_tipi = product_type
	doc.artegon_tedarik_yontemi = supply_mode
	doc.artegon_dis_operasyonlar = external_ops
	default_row = None
	for row in doc.item_defaults:
		if row.company == COMPANY:
			default_row = row
			break
	if not default_row:
		default_row = doc.append("item_defaults", {})
	default_row.company = COMPANY
	default_row.default_warehouse = _wh("Hammadde Deposu") if product_type in {"Malzeme", "Ambalaj"} else _wh("Bitmiş Ürünler")
	default_row.default_price_list = BUYING_PRICE_LIST if is_purchase_item else SELLING_PRICE_LIST
	if supply_mode == "Satın Alma":
		default_row.default_supplier = _party_docname("Supplier", SUPPLIERS[0])
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _ensure_item_price(item_code: str, price_list: str, rate: float, buying: int, selling: int, supplier: str | None = None) -> None:
	supplier_name = _party_docname("Supplier", supplier) if supplier else None
	filters = {"item_code": item_code, "price_list": price_list}
	if supplier_name:
		filters["supplier"] = supplier_name
	existing = frappe.get_all("Item Price", filters=filters, pluck="name")
	if existing:
		doc = frappe.get_doc("Item Price", existing[0])
	else:
		doc = frappe.get_doc({"doctype": "Item Price", "item_code": item_code, "price_list": price_list})
	doc.currency = "TRY"
	doc.price_list_rate = rate
	doc.buying = buying
	doc.selling = selling
	if supplier_name:
		doc.supplier = supplier_name
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _make_pdf(title: str, filename: str) -> bytes:
	PDF_DIR.mkdir(parents=True, exist_ok=True)
	path = PDF_DIR / filename
	if not path.exists():
		writer = PdfWriter()
		writer.add_blank_page(width=595, height=842)
		writer.add_metadata({"/Title": title, "/Author": "ARTEGON"})
		with path.open("wb") as handle:
			writer.write(handle)
	return path.read_bytes()


def _attach_pdf(item_code: str, title: str) -> None:
	existing_files = frappe.get_all(
		"File",
		filters={"attached_to_doctype": "Item", "attached_to_name": item_code, "file_name": f"{item_code}.pdf"},
		fields=["name", "file_url"],
		order_by="creation asc",
	)
	if existing_files:
		frappe.db.set_value("Item", item_code, "artegon_teknik_resim_pdf", existing_files[0].file_url, update_modified=False)
		for extra_file in existing_files[1:]:
			frappe.delete_doc("File", extra_file.name, ignore_permissions=True, force=1)
		return
	file_doc = save_file(f"{item_code}.pdf", _make_pdf(title, f"{item_code}.pdf"), "Item", item_code, is_private=1)
	frappe.db.set_value("Item", item_code, "artegon_teknik_resim_pdf", file_doc.file_url, update_modified=False)


def _ensure_bom(item_code: str) -> None:
	if frappe.get_all("BOM", filters={"item": item_code, "is_default": 1, "docstatus": 1}, pluck="name"):
		return
	doc = frappe.get_doc({"doctype": "BOM", "company": COMPANY, "item": item_code, "quantity": 1, "is_active": 1, "is_default": 1, "with_operations": 1, "currency": "TRY", "buying_price_list": BUYING_PRICE_LIST})
	for component_code, qty in BOM_COMPONENTS[item_code]:
		doc.append("items", {"item_code": component_code, "qty": qty, "uom": "Adet", "stock_uom": "Adet", "stock_qty": qty, "include_item_in_manufacturing": 1})
	for operation_name, mins in BOM_OPERATIONS.get(item_code, []):
		doc.append("operations", {"operation": operation_name, "workstation": OPERATIONS[operation_name], "time_in_mins": mins})
	doc.insert(ignore_permissions=True)
	doc.submit()
	frappe.db.set_value("Item", item_code, "default_bom", doc.name, update_modified=False)


def _stock_exists(remarks: str) -> bool:
	return bool(frappe.db.exists("Stock Entry", {"stock_entry_type": "Material Receipt", "remarks": remarks, "docstatus": 1}))


def _make_stock_entry(target_warehouse: str, item_rows: list[tuple[str, float]]) -> None:
	remarks = f"ARTEGON demo stok yükleme - {target_warehouse}"
	if _stock_exists(remarks):
		return
	entry = frappe.get_doc({"doctype": "Stock Entry", "stock_entry_type": "Material Receipt", "company": COMPANY, "to_warehouse": target_warehouse, "remarks": remarks})
	for item_code, qty in item_rows:
		if flt(qty) <= 0:
			continue
		entry.append("items", {"item_code": item_code, "qty": qty, "uom": "Adet", "stock_uom": "Adet", "conversion_factor": 1, "t_warehouse": target_warehouse, "basic_rate": flt(frappe.db.get_value("Item", item_code, "standard_rate")) or 1})
	entry.insert(ignore_permissions=True)
	entry.submit()


def _ensure_project_and_tasks() -> None:
	project_name = "ARTEGON Pilot Sipariş Akışı"
	existing = frappe.get_all("Project", filters={"project_name": project_name}, pluck="name")
	project = frappe.get_doc("Project", existing[0]) if existing else frappe.get_doc({"doctype": "Project", "project_name": project_name, "status": "Open", "company": COMPANY}).insert(ignore_permissions=True)
	for subject, owner in [
		("Model kartları ve teknik resim yükleme", "teknik@artegon.com.tr"),
		("Müşteri siparişi girişi", "satis@artegon.com.tr"),
		("Depo stok kontrolü ve eksik bildirimi", "depo@artegon.com.tr"),
		("Eksik malzeme tedarik planı", "satinalma@artegon.com.tr"),
		("İş emri ve üretim planlama", "uretim@artegon.com.tr"),
		("Giriş kalite kontrol planı", "kalite@artegon.com.tr"),
		("Montaj ve fonksiyon testi", "montaj@artegon.com.tr"),
		("Paketleme ve sevkiyat onayı", "paketleme@artegon.com.tr"),
	]:
		if frappe.db.exists("Task", {"subject": subject, "project": project.name}):
			continue
		task = frappe.get_doc({"doctype": "Task", "subject": subject, "project": project.name, "status": "Open", "exp_start_date": nowdate(), "exp_end_date": nowdate()}).insert(ignore_permissions=True)
		frappe.get_doc({"doctype": "ToDo", "allocated_to": owner, "reference_type": "Task", "reference_name": task.name, "description": f"{subject} görevini gözden geçir."}).insert(ignore_permissions=True)


def _ensure_demo_sales_order() -> str:
	existing = frappe.get_all("Sales Order", filters={"po_no": "ART-DEMO-SIPARIS-001"}, pluck="name")
	if existing:
		return existing[0]
	order = frappe.get_doc({"doctype": "Sales Order", "company": COMPANY, "customer": _party_docname("Customer", CUSTOMERS[0]), "transaction_date": nowdate(), "delivery_date": nowdate(), "currency": "TRY", "selling_price_list": SELLING_PRICE_LIST, "po_no": "ART-DEMO-SIPARIS-001", "items": [{"item_code": "MDL-A100", "qty": 6, "rate": 17500.0, "delivery_date": nowdate(), "warehouse": _wh("Bitmiş Ürünler")}, {"item_code": "MDL-B200", "qty": 4, "rate": 24800.0, "delivery_date": nowdate(), "warehouse": _wh("Bitmiş Ürünler")}]}).insert(ignore_permissions=True)
	order.submit()
	return order.name


def bootstrap_demo():
	_set_single("System Settings", {"language": "tr", "country": "Türkiye", "time_zone": "Europe/Istanbul"})
	_ensure_custom_fields()
	_ensure_uom("Adet")
	for department in DEPARTMENTS:
		_ensure_department(department)
	for row in DEMO_USERS:
		_ensure_user(row)
	root = _wh("Tüm Depolar")
	for label in ["Hammadde Deposu", "Kalite Kontrol Bekleme", "Karantina", "Red Deposu", "Sevkiyata Hazır", "Montaj Hattı"]:
		_ensure_warehouse(label, root)
	_ensure_price_list(BUYING_PRICE_LIST, 1, 0)
	_ensure_price_list(SELLING_PRICE_LIST, 0, 1)
	company = frappe.get_doc("Company", COMPANY)
	company.default_currency = "TRY"
	company.country = "Türkiye"
	cash_account = f"100.01 - TL KASA - {_abbr()}"
	payable_account = f"320.01 - SATICILAR TRY - {_abbr()}"
	for df in frappe.get_meta("Company").fields:
		if df.fieldtype == "Link" and df.options == "Account":
			account_name = getattr(company, df.fieldname, None)
			updated_account = _ensure_account_currency(account_name, "TRY")
			if updated_account:
				setattr(company, df.fieldname, updated_account)
	receivable_account = company.default_receivable_account
	inventory_account = company.default_inventory_account
	payable_account = _ensure_account_currency(payable_account, "TRY") or company.default_payable_account
	if frappe.db.exists("Account", cash_account):
		company.default_cash_account = _ensure_account_currency(cash_account, "TRY") or ""
	else:
		company.default_cash_account = ""
	if receivable_account:
		company.default_receivable_account = receivable_account
	if inventory_account:
		company.default_inventory_account = inventory_account
	if payable_account:
		company.default_payable_account = payable_account
	company.save(ignore_permissions=True)
	frappe.db.set_single_value("Global Defaults", "default_company", COMPANY)
	frappe.db.set_single_value("Global Defaults", "default_currency", "TRY")
	frappe.db.set_value("User", "Administrator", "language", "tr", update_modified=False)
	_set_single("Selling Settings", {"selling_price_list": SELLING_PRICE_LIST, "cust_master_name": "Naming Series"})
	_set_single("Buying Settings", {"buying_price_list": BUYING_PRICE_LIST, "supp_master_name": "Naming Series"})
	_set_single("Stock Settings", {"default_warehouse": _wh("Hammadde Deposu"), "stock_uom": "Adet", "allow_negative_stock": 0})
	_set_single("Manufacturing Settings", {"allow_editing_of_items_and_quantities_in_work_order": 1})
	for supplier in SUPPLIERS:
		_ensure_party("Supplier", supplier)
	for customer in CUSTOMERS:
		_ensure_party("Customer", customer)
	for group_name, parent in [("ARTEGON Modeller", "Products"), ("ARTEGON Yarı Mamuller", "Sub Assemblies"), ("ARTEGON Malzemeler", "Raw Material"), ("ARTEGON Ambalaj", "Consumable")]:
		_ensure_item_group(group_name, parent)
	for workstation_name, capacity, rate in WORKSTATIONS:
		_ensure_workstation(workstation_name, capacity, rate)
	for operation_name, workstation in OPERATIONS.items():
		_ensure_operation(operation_name, workstation)
	for item_code, item_name, rate in PURCHASED_MATERIALS:
		_ensure_item(item_code, item_name, "ARTEGON Malzemeler", rate, "Malzeme", "Satın Alma", 0, 1)
		for idx, supplier in enumerate(SUPPLIERS):
			_ensure_item_price(item_code, BUYING_PRICE_LIST, round(rate * (1 + (idx * 0.07)), 2), 1, 0, supplier)
	for item_code, item_name, rate in PACKAGING_MATERIALS:
		_ensure_item(item_code, item_name, "ARTEGON Ambalaj", rate, "Ambalaj", "Satın Alma", 0, 1)
		for idx, supplier in enumerate(SUPPLIERS[:2]):
			_ensure_item_price(item_code, BUYING_PRICE_LIST, round(rate * (1 + (idx * 0.05)), 2), 1, 0, supplier)
	for item_code, item_name, rate, supply_mode, external_ops in SEMI_FINISHED:
		_ensure_item(item_code, item_name, "ARTEGON Yarı Mamuller", rate, "Yarı Mamul", supply_mode, 0, 0, external_ops)
		_attach_pdf(item_code, item_name)
	for item_code, item_name, rate in MODELS:
		_ensure_item(item_code, item_name, "ARTEGON Modeller", rate, "Model", "İç Üretim", 1, 0)
		_ensure_item_price(item_code, SELLING_PRICE_LIST, rate, 0, 1)
		_attach_pdf(item_code, item_name)
	for item_code in BOM_COMPONENTS:
		_ensure_bom(item_code)
	raw_rows, semi_rows, fg_rows = [], [], []
	for item_code, qty in OPENING_STOCK.items():
		if item_code.startswith("MDL-"):
			fg_rows.append((item_code, qty))
		elif item_code.startswith("YRM-"):
			semi_rows.append((item_code, qty))
		else:
			raw_rows.append((item_code, qty))
	_make_stock_entry(_wh("Hammadde Deposu"), raw_rows)
	_make_stock_entry(_wh("Devam Eden İşler"), semi_rows)
	_make_stock_entry(_wh("Bitmiş Ürünler"), fg_rows)
	_ensure_project_and_tasks()
	order_name = _ensure_demo_sales_order()
	ui_result = apply_simplified_ui()
	frappe.clear_cache()
	frappe.db.commit()
	return {"company": COMPANY, "models": len(MODELS), "materials": len(PURCHASED_MATERIALS) + len(PACKAGING_MATERIALS) + len(SEMI_FINISHED), "demo_sales_order": order_name, "workspace": ui_result["workspace"]}
