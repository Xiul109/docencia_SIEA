from odoo.models import Model
from odoo import fields, api, exceptions
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)

class PropertyOffer(Model):
    _name = "estate.property.offer"
    _description = "An offer made for a property."
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"),
                               ("refused", "Refused")],
                               copy = False)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one("estate.property", "Property", required=True)
    property_type_id = fields.Many2one(related="property_id.type_id")

    # Constrains
    _sql_constraints = [
        ("e_positive_offer_price", "CHECK (price > 0)", "Offer price must be bigger than 0."),
    ]

    # Private methods
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date if record.create_date else fields.Datetime.now()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date if record.create_date else fields.Datetime.now()
            record.validity = (fields.Datetime.to_datetime(record.date_deadline) - base_date).days
    
    # Overrides
    @api.model
    def create(self, vals):
        self.env["estate.property"].browse(vals["property_id"]).state = "offer_received"
        return super().create(vals)
    
    # Actions
    def action_accept(self):
        for record in self:
            for offer in record.property_id.offers_ids:
                if offer.status == "accepted" and offer != record:
                    raise exceptions.UserError("Only one offer can be accepted at the same time.")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

        return True
    
    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    