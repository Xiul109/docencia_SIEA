from odoo import models, Command

class AccountProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            invoice = self.env["account.move"].create(
                {"partner_id":record.buyer_id.id,
                 "move_type":"out_invoice",
                 "line_ids": [
                     Command.create({"name":"Price part",
                                     "quantity": 1,
                                     "price_unit": record.selling_price*0.06}),
                     Command.create({"name":"Administrative fee",
                                     "quantity": 1,
                                     "price_unit": 100})
                 ]
                 })
        return super().action_sold()
