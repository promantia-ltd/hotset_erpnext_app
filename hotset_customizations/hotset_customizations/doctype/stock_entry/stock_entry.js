// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Entry', {
	refresh:function(frm,cdt,cdn){
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
									warehouse:detail.input_source	
								},
								async:false,
								callback: function(r){
									var qty_count=0;
									var serial_no_string=""
									var child=frm.add_child("items");
									child.s_warehouse=detail.input_source;
									child.t_warehouse=frm.doc.to_warehouse;
									child.item_code=detail.item_code;
									child.item_name=detail.item_name;
									child.qty=(detail.qty/c.quantity)*frm.doc.fg_completed_qty;
									child.basic_rate=detail.rate;
									child.uom=detail.uom;
									child.conversion_factor=detail.conversion_factor;
									child.transfer_qty=detail.stock_qty;
									var serial_no_qty=0;
									var item_qty=child.qty;
									for (let i = 0; i < r.message.length; i++) {
										if(!serial_no_assigned.includes(r.message[i][0])){
											serial_no_qty=serial_no_qty+r.message[i][1]
											serial_no_assigned.push(r.message[i][0])
											serial_no_string=serial_no_string.concat(r.message[i][0])
											if(item_qty<=r.message[i][1]){
												child.serial_no=serial_no_string
												break;
											}
											serial_no_string=serial_no_string.concat("\n")
											item_qty=item_qty-r.message[i][1]
										}
									}
									



									
								}
							});
						})
					})
					cur_frm.refresh_field("required_items")
				})
			}
		}
		}
	}
})

