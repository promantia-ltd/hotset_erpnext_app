# -*- coding: utf-8 -*-
# Copyright (c) 2020, seabridge_app and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Company(Document):
	pass

def after_submit(doc,method):
    serial_no_list=frappe.db.get_list("Serial No",filters={'purchase_document_type':'Purchase Receipt','purchase_document_no': doc.name},fields={'*'})
    for no in serial_no_list:
        serial_no_doc=frappe.get_doc("Serial No",no.name)
        item_doc=frappe.get_doc("Item",no.item_code)
        uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'uom': ['!=',item_doc.stock_uom],'parent': item_doc.item_code},fields={'*'})
        serial_no_doc.db_set('available_qty', 1/uom_list[0].conversion_factor)
        serial_no_doc.db_set('secondary_uom', uom_list[0].uom)
        serial_no_doc.db_set('stock_warehouse',serial_no_doc.warehouse)
        frappe.db.commit()

