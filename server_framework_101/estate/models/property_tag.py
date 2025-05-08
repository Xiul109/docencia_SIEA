from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Used for adding the possibility of adding tags to properties."
    _order = "name"

    name = fields.Char(required = True, string="Title")
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name must be unique.')
    ]
