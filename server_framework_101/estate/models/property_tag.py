from odoo.models import Model
from odoo import fields
from dateutil.relativedelta import relativedelta

class PropertyTag(Model):
    _name = "estate.property.tag"
    _description = "A tag for properties."
    _order = "name"

    name = fields.Char(required = True)
    color = fields.Integer()

    # Constrains
    _sql_constraints = [
        ("unique_name", "UNIQUE (name)", "Tag name must be unique.")
    ]
    