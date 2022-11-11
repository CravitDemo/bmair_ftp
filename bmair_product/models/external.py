# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import ftplib
import logging
_logger = logging.getLogger(__name__)

class ExternalInterface(models.Model):
    _name = "external.interface"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    ftp_location = fields.Char(string='FTP Location', help='Link to the FTP location')
    user_name = fields.Char(string='Username', help='Username to connect to the FTP location')
    pwd = fields.Char(string='Password', help='Password to connect to the FTP location')
    note = fields.Text(stirng="Notes" ,help='Area to add internal notes/description about this interface')
    partner_id = fields.Many2one('res.partner', string="Partner")
    country_id = fields.Many2one('res.country', string="Country")
    con_state = fields.Selection(
        [('draft', 'Draft'),('success', 'Success'),('fail', 'Fail')],string='State',default='draft')

    def test_connection_ftp(self):
        if self.ftp_location:
            try:
                with ftplib.FTP_TLS(self.ftp_location) as ftp:
                    ftp.login(self.user_name, self.pwd)
#                     ftp.connect(self.user_name, self.pwd)
                    self.write({'con_state': 'success'})
            except Exception as error:
                _logger.info("FTP Response Data : %s" % (error))
#                 print (error,"error----")
                self.write({'con_state': 'fail'})
        return True
