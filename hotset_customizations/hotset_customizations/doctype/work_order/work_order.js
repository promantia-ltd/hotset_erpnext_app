// Copyright (c) 2020, seabridge_app and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order', {
	refresh:function(frm,cdt,cdn){
		if((frm.doc.status=="Submitted" || frm.doc.status=="Not Started" || frm.doc.status=="In Process") && frm.doc.skip_material_transfer!=1){
			frm.add_custom_button('Reserve Qty', function(){
				if(frm.doc.bom_no){
					var comment="Reserved Qty<br>"
					frappe.db.get_value("BOM",frm.doc.bom_no,"quantity",(c)=>{
						frappe.model.with_doc("BOM", frm.doc.bom_no, function() {
		           				var tabletransfer= frappe.model.get_doc("BOM", frm.doc.bom_no)
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
									comment=comment.concat(r.message)
								}
								});


		
							})
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
						})
						
					})
					
				}
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
				setTimeout(() => {
				frm.remove_custom_button('Start');
				}, 10);
			frm.remove_custom_button("Reserve Qty");
			});
			 
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

