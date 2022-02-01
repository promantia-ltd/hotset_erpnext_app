# -*- coding: utf-8 -*-
# Copyright (c) 2020, seabridge_app and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Company(Document):
	pass

@frappe.whitelist()
def get_warehouse_filter(doctype, txt, searchfield, start, page_len, filters):
    parent_warehouse = filters['workstation']
    return frappe.db.sql("""
                select w_name
                from `tabInput Sources`
                where parent = %s and parenttype="Workstation"
        """, (parent_warehouse))


@frappe.whitelist()
def get_operation_filter(doctype, txt, searchfield, start, page_len, filters):
    operation_list = str(filters['operation_list'])
    operation_list=operation_list[1:]
    operation_list=operation_list[:-1]
    operation_list="("+operation_list+")"
    return frappe.db.sql("""
                select name
                from `tabOperation`
                where name in 
        """+operation_list)
