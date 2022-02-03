# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__version__ = '0.0.1'
import erpnext.stock.doctype.serial_no.serial_no
from hotset_customizations.api import validate_serial_no

erpnext.stock.doctype.serial_no.serial_no.validate_serial_no=validate_serial_no
