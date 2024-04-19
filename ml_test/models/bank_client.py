from odoo.models import Model
from odoo import fields

import numpy as np

import joblib
import os
import logging

_logger = logging.getLogger(__name__)

clf_path = os.path.join(os.path.dirname(__file__) ,
                        "../dt_training/client_exit_classifier.pkl")
clf = joblib.load(clf_path)
clf_fields = ["credit_score", "geography", "gender", "age", "tenure", "balance",
              "num_of_products", "has_cr_card", "is_active_member", "estimated_salary"]

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

    def action_predict_exit(self):
        for record in self:
            data = [record[f] for f in clf_fields]
            data[1] = data[1].code
            data = np.array([data], dtype="object")
            record.exited =clf.predict(data)
        return True