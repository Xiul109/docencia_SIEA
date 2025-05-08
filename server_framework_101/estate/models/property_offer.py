from odoo import api, models, fields, exceptions
from dateutil.relativedelta import relativedelta

import datetime

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Each of the offers received by a property."
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection = [("accepted", "Accepted"), ("refused", "Refused")], copy = False)
    partner_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer(string="Validity (days)", default = 7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one("estate.property.type", related = "property_id.property_type_id")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'An offer price must be strictly postive')
    ]

    # CRUD
    @api.model_create_multi
    def create(self, vals_list):
        properties = []
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.state in ["offer_accepted", "cancelled", "sold"]:
                raise exceptions.UserError("Cannot receive more offers if an offer has been already accepted or the property has been sold or cancelled.")
            if (len(property.offer_ids) > 0) and (vals["price"]  < min(property.offer_ids.mapped("price"))):
                raise exceptions.UserError("Offers with lower price than existing ones won't be accepted.")
            properties.append(property)

        # Property state is not modified if exception is raised
        for property in properties:
            property.state = "offer_received"

        return super().create(vals_list)


    # Computes
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date if record.create_date else datetime.date.today()
            record.date_deadline = date + relativedelta(days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    # Actions
    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted":
                    raise exceptions.UserError("Only one offer can be accepted.")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
