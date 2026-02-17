from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from thai_payroll.constants import CUSTOM_FIELDS

def execute():
    custom_fields = {
        "Salary Structure": list(filter(lambda l: l["fieldname"] in ["custom_sso_component"], CUSTOM_FIELDS["Salary Structure"]))
    }
    create_custom_fields(custom_fields, ignore_validate=True)