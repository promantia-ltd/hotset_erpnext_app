# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__version__ = '0.0.1'
import erpnext
from erpnext.stock.doctype.serial_no.serial_no import validate_serial_no as erpnext_validate_serial_no
from hotset_customizations.api import validate_serial_no

erpnext_validate_serial_no=validate_serial_no
