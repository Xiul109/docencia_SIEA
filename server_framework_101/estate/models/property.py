from odoo.models import Model
from odoo import fields, api, exceptions
from dateutil.relativedelta import relativedelta

class Property(Model):
    _name = "estate.property"
    _description = "A property offered by the Real Estate."
    _order = "id desc"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From",required = True, copy = False, 
                                    default = fields.Date.add(fields.Date.today(), relativedelta(months = 3)))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly = True)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([("north", "North"),
                                           ("south", "South"),
                                           ("west" , "West"),
                                           ("east" , "East"),],
                                           default = "north",)
    
    state = fields.Selection([("new", "New"),
                              ("offer_received", "Offer Received"),
                              ("offer_accepted", "Offer Accepted"),
                              ("sold", "Sold"),
                              ("canceled", "Canceled")],
                              required = True, copy = False, default = "new")
    
    active = fields.Boolean(default = True)

    # Refs
    type_id = fields.Many2one("estate.property.type", string="Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self:self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")

    tags_ids = fields.Many2many("estate.property.tag", string="Tag")
    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    # Constrains
    _sql_constraints = [
        ("e_positive_expected_price", "CHECK (expected_price > 0)", "Expected price must be bigger than 0."),
        ("positive_selling_price", "CHECK (selling_price >= 0)", "Selling price cannot be negative.")
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_expected_agains_selling_price(self):
        for record in self:
            for offer in record.offers_ids:
                if offer.status == "accepted" and record.selling_price<0.9*record.expected_price:
                    raise exceptions.ValidationError("Selling price cannot be lower than the 90% of the expected price.")

    # Private methods
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.depends("offers_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offers_ids.mapped("price")) if len(record.offers_ids) > 0 else 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_canceled(self):
        for record in self:
            if not record.state in ["new", "canceled"]:
                raise exceptions.UserError("Only new or canceled properties can be deleted.")

    # Actions
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property cannot be canceled")
            else:
                record.state = "canceled"
        return True
    
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("A canceled property cannot be sold")
            else:
                record.state = "sold"
        return True