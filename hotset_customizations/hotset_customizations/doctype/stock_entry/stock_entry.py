# -*- coding: utf-8 -*-
# Copyright (c) 2020, seabridge_app and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Company(Document):
	pass

@frappe.whitelist()
def get_serial_no(item,warehouse):
    query= frappe.db.sql("""
                select name,available_qty
                from `tabSerial No`
                where item_code = %s and stock_warehouse=%s and status not in ("Inactive","Expired") and available_qty>0 order by creation
        """, (item,warehouse))
    return query


def set_serial_no_status(doc,method):
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        for item in doc.items:
            serial_no_list=[]
            if item.serial_no:
                serial_no=item.serial_no
                item_serial_nos=serial_no.split("\n")
                length = len(item_serial_nos)
                for i in range(length):
                    serial_no_list.append(item_serial_nos[i])
                
                list_length=len(serial_no_list)
                item_qty=item.qty
                for i in range(list_length):
                    sn_doc=frappe.get_doc("Serial No",serial_no_list[i])
                    if sn_doc.available_qty>=item_qty:
                        available_qty=sn_doc.available_qty-item_qty
                        sn_doc.db_set('available_qty',available_qty)
                    else:
                        item_qty=item_qty-sn_doc.available_qty
                        sn_doc.db_set('available_qty',0)
                    frappe.db.commit()

def before_save(doc,method):
    if doc.stock_entry_type=="Manufacture":
        serial_no_list=""
        stock_entry_list=frappe.db.get_list("Stock Entry",filters={'work_order':doc.work_order,'stock_entry_type':"Material Transfer for Manufacture"},fields={'*'})
        if stock_entry_list:
            for stock_entry in stock_entry_list:
                se_doc=frappe.get_doc("Stock Entry",stock_entry.name)
                for item in doc.items:
                    serial_no_list=""
                    stock_entry_item_list=frappe.db.get_list("Stock Entry Detail",filters={'parent':se_doc.name,'item_code':item.item_code},fields={'*'})
                    if stock_entry_item_list:
                        for se_item in stock_entry_item_list:
                            serial_no_list=serial_no_list+str(se_item.serial_no)+"\n"
                    if serial_no_list:
                        item.serial_no=serial_no_list

    item_with_stock=[]
    items_removed=""
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        for item in doc.items:
            item_data=[item.item_code,item.s_warehouse]
            projected_qty = frappe.db.get_value('Bin', {'item_code': item.item_code,'warehouse':item.s_warehouse}, 'projected_qty')
            if projected_qty>=item.qty:
                  item_with_stock.append(item_data)
    for item_stock in item_with_stock:
        for item in doc.items:
            if item.item_code==item_stock[0] and item.s_warehouse==item_stock[1]:
                if items_removed!="":
                    items_removed=items_removed+", "
                items_removed=items_removed+str(item.item_code)+"-"+str(item.s_warehouse)+" "
                doc.remove(item)
    if items_removed!="":
        frappe.msgprint("Removed items: "+items_removed+"as Stock available in the warehouse")
