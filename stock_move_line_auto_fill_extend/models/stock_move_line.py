from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    intercompany_moveline_id = fields.Many2one('stock.move.line', string="Inter Company Move Line")
