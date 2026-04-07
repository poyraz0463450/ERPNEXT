from __future__ import annotations

import frappe
from frappe.utils import add_days, flt, nowdate


COMPANY = "ARTEGON"
PURCHASE_USER = "satinalma@artegon.com.tr"
PRODUCTION_USER = "uretim@artegon.com.tr"


def _warehouse_map(company: str) -> dict[str, str]:
	abbr = frappe.db.get_value("Company", company, "abbr") or "ART"
	return {
		"raw": f"Hammadde Deposu - {abbr}",
		"wip": f"Devam Eden İşler - {abbr}",
		"fg": f"Bitmiş Ürünler - {abbr}",
		"shipping": f"Sevkiyata Hazır - {abbr}",
	}


def _qty_in_warehouses(item_code: str, warehouses: list[str]) -> float:
	if not warehouses:
		return 0.0

	result = frappe.db.sql(
		"""
		select coalesce(sum(actual_qty), 0)
		from `tabBin`
		where item_code = %s and warehouse in %s
		""",
		(item_code, tuple(warehouses)),
	)
	return flt(result[0][0]) if result else 0.0


def _cheapest_supplier(item_code: str) -> tuple[str | None, float]:
	for row in frappe.get_all(
		"Item Price",
		filters={"item_code": item_code, "buying": 1},
		fields=["supplier", "price_list_rate"],
		order_by="price_list_rate asc",
	):
		if row.supplier:
			return row.supplier, flt(row.price_list_rate)
	return None, 0.0


def _assign_todo(user: str | None, description: str, reference_doctype: str, reference_name: str) -> None:
	if not user or not frappe.db.exists("User", user):
		return

	if frappe.db.exists(
		"ToDo",
		{
			"allocated_to": user,
			"reference_type": reference_doctype,
			"reference_name": reference_name,
			"description": description,
			"status": ("!=", "Cancelled"),
		},
	):
		return

	frappe.get_doc(
		{
			"doctype": "ToDo",
			"allocated_to": user,
			"reference_type": reference_doctype,
			"reference_name": reference_name,
			"description": description,
		}
	).insert(ignore_permissions=True)


def _ensure_work_order(doc, item_code: str, qty: float, bom_no: str, warehouses: dict[str, str], sales_order_item: str | None = None) -> str:
	existing = frappe.get_all(
		"Work Order",
		filters={
			"sales_order": doc.name,
			"production_item": item_code,
			"bom_no": bom_no,
			"docstatus": ("!=", 2),
		},
		fields=["name", "qty"],
		order_by="creation asc",
	)
	if existing:
		work_order = frappe.get_doc("Work Order", existing[0].name)
		if flt(work_order.qty) < flt(qty):
			work_order.qty = flt(qty)
			work_order.save(ignore_permissions=True)
		return work_order.name

	work_order = frappe.get_doc(
		{
			"doctype": "Work Order",
			"company": doc.company,
			"production_item": item_code,
			"item": item_code,
			"bom_no": bom_no,
			"qty": flt(qty),
			"sales_order": doc.name,
			"sales_order_item": sales_order_item,
			"source_warehouse": warehouses["raw"],
			"wip_warehouse": warehouses["wip"],
			"fg_warehouse": warehouses["fg"],
			"use_multi_level_bom": 1,
			"planned_start_date": nowdate(),
			"planned_end_date": add_days(nowdate(), 3),
		}
	).insert(ignore_permissions=True)
	return work_order.name


def _merge_shortage(target: dict[str, dict], item_code: str, qty: float, schedule_date: str, bom_no: str | None = None) -> None:
	if item_code not in target:
		description = frappe.db.get_value("Item", item_code, "description") or frappe.db.get_value("Item", item_code, "item_name")
		uom = frappe.db.get_value("Item", item_code, "stock_uom") or "Adet"
		supplier, rate = _cheapest_supplier(item_code)
		target[item_code] = {
			"qty": 0.0,
			"schedule_date": schedule_date,
			"description": description or item_code,
			"uom": uom,
			"supplier": supplier,
			"rate": rate,
			"bom_no": bom_no,
		}

	target[item_code]["qty"] = flt(target[item_code]["qty"]) + flt(qty)
	target[item_code]["schedule_date"] = max(target[item_code]["schedule_date"], schedule_date)
	if bom_no and not target[item_code].get("bom_no"):
		target[item_code]["bom_no"] = bom_no


