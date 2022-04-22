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
    if stock_qty<=1/float(uom_list[0].conversion_factor):
        query= frappe.db.sql("""
                select name,available_qty
                from `tabSerial No`
                where item_code = %s and stock_warehouse=%s and status not in ("Inactive","Expired") and available_qty>=%s order by creation
        """, (item,warehouse,stock_qty))
    else:
        frappe.throw('Crossed the Serial No limit. Maximum: '+(1/float(uom_list[0].conversion_factor))+' Expected: '+stock_qty)
    return query

@frappe.whitelist()
def get_item_serial_no(item,warehouse,qty,work_order):
    item_doc=frappe.get_doc("Item",item)

    uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item,'uom':['!=',item_doc.stock_uom]},fields={'*'})
    
    stock_qty=float(qty)/float(uom_list[0].conversion_factor)
    if stock_qty:
        query= frappe.db.sql("""
                select sd.parent,available_qty
                from `tabSerial No` s,`tabStock Details` sd
                where s.name=sd.parent and s.item_code = %s and sd.warehouse=%s and s.status not in ("Inactive","Expired") and sd.reserved_qty>=%s and sd.work_order=%s order by s.creation
        """, (item,warehouse,round(stock_qty,2),work_order))
    else:
        frappe.throw('Crossed the Serial No limit. Maximum: '+(1/float(uom_list[0].conversion_factor))+' Expected: '+stock_qty)
    return query

def before_submit(doc,method):
    if doc.stock_entry_type=="Manufacture":
        for item in doc.items:
                if item.is_finished_item!=1:
                    serial_no=item.serial_no
                    if not serial_no:
                        frappe.throw('Please Set appropriate Serial No for item at row '+str(item.idx)) 



def set_serial_no_status(doc,method):
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        comment="<b>Stock Reserved Successfully</b><br>Assigned Spools:<br>"
        for item in doc.items:
            if item.serial_no:
                item_doc=frappe.get_doc("Item",item.item_code)
                uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
                stock_qty=float(item.required_qty)/float(uom_list[0].conversion_factor)
                sn_doc=frappe.get_doc("Serial No",item.serial_no)
                stock_detail_doc=frappe.db.get_value('Stock Details',{'parent':sn_doc.name,'work_order': doc.work_order},'name')
                sn_doc.db_set('stock_warehouse',item.t_warehouse)
                sn_doc.db_set('available_qty',sn_doc.available_qty-stock_qty)
                sn_doc.save(ignore_permissions=True)
                if stock_detail_doc:
                    stock_detail_doc=frappe.get_doc("Stock Details",stock_detail_doc)
                    reserved_qty=stock_detail_doc.reserved_qty+stock_qty
                    stock_detail_doc.db_set('reserved_qty',reserved_qty)
                else:
                    sn_doc.append('stock_details', {
                        'work_order':doc.work_order,
                        'warehouse':item.t_warehouse,
                        'reserved_qty':stock_qty,
                        'consumed_qty':0
                    })
                    sn_doc.save(ignore_permissions=True)
                
                frappe.db.commit()
                comment=comment+item.t_warehouse+" : <a href='/app/serial-no/"+item.serial_no+"'>"+item.serial_no+"</a> : "+str(round(stock_qty,2))+" "+sn_doc.secondary_uom+"<br>"
        doc.add_comment('Comment',comment)

    if doc.stock_entry_type=="Manufacture":
        if doc.work_order:
            for item in doc.items:
                if item.is_finished_item!=1:
                    serial_no_list=[]
                    item_doc=frappe.get_doc("Item",item.item_code)
                    uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
                    if uom_list[0].uom!=item.uom:
                        stock_qty=float(item.qty)/float(uom_list[0].conversion_factor)
                    else:
                        stock_qty=item.qty
                    total_qty=stock_qty
                    serial_no=item.serial_no
                    if serial_no:
                        item_serial_nos=serial_no.split("\n")
                        length = len(item_serial_nos)
                        for i in range(length):
                            serial_no_list.append(item_serial_nos[i])
                        list_length=len(serial_no_list)
                        for i in range(list_length):
                            if serial_no_list[i]!="":
                                sn_doc=frappe.get_doc("Serial No",serial_no_list[i])
                                stock_detail_doc=frappe.db.get_value('Stock Details',{'parent':sn_doc.name,'work_order': doc.work_order},'name')
                                if stock_detail_doc:
                                    stock_detail_doc=frappe.get_doc("Stock Details",stock_detail_doc)
                                    stock_detail_doc.db_set('reserved_qty',stock_detail_doc.reserved_qty-stock_qty)
                                    stock_detail_doc.db_set('consumed_qty',stock_detail_doc.consumed_qty+stock_qty)
                                    sn_doc.add_comment('Comment','Used qty: '+str(round(stock_qty, 2))+' for transaction with Stock Entry: '+doc.name)
                                frappe.db.commit()
                    else:
                        frappe.throw('Please Set appropriate Serial No for item at row '+str(item.idx)) 
        else:
            for item in doc.items:
                if item.is_finished_item!=1:
                    serial_no_list=[]
                    item_doc=frappe.get_doc("Item",item.item_code)
                    uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
                    if uom_list[0].uom!=item.uom:
                        stock_qty=float(item.qty)/float(uom_list[0].conversion_factor)
                    else:
                        stock_qty=item.qty
                    total_qty=stock_qty
                    serial_no=item.serial_no
                    if serial_no:
                        item_serial_nos=serial_no.split("\n")
                        length = len(item_serial_nos)
                        for i in range(length):
                            serial_no_list.append(item_serial_nos[i])
                        list_length=len(serial_no_list)
                        for i in range(list_length):
                            if serial_no_list[i]!="":
                                sn_doc=frappe.get_doc("Serial No",serial_no_list[i])
                                sn_doc.db_set('available_qty',sn_doc.available_qty-stock_qty)
                                sn_doc.add_comment('Comment','Used qty: '+str(round(stock_qty, 2))+' for transaction with Stock Entry: '+doc.name)
                                frappe.db.commit()
                    else:
                        frappe.throw('Please Set appropriate Serial No for item at row '+str(item.idx))
