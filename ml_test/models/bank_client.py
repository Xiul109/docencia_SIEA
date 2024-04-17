from odoo.models import Model
from odoo import fields, api, exceptions
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)

class BankClient(Model):
    """Representation of a client from a bank."""
    _name = "bank.client"
    _description = "Data from the clients of the bank."

    customer_id = fields.Char() # It is the original id, not the Odoo one
    surname = fields.Char()
    geography = fields.Many2one("res.country")
    gender = fields.Selection([("female", "Female"),
                               ("male", "Male"),
                               ("other", "Other")
                               ])
    age = fields.Integer()

    balance = fields.Float()
    estimated_salary = fields.Float()

    credit_score = fields.Integer()
    tenure = fields.Integer()
    
    num_of_products = fields.Integer()
    has_cr_card =  fields.Boolean()
    is_active_member = fields.Boolean()
    
    exited = fields.Boolean()