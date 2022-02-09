// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt


frappe.ui.form.on('Stock Entry', {
	refresh:function(frm,cdt,cdn){
		var finished_item=""
		frappe.db.get_value("Work Order",frm.doc.work_order,"source_warehouse",(c)=>{
			frm.set_value("from_warehouse",c.source_warehouse)
		})
		if(frm.doc.stock_entry_type=="Material Transfer for Manufacture"){
		const serial_no_assigned=[];
		if(frm.doc.__islocal==1){
			if(frm.doc.bom_no){
				frappe.db.get_value("BOM",frm.doc.bom_no,"quantity",(c)=>{
					frappe.model.with_doc("BOM", frm.doc.bom_no, function() {
					cur_frm.clear_table("items");
					var tabletransfer= frappe.model.get_doc("BOM", frm.doc.bom_no)
						$.each(tabletransfer.items, function(index, detail){	
						frappe.call({
								method:"hotset_customizations.hotset_customizations.doctype.stock_entry.stock_entry.get_serial_no",
								args:{
									item:detail.item_code,
									warehouse:frm.doc.from_warehouse,
									qty:(detail.stock_qty/c.quantity)*frm.doc.fg_completed_qty	
								},
								async:false,
								callback: function(r){
									var qty_count=0;
									var serial_no_string=""
									var child=frm.add_child("items");
									child.s_warehouse=frm.doc.from_warehouse;
									child.t_warehouse=detail.input_source;
									child.item_code=detail.item_code;
									child.item_name=detail.item_name;
									child.required_qty=(detail.stock_qty/c.quantity)*frm.doc.fg_completed_qty;
									child.qty=(detail.stock_qty/c.quantity)*frm.doc.fg_completed_qty;
									child.basic_rate=detail.rate;
									child.uom=detail.stock_uom;
									child.conversion_factor=detail.conversion_factor;
									child.transfer_qty=detail.stock_qty;
									var serial_no_qty=0;
									var uom_conversion_factor=1
									frappe.model.with_doc("Item", child.item_code, function() {
										var tabletransfer= frappe.model.get_doc("Item", child.item_code)
											$.each(tabletransfer.uoms, function(index, uom_detail){
												if(uom_detail.uom!=child.uom){
													uom_conversion_factor=uom_detail.conversion_factor
									var item_qty=child.qty/uom_conversion_factor;
									for (let i = 0; i < r.message.length; i++) {
										if(!serial_no_assigned.includes(r.message[i][0])){
											serial_no_assigned.push(r.message[i][0])
											child.serial_no=r.message[i][0]
											child.qty=r.message[i][1]*uom_conversion_factor
											break
										}
									}
												}

											})
									})	
								}
							});
						})
					})
					cur_frm.refresh_field("required_items")
				})
			}
		}
		}

		if(frm.doc.stock_entry_type=="Manufacture"){
			const serial_no_assigned=[];
			if(frm.doc.__islocal==1){
				if(frm.doc.bom_no){
					frappe.db.get_value("BOM",frm.doc.bom_no,"quantity",(c)=>{
						frappe.model.with_doc("BOM", frm.doc.bom_no, function() {
							$.each(frm.doc.items, function(idx, item){
								if(item.is_finished_item==1){
									finished_item=item
								}
							})

						cur_frm.clear_table("items");
						var tabletransfer= frappe.model.get_doc("BOM", frm.doc.bom_no)
							$.each(tabletransfer.items, function(index, detail){	
							frappe.call({
									method:"hotset_customizations.hotset_customizations.doctype.stock_entry.stock_entry.get_serial_no",
									args:{
										item:detail.item_code,
										warehouse:detail.input_source,
										qty:(detail.stock_qty/c.quantity)*frm.doc.fg_completed_qty	
									},
									async:false,
									callback: function(r){
										var qty_count=0;
										var serial_no_string=""
										var child=frm.add_child("items");
										child.s_warehouse=detail.input_source;
										child.item_code=detail.item_code;
										child.item_name=detail.item_name;
										child.qty=(detail.stock_qty/c.quantity)*frm.doc.fg_completed_qty;
										child.basic_rate=detail.rate;
										child.uom=detail.stock_uom;
										child.conversion_factor=detail.conversion_factor;
										child.transfer_qty=detail.stock_qty;
										var serial_no_qty=0;
										var uom_conversion_factor=1
										frappe.model.with_doc("Item", child.item_code, function() {
											var tabletransfer= frappe.model.get_doc("Item", child.item_code)
												$.each(tabletransfer.uoms, function(index, uom_detail){
													if(uom_detail.uom!=child.uom){
														uom_conversion_factor=uom_detail.conversion_factor
										var item_qty=child.qty/uom_conversion_factor;
										for (let i = 0; i < r.message.length; i++) {
											if(!serial_no_assigned.includes(r.message[i][0])){
												serial_no_assigned.push(r.message[i][0])
												child.serial_no=r.message[i][0]
												break
											}
										}
													}
	
												})
										})	
									}
								});
							})
							var fin_child=frm.add_child("items");
							fin_child.t_warehouse=finished_item.t_warehouse;
							fin_child.is_finished_item=finished_item.is_finished_item;
							fin_child.item_code=finished_item.item_code;
							fin_child.item_name=finished_item.item_name;
							fin_child.qty=finished_item.qty;
							fin_child.basic_rate=finished_item.basic_rate;
							fin_child.uom=finished_item.uom;
							fin_child.conversion_factor=finished_item.conversion_factor;
							fin_child.transfer_qty=finished_item.transfer_qty;
						})
						cur_frm.refresh_field("required_items")
					})
				}
			}
			}

	}
})