def _collect_component_shortages(
	bom_no: str,
	required_qty: float,
	warehouses: dict[str, str],
	purchase_shortages: dict[str, dict],
	manufacture_shortages: dict[str, dict],
	operation_notes: list[str],
) -> None:
	for row in frappe.get_all(
		"BOM Explosion Item",
		filters={"parent": bom_no},
		fields=["item_code", "stock_qty", "source_warehouse"],
	):
		item_code = row.item_code
		route = frappe.db.get_value("Item", item_code, "artegon_tedarik_yontemi") or "Satın Alma"
		child_bom = frappe.db.get_value("Item", item_code, "default_bom")
		required_component_qty = flt(row.stock_qty) * flt(required_qty)
		lookup_warehouses = [row.source_warehouse] if row.source_warehouse else [warehouses["raw"], warehouses["wip"], warehouses["fg"]]
		available_qty = _qty_in_warehouses(item_code, lookup_warehouses)
		shortage_qty = max(required_component_qty - available_qty, 0)
		if shortage_qty <= 0:
			continue

		external_ops = frappe.db.get_value("Item", item_code, "artegon_dis_operasyonlar")
		if external_ops:
			operation_notes.append(f"{item_code}: {external_ops}")

		if route == "İç Üretim" and child_bom:
			_merge_shortage(manufacture_shortages, item_code, shortage_qty, add_days(nowdate(), 2), child_bom)
		else:
			_merge_shortage(purchase_shortages, item_code, shortage_qty, add_days(nowdate(), 2), bom_no)


def _create_purchase_material_request(doc, shortages: dict[str, dict], warehouses: dict[str, str]) -> str:
	existing = frappe.get_all(
		"Material Request",
		filters={
			"docstatus": ("!=", 2),
			"material_request_type": "Purchase",
			"custom_artegon_kaynak_siparis": doc.name,
		},
		pluck="name",
	)
	if existing:
		return existing[0]

	request = frappe.get_doc(
		{
			"doctype": "Material Request",
			"company": doc.company,
			"material_request_type": "Purchase",
			"transaction_date": nowdate(),
			"custom_artegon_kaynak_siparis": doc.name,
		}
	)

	for item_code in sorted(shortages):
		row = shortages[item_code]
		supplier_note = ""
		if row.get("supplier"):
			supplier_note = f"\nÖnerilen tedarikçi: {row['supplier']} ({row['rate']} TL)"
		request.append(
			"items",
			{
				"item_code": item_code,
				"qty": flt(row["qty"]),
				"schedule_date": row["schedule_date"],
				"warehouse": warehouses["raw"],
				"uom": row["uom"],
				"stock_uom": row["uom"],
				"sales_order": doc.name,
				"bom_no": row.get("bom_no"),
				"description": f"{row['description']}{supplier_note}",
			},
		)

	request.insert(ignore_permissions=True)
	return request.name


def handle_sales_order_submit(doc, method=None):
	if doc.doctype != "Sales Order":
		return

	warehouses = _warehouse_map(doc.company or COMPANY)
	purchase_shortages: dict[str, dict] = {}
	manufacture_shortages: dict[str, dict] = {}
	notes: list[str] = []
	operation_notes: list[str] = []
	work_orders: list[str] = []

	for item in doc.items:
		if not item.item_code:
			continue

		item_code = item.item_code
		bom_no = item.bom_no or frappe.db.get_value("Item", item_code, "default_bom")
		finished_available = _qty_in_warehouses(item_code, [warehouses["fg"], warehouses["shipping"]])
		manufacture_qty = max(flt(item.qty) - finished_available, 0)

		if manufacture_qty <= 0:
			notes.append(f"{item_code}: bitmiş ürün stoğu yeterli.")
			continue

		if bom_no:
			work_order_name = _ensure_work_order(doc, item_code, manufacture_qty, bom_no, warehouses, item.name)
			work_orders.append(work_order_name)
			notes.append(f"{item_code}: {manufacture_qty} adet için iş emri oluşturuldu ({work_order_name}).")
			_collect_component_shortages(bom_no, manufacture_qty, warehouses, purchase_shortages, manufacture_shortages, operation_notes)
		else:
			_merge_shortage(purchase_shortages, item_code, manufacture_qty, item.delivery_date or add_days(nowdate(), 3))
			notes.append(f"{item_code}: varsayılan BOM olmadığı için satın alma listesine eklendi.")

	for item_code, row in sorted(manufacture_shortages.items()):
		work_order_name = _ensure_work_order(doc, item_code, row["qty"], row["bom_no"], warehouses)
		work_orders.append(work_order_name)
		notes.append(f"{item_code}: yarı mamul açığı için iş emri oluşturuldu ({work_order_name}).")

	material_request_name = None
	if purchase_shortages:
		material_request_name = _create_purchase_material_request(doc, purchase_shortages, warehouses)
		notes.append(f"Satın alma için malzeme talebi oluşturuldu ({material_request_name}).")

	if operation_notes:
		notes.append("Dış operasyon takibi gereken kalemler:")
		notes.extend(operation_notes)

	summary = "\n".join(notes) if notes else "Sipariş otomasyonu çalıştı, ek işlem gerekmedi."
	if frappe.get_meta("Sales Order").has_field("artegon_otomasyon_ozeti"):
		doc.db_set("artegon_otomasyon_ozeti", summary, update_modified=False)
	doc.add_comment("Comment", summary)

	if material_request_name:
		_assign_todo(
			PURCHASE_USER,
			f"{doc.name} siparişi için satın alma ve tedarikçi karşılaştırmasını tamamla.",
			"Material Request",
			material_request_name,
		)

	for work_order_name in work_orders:
		_assign_todo(
			PRODUCTION_USER,
			f"{doc.name} siparişi için iş emrini planla ve üretime başlat.",
			"Work Order",
			work_order_name,
		)
