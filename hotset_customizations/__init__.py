# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__version__ = '0.0.1'
import erpnext.stock.doctype.serial_no.serial_no
import hotset_customizations.api

erpnext.stock.doctype.serial_no.serial_no.validate_serial_no=hotset_customizations.api.validate_serial_no
