{
    "name": "ML Test ",  # The name that will appear in the App list
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        "security/ir.model.access.csv",
        "views/bank_client_views.xml",
        "views/mltest_group_views.xml",
        "views/mltest_clustering_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
