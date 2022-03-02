# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__version__ = '0.0.1'
import erpnext
from hotset_customizations.api import hotset_validate_serial_no


erpnext.stock.doctype.serial_no.serial_no.validate_serial_no=hotset_validate_serial_no
