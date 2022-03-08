# -*- coding: utf-8 -*-
# Copyright (c) 2020, seabridge_app and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Company(Document):
	pass

@frappe.whitelist()
def reserve_qty(item,warehouse,item_qty,work_order,bom_qty,wo_qty):
    qty=float(item_qty)*float(wo_qty)/float(bom_qty)
    query= frappe.db.sql("""
                select name
                from `tabSerial No`
                where item_code = %s and stock_warehouse=%s and status not in ("Inactive","Expired") and available_qty>=%s order by creation
        """, (item,warehouse,qty))
    if query:
        serial_no=query[0][0]
        sn_doc=frappe.get_doc("Serial No",serial_no)
        stock_detail_doc=frappe.db.get_value('Stock Details',{'parent':sn_doc.name,'work_order': work_order},'name')
        sn_doc.db_set('stock_warehouse',warehouse)
        sn_doc.db_set('available_qty',sn_doc.available_qty-qty)
        sn_doc.save(ignore_permissions=True)
        if stock_detail_doc:
                    stock_detail_doc=frappe.get_doc("Stock Details",stock_detail_doc)
                    reserved_qty=stock_detail_doc.reserved_qty+qty
                    stock_detail_doc.db_set('reserved_qty',reserved_qty)
        else:
                    sn_doc.append('stock_details', {
                        'work_order':work_order,
                        'warehouse':warehouse,
                        'reserved_qty':qty,
                        'consumed_qty':0
                    })
                    sn_doc.save(ignore_permissions=True)
        frappe.db.commit()
        comment=warehouse+" : <a href='/app/serial-no/"+serial_no+"'>"+serial_no+"</a> : "+str(qty)+" "+sn_doc.secondary_uom+"<br>"
        return comment

@frappe.whitelist()
def add_comment(doctype,docname,comment):
    wo_doc=frappe.get_doc(doctype,docname)
    wo_doc.add_comment('Comment',comment)
