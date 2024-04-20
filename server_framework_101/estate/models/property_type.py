from odoo.models import Model
from odoo import fields
from dateutil.relativedelta import relativedelta

class PropertyType(Model):
    _name = "estate.property.type"
    _description = "A type of property valid for the estate."
    _order = "sequence,name"

    name = fields.Char(required = True)
    sequence = fields.Integer()

    property_ids = fields.One2many("estate.property", "type_id")
    
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    # Constrains
    _sql_constraints = [
        ("unique_name", "UNIQUE (name)", "Type name must be unique.")
    ]

    # Private methdos
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)