def before_save(doc,method):
    item_with_stock=[]
    items_removed=""
    comment="Stock available in the below spools:<br>"
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        for item in doc.items:
            item_data=[item.item_code,item.t_warehouse]
            item_doc=frappe.get_doc("Item",item.item_code)

            uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
            stock_qty=float(item.required_qty)/float(uom_list[0].conversion_factor)
            projected_qty = frappe.db.sql("""
                select name
                from `tabSerial No`
                where item_code = %s and stock_warehouse=%s and status not in ("Inactive","Expired") and available_qty>=%s order by creation
            """, (item.item_code,item.t_warehouse,stock_qty))
            if projected_qty:
                sn_doc=frappe.get_doc("Serial No",projected_qty[0][0])
                stock_detail_doc=frappe.db.get_value('Stock Details',{'parent':sn_doc.name,'work_order': doc.work_order},'name')
                sn_doc.db_set('stock_warehouse',item.t_warehouse)
                sn_doc.db_set('available_qty',sn_doc.available_qty-stock_qty)
                sn_doc.save(ignore_permissions=True)
                if stock_detail_doc:
                    stock_detail_doc=frappe.get_doc("Stock Details",stock_detail_doc)
                    reserved_qty=stock_detail_doc.reserved_qty+stock_qty
                    stock_detail_doc.db_set('reserved_qty',reserved_qty)
                else:
                    sn_doc.append('stock_details', {
                        'work_order':doc.work_order,
                        'warehouse':item.t_warehouse,
                        'reserved_qty':stock_qty,
                        'consumed_qty':0
                    })
                    sn_doc.save(ignore_permissions=True)
                comment=comment+item.t_warehouse+" : <a href='/app/serial-no/"+sn_doc.name+"'>"+sn_doc.name+"</a> : "+str(round(stock_qty,2))+" "+sn_doc.secondary_uom+"<br>"
                frappe.db.commit()
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
        doc.comment=comment

def on_cancel(doc,method):
    if doc.stock_entry_type=="Material Transfer for Manufacture":
        comment="Released Spools:<br>"
        for item in doc.items:
            if item.serial_no:
                item_doc=frappe.get_doc("Item",item.item_code)
                uom_list=frappe.db.get_list("UOM Conversion Detail",filters={'parenttype':'Item','parent':item.item_code,'uom':['!=',item_doc.stock_uom]},fields={'*'})
                stock_qty=float(item.required_qty)/float(uom_list[0].conversion_factor)
                sn_doc=frappe.get_doc("Serial No",item.serial_no)
                stock_detail_doc=frappe.db.get_value('Stock Details',{'parent':sn_doc.name,'work_order': doc.work_order},'name')
                if stock_detail_doc:
                    stock_detail_doc=frappe.get_doc("Stock Details",stock_detail_doc)
                    reserved_qty=stock_detail_doc.reserved_qty-stock_qty
                    stock_detail_doc.db_set('reserved_qty',reserved_qty)
                    frappe.db.commit()
                if (1/float(uom_list[0].conversion_factor))==(sn_doc.available_qty+stock_qty):
                    sn_doc.db_set('stock_warehouse',item.s_warehouse)
                sn_doc.db_set('available_qty',sn_doc.available_qty+stock_qty)
                frappe.db.commit()
                comment=comment+item.t_warehouse+" : "+item.serial_no+"<br>"     
        doc.add_comment('Comment',comment)

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
                        stock_detail_doc=frappe.db.get_value('Stock Details',{'parent':sn_doc.name,'work_order': doc.work_order},'name')
                        if stock_detail_doc:
                            stock_detail_doc=frappe.get_doc("Stock Details",stock_detail_doc)
                            stock_detail_doc.db_set('reserved_qty',stock_detail_doc.reserved_qty+stock_qty)
                            stock_detail_doc.db_set('consumed_qty',stock_detail_doc.consumed_qty-stock_qty)
                            sn_doc.add_comment('Comment','Released qty: '+str(round(stock_qty, 2))+' for transaction with Stock Entry: '+doc.name)
                        frappe.db.commit()

