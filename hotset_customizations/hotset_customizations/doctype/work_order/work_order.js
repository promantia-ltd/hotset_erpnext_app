// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order', {
	refresh:function(frm,cdt,cdn){
		if(frm.doc.docstatus==1){
			var stock_avail_qty=0;
			var item_count=0;
			var check_stock=0;
			frm.remove_custom_button('Start');
			const show_start_btn = (frm.doc.skip_transfer
					|| frm.doc.transfer_material_against == 'Job Card') ? 0 : 1;
			if (show_start_btn) {
				if ((flt(frm.doc.material_transferred_for_manufacturing) < flt(frm.doc.qty))
				&& frm.doc.status != 'Stopped') {
					frm.has_start_btn = true;
					frm.add_custom_button(__('Create Pick List'), function() {
						erpnext.work_order.create_pick_list(frm);
					});
					frm.add_custom_button('Start', function(){
				if(frm.doc.bom_no){
					var comment="Reserved Qty<br>"
					frappe.db.get_value("BOM",frm.doc.bom_no,"quantity",(c)=>{
						frappe.model.with_doc("BOM", frm.doc.bom_no, function() {
		           				var tabletransfer= frappe.model.get_doc("BOM", frm.doc.bom_no)
							$.each(tabletransfer.items, function(index, row){
								item_count+=1;
								frappe.call({
								method:"hotset_customizations.hotset_customizations.doctype.work_order.work_order.check_stock",
								args:{
									item:row.item_code,				
									warehouse:row.input_source,
									item_qty:row.qty,
									work_order:frm.doc.name,
									bom_qty:c.quantity,
									wo_qty:frm.doc.qty-frm.doc.material_transferred_for_manufacturing	
								},
								async:false,
								callback: function(r){
									if(r.message==true){
										check_stock+=1;
									}
										
								}
								});
							})
							if(check_stock==item_count){
							
		           				$.each(tabletransfer.items, function(index, row){
								
								frappe.call({
								method:"hotset_customizations.hotset_customizations.doctype.work_order.work_order.reserve_qty",
								args:{
									item:row.item_code,				
									warehouse:row.input_source,
									item_qty:row.qty,
									work_order:frm.doc.name,
									bom_qty:c.quantity,
									wo_qty:frm.doc.qty-frm.doc.material_transferred_for_manufacturing	
								},
								async:false,
								callback: function(r){
									if(r.message.length==2){
										comment=comment.concat(r.message[0])
										stock_avail_qty+=1;
										
									}	
									
								}
								});
							})
							frm.remove_custom_button('Start');
							}
							else{
								erpnext.work_order.make_se(frm, 'Material Transfer for Manufacture');
							}
							if(item_count==stock_avail_qty){
							frappe.call({
								method:"hotset_customizations.hotset_customizations.doctype.work_order.work_order.add_comment",
								args:{
									doctype:"Work Order",
									docname:frm.doc.name,
									comment:comment	
								},
								async:false,
								callback: function(r){
								}
								});
							 msgprint('<b>Stock Reserved Successfully</b><br>'+comment,'Alert')
							frappe.call({
                                            async: false,
                                            "method": "frappe.client.set_value",
                                            "args": {
                                                "doctype": "Work Order",
                                                "name": frm.doc.name,
                                                "fieldname": "skip_material_transfer",
                                                "value":1
                                            }
                                        });
							}
						})
						
					})
					
				}
				
				
			}).addClass('btn-primary');
			 
		}
		}
		}
	
	},
	before_save:function(frm,cdt,cdn){
		var from_warehouse=""
		$.each(frm.doc.required_items, function(idx, item){
			from_warehouse=item.source_warehouse
		})
		frm.set_value("source_warehouse",from_warehouse)
		
		
	}
})

