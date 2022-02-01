// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order', {
	refresh:function(frm,cdt,cdn){
		if(frm.doc.__islocal==1){
			frappe.model.with_doc("BOM", frm.doc.bom_no, function() {
			var tabletransfer= frappe.model.get_doc("BOM", frm.doc.bom_no)
			    $.each(tabletransfer.items, function(index, detail){
				$.each(frm.doc.required_items, function(idx, item){
					if(detail.item_code==item.item_code){
					item.source_warehouse=detail.input_source
					}
				})
			    })
			})
			cur_frm.refresh_field("required_items")
		}
	},
	bom_no:function(frm,cdt,cdn){
		frappe.model.with_doc("BOM", frm.doc.bom_no, function() {
		var tabletransfer= frappe.model.get_doc("BOM", frm.doc.bom_no)
		    $.each(tabletransfer.items, function(index, detail){
			$.each(frm.doc.required_items, function(idx, item){
				if(detail.item_code==item.item_code){
				item.source_warehouse=detail.input_source
				cur_frm.refresh_field("required_items")
				}
			})
		    })
		})
		
	}
})

