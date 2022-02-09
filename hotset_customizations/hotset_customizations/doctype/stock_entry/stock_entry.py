# -*- coding: utf-8 -*-
# Copyright (c) 2020, seabridge_app and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Company(Document):
	pass

@frappe.whitelist()
def get_serial_no(item,warehouse,qty):
    item_doc=frappe.get_doc("Item",item)

    uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item,'uom':['!=',item_doc.stock_uom]},fields={'*'})
    stock_qty=float(qty)/float(uom_list[0].conversion_factor)
    query= frappe.db.sql("""
                select name,available_qty
                from `tabSerial No`
                where item_code = %s and stock_warehouse=%s and status not in ("Inactive","Expired") and available_qty>%s order by creation
        """, (item,warehouse,stock_qty))
    return query


def set_serial_no_status(doc,method):
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        for item in doc.items:
            if item.serial_no:
                sn_doc=frappe.get_doc("Serial No",item.serial_no)
                sn_doc.db_set('stock_warehouse',item.t_warehouse)
                frappe.db.commit()

    if doc.stock_entry_type=="Manufacture":
        for item in doc.items:
            if item.is_finished_item!=1:
                serial_no_list=[]
                item_doc=frappe.get_doc("Item",item.item_code)
                uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
                stock_qty=float(item.qty)/float(uom_list[0].conversion_factor)
                total_qty=stock_qty
                serial_no=item.serial_no
                item_serial_nos=serial_no.split("\n")
                length = len(item_serial_nos)
                for i in range(length):
                    serial_no_list.append(item_serial_nos[i])
                list_length=len(serial_no_list)
                for i in range(list_length):
                    if serial_no_list[i]!="":
                        sn_doc=frappe.get_doc("Serial No",serial_no_list[i])
                        if sn_doc.available_qty>=0:
                            if sn_doc.available_qty<total_qty:
                                available_qty=0
                                sn_doc.db_set('available_qty',available_qty)
                                sn_doc.add_comment('Comment','Used qty: '+str(sn_doc.available_qty)+' for transaction with Stock Entry: '+doc.name)
                                total_qty=total_qty-sn_doc.available_qty
                            else:
                                available_qty=sn_doc.available_qty-total_qty
                                sn_doc.db_set('available_qty',available_qty)
                                sn_doc.add_comment('Comment','Used qty: '+str(total_qty)+' for transaction with Stock Entry: '+doc.name)

                            frappe.db.commit()
def before_save(doc,method):
    item_with_stock=[]
    items_removed=""
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        for item in doc.items:
            item_data=[item.item_code,item.t_warehouse]
            projected_qty = frappe.db.get_value('Bin', {'item_code': item.item_code,'warehouse':item.t_warehouse}, 'projected_qty')
            if projected_qty:
                if float(projected_qty)>=float(item.required_qty):
                    item_with_stock.append(item_data)
    for item_stock in item_with_stock:
        for item in doc.items:
            if item.item_code==item_stock[0] and item.t_warehouse==item_stock[1]:
                if items_removed!="":
                    items_removed=items_removed+", "
                items_removed=items_removed+str(item.item_code)+"-"+str(item.t_warehouse)+" "
                doc.remove(item)
    if items_removed!="":
        for item in doc.items:
            item_doc=frappe.get_doc("Item",item.item_code)

            uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
            stock_qty=float(item.required_qty)/float(uom_list[0].conversion_factor)
            query= frappe.db.sql("""
                        select name,available_qty
                        from `tabSerial No`
                        where item_code = %s and stock_warehouse=%s and status not in ("Inactive","Expired") and available_qty>%s order by creation
                """, (item.item_code,item.s_warehouse,stock_qty))
            item.serial_no=query[0][0]
            item.qty=float(query[0][1])*float(uom_list[0].conversion_factor)
        frappe.msgprint("Removed items: "+items_removed+"as Stock available in the warehouse")
