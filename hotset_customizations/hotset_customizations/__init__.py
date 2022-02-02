# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
__version__ = '0.0.1'

@frappe.whitelist()
def validate_serial_no(sle, item_det):
	print('INIT--------------')
