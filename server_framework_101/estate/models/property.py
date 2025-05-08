from odoo import api, models, fields, exceptions
import datetime

class Property(models.Model):
    _name = "estate.property"
    _description = "Represents a property: a house, a flat, a commercial property, etc."
    _order = "id desc"

    active = fields.Boolean(default = True)

    name = fields.Char(required = True, string="Title")

    property_tag_ids = fields.Many2many("estate.property.tag")

    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From" ,default = fields.Date.today() + datetime.timedelta(days = 90), copy = False)
    state = fields.Selection(selection = [("new", "New"), ("offer_received", "Offer Received"),
                                          ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
                             default = "new")

    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    best_price = fields.Float(compute = "_compute_best_price")

    bedrooms =  fields.Integer(default = 2)
    living_area =  fields.Integer(string="Living Area (m²)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (m²)")
    garden_orientation = fields.Selection(selection = [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    total_area = fields.Integer(string = "Total area (m²)", compute = "_compute_total_area")

    offer_ids = fields.One2many("estate.property.offer", "property_id")

    salesperson_id = fields.Many2one("res.users", string = "Salesperson", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string = "Buyer", copy = False)

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be postive'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly postive')
    ]

    # CRUD methods
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if self.state not in ["new", "cancelled"]:
            raise exceptions.UserError("Can't delete unless status is wither New or Cancelled.")

    # Compute methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    # On changes
    @api.onchange("garden")
    def _onchange_garde(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

    # Constrains
    @api.constrains('selling_price', "expected_price")
    def _check_selling_prince(self):
        for record in self:
            if record.state == "offer_accepted" and record.selling_price < (record.expected_price * .9):
                raise exceptions.ValidationError("Selling price must be greater than 90% of expected price.")

    # Actions
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property can not be cancelled.")
            record.state = "cancelled"
        return True

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("A sold property can not be cancelled.")
            record.state = "sold"
        return True
