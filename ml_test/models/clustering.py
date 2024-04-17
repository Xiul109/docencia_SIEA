from odoo.models import Model
from odoo import fields, api, exceptions
from dateutil.relativedelta import relativedelta

from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np

import logging

_logger = logging.getLogger(__name__)

class Clustering(Model):
    """Contains the parameters for KMeans and DBSCAN algorithms and also contains the groups
    that generated after applying the algorithms."""
    
    _name = "mltest.clustering"
    _description = "A clustering wrapper."

    name = fields.Char()
    algorithm = fields.Selection([("k-means", "K-Means"),
                                  ("dbscan", "DBSCAN"),
                                  ], default = "k-means")

    k_param = fields.Integer(string="K", default = 3)
    epsilon_param = fields.Float(string="Epsilon", default = 0.05)
    min_samples_param = fields.Integer(string="Minimum Samples", default = 5)


    groups = fields.One2many("mltest.group", "clustering_id")

    def action_perform_clustering(self):
        for record in self:
            # Initializing the model
            model = None
            if record.algorithm == "k-means":
                model = KMeans(record.k_param, algorithm="lloyd")
                # Lloyd algorithm do not work well in Odoo
            else:
                model = DBSCAN(eps=record.epsilon_param, min_samples=record.min_samples_param)
            # Cleaning the groups
            for g in record.groups:
                g.unlink()
            
            self._perform_clustering_for_record(record, model)
        return True

    def _perform_clustering_for_record(self, record, model):
        # Extracting required data
        clients = np.array(list(map(lambda client: np.array([client.id,
                                                             client.balance,
                                                             client.estimated_salary,
                                                             client.credit_score,
                                                             client.tenure,
                                                             client.num_of_products]),
                                    self.env["bank.client"].search([]))))
        ids = clients[:, 0]
        
        # Scaling the values
        scaler = StandardScaler()
        data = scaler.fit_transform(clients[:, 1:])

        # Fitting the model
        model.fit(data)

        # Creating the groups containing the clients
        labels = model.labels_
        for label in np.unique(labels):
            members = [(4, id) for id in ids[np.where(labels==label)]]
            record.write({"groups":[(0, 0, {"name": "g%d"%label, 
                                            "clustering_id": record.id,
                                            "members":members})]})
