from odoo.models import Model
from odoo import fields

class User(Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesman_id")