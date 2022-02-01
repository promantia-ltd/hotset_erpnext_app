// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt

var wip_warehouse="";
frappe.ui.form.on('Workstation', {
	refresh:function(frm,cdt,cdn){
		wip_warehouse=frm.doc.wip_warehouse
		frm.fields_dict['input_sources'].grid.get_field('w_name').get_query = function(frm, cdt, cdn) {
			return{
				filters: {
					'parent': wip_warehouse
				}
			};
		};
		frm.fields_dict['input_sources'].grid.get_field('item').get_query = function(frm, cdt, cdn) {
			return{
				filters: {
					'include_item_in_manufacturing': 1
				}
			};
		};
		
	},
	wip_warehouse:function(frm,cdt,cdn){
		wip_warehouse=frm.doc.wip_warehouse
		
	}
})


frappe.ui.form.on("Input Sources", "item",function(frm, doctype, name) {
      var row = locals[doctype][name];
        frappe.db.get_value("Item",row.item, "item_group",(s)=>{
                row.item_group=s.item_group;
		frm.refresh_field("input_sources")
        })

        
})
