from odoo import fields, models, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    route_id = fields.Many2one('stock.location.route', string='FSM Route')
