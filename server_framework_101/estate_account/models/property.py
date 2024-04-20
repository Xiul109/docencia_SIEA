from odoo.models import Model
from odoo.fields import Command

import logging

_logger = logging.getLogger(__name__)

class Property(Model):
    _inherit = "estate.property"
    

    def action_sold(self):
        for record in self:
            values = {"partner_id":record.buyer_id.id,
                    "move_type":"out_invoice",
                    "line_ids":[
                        Command.create({"name":"Taxes", "quantity":1, "price_unit":record.selling_price*0.06}),
                        Command.create({"name":"Administrative fee", "quantity":1, "price_unit":100.00}),
                    ]}
            self.env["account.move"].create(values)
        return super().action_sold()