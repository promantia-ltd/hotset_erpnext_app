// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt


frappe.ui.form.on('BOM', {
	refresh:function(frm,cdt,cdn){
		frm.fields_dict['items'].grid.get_field('input_source').get_query = function(frms, cdt, cdn) {
			var child = locals[cdt][cdn];
			var workstation=""
			$.each(frm.doc.operations, function(idx, item){
				if(child.operation==item.operation){
					workstation=item.workstation
				}
			})
			return {
				query: "hotset_customizations.hotset_customizations.doctype.bom.bom.get_warehouse_filter",
				filters: {
					'workstation': workstation
				}	
			};
		};


		frm.fields_dict['items'].grid.get_field('operation').get_query = function(frms, cdt, cdn) {
			var child = locals[cdt][cdn];
			var operation_count=0;
			const operations=[];
			$.each(frm.doc.operations, function(idx, item){
				if(item.operation){
					operations.push(item.operation)
				}
			})
			return {
				query: "hotset_customizations.hotset_customizations.doctype.bom.bom.get_operation_filter",
				filters: {
					'operation_list': operations
				}	
			};
		};
	}
})

