from odoo import models, fields, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Represents each type of property."
    _order = "sequence, name"

    name = fields.Char(required = True, string="Title")
    sequence = fields.Integer()

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute = "_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name must be unique.')
    ]
