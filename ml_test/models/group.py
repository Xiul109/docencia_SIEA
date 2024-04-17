from odoo.models import Model
from odoo import fields, api, exceptions
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)

class Group(Model):
    _name = "mltest.group"
    _description = "A group of clients."

    name = fields.Char()
    members = fields.Many2many("bank.client")
    n_members = fields.Integer(compute="_compute_n_members")

    clustering_id = fields.Many2one("mltest.clustering")

    @api.depends("members")
    def _compute_n_members(self):
        for record in self:
            record.n_members = len(record.members)
