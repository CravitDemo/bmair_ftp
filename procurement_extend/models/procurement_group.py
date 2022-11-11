# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from collections import defaultdict, namedtuple

from dateutil.relativedelta import relativedelta

from odoo import SUPERUSER_ID, _, api, fields, models, registry
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero, html_escape
from odoo.tools.misc import split_every

_logger = logging.getLogger(__name__)




class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    
    @api.model
    def _run_scheduler_tasks(self, use_new_cursor=False, company_id=False):
        # Minimum stock rules
        domain = self._get_orderpoint_domain(company_id=company_id)
        orderpoints = self.env['stock.warehouse.orderpoint'].search(domain)
        # ensure that qty_* which depends on datetime.now() are correctly
        # recomputed
        orderpoints.sudo()._compute_qty_to_order()
        orderpoints.sudo()._manual_procure_orderpoint_confirm(use_new_cursor=use_new_cursor, company_id=company_id, raise_user_error=False)
        if use_new_cursor:
            self._cr.commit()

        # Search all confirmed stock_moves and try to assign them
        domain = self._get_moves_to_assign_domain(company_id)
        moves_to_assign = self.env['stock.move'].search(domain, limit=None,
            order='priority desc, date asc')
        for moves_chunk in split_every(100, moves_to_assign.ids):
            self.env['stock.move'].browse(moves_chunk).sudo()._action_assign()
            if use_new_cursor:
                self._cr.commit()

        # Merge duplicated quants
        self.env['stock.quant']._quant_tasks()

        if use_new_cursor:
            self._cr.commit()

    
    @api.model
    def procurement_manual_run_scheduler(self, use_new_cursor=False, company_id=False):
        """ Call the scheduler in order to check the running procurements (super method), to check the minimum stock rules
        and the availability of moves. This function is intended to be run for all the companies at the same time, so
        we run functions as SUPERUSER to avoid intercompanies and access rights issues. """
        try:
            if use_new_cursor:
                cr = registry(self._cr.dbname).cursor()
                self = self.with_env(self.env(cr=cr))  # TDE FIXME

            self._run_scheduler_tasks(use_new_cursor=use_new_cursor, company_id=company_id)
        finally:
            if use_new_cursor:
                try:
                    self._cr.close()
                except Exception:
                    pass
        return {}