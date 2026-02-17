from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from thai_payroll.constants import CUSTOM_FIELDS

def execute():
    custom_fields = {
        "Salary Structure Assignment": list(filter(lambda l: l["fieldname"] in ["custom_sso_contribution_till_date"], CUSTOM_FIELDS["Salary Structure Assignment"]))
    }
    create_custom_fields(custom_fields, ignore_validate=True)