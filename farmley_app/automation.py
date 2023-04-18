import frappe
from datetime import datetime, timedelta

def auto_cancel_delivery_note():
    # Get all delivery notes that are not cancelled and have no associated sales invoice
    delivery_notes = frappe.db.sql("""
        SELECT name, posting_date
        FROM `tabDelivery Note`
        WHERE docstatus = 1
            AND status != 'Cancelled'
            AND is_internal_customer != 1
            AND NOT EXISTS (
                SELECT 1
                FROM `tabSales Invoice Item` sii
                INNER JOIN `tabDelivery Note Item` dni ON dni.name = sii.dn_detail
                WHERE dni.parent = `tabDelivery Note`.name
            )
    """, as_dict=True)

    # Cancel delivery notes that are older than 12 hours
    for delivery_note in delivery_notes:
        posting_date_str = delivery_note.posting_date.strftime('%Y-%m-%d')
        posting_date = datetime.strptime(posting_date_str, '%Y-%m-%d')
        hours_difference = (datetime.now() - posting_date).total_seconds() / 3600
        if hours_difference >= 12:
            delivery_note_doc = frappe.get_doc('Delivery Note', delivery_note.name)
            delivery_note_doc.cancel()
            frappe.db.commit()

# Run the auto_cancel_delivery_note function every hour
def scheduler():
    frappe.enqueue("farmley_app.automation.auto_cancel_delivery_note")