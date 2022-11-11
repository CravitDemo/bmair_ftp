# -*- coding: utf-8 -*-
# Copyright 2019 B-Informed (<https://www.b-informed.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.tools.translate import _
from odoo.tools import append_content_to_html, DEFAULT_SERVER_DATE_FORMAT, html2plaintext
from odoo.exceptions import UserError


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def get_html(self, options, line_id=None, additional_context=None):
        """
        Override
        Compute and return the content in HTML of the followup for the partner_id in options
        """
        if additional_context is None:
            additional_context = {}
            additional_context['followup_line'] = self.get_followup_line(options)

        partner = self.env['res.partner'].browse(options['partner_id'])
        additional_context['partner'] = partner
        additional_context['lang'] = partner.lang or get_lang(self.env).code
        additional_context['followup_address_id'] = False
        additional_context['invoice_address_id']=False
        followup=self.env['res.partner'].search([('type','=','followup'),('parent_id','=',partner.id)],limit=1)
        if followup and followup.email:
            additional_context['followup_address_id']=followup
        invoices = self.env['res.partner'].search([('type', '=', 'invoice'), ('parent_id', '=', partner.id)],limit=1)
        if invoices and invoices.email:
            additional_context['invoice_address_id'] = invoices
        additional_context['today'] = fields.date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
        return super(AccountFollowupReport, self).get_html(options, line_id=line_id, additional_context=additional_context)

    @api.model
    def send_email(self, options):
        """
        Send by mail the followup to the customer
        """
        partner = self.env['res.partner'].browse(options.get('partner_id'))
        non_blocked_amls = partner.unreconciled_aml_ids.filtered(lambda aml: not aml.blocked)
        if not non_blocked_amls:
            return True
        non_printed_invoices = partner.unpaid_invoices.filtered(lambda inv: not inv.message_main_attachment_id)
        if non_printed_invoices and partner.followup_level.join_invoices:
            raise UserError(
                _('You are trying to send a followup report to a partner for which you didn\'t print all the invoices ({})').format(
                    " ".join(non_printed_invoices.mapped('name'))))
        p_id = partner

        email=partner.email
        followup = self.env['res.partner'].search([('type', '=', 'followup'), ('parent_id', '=', partner.id)], limit=1)

        if followup and followup.email:
            p_id=followup
            email = followup.email
        if not followup:
            invoices=self.env['res.partner'].search([('type', '=', 'invoice'), ('parent_id', '=', partner.id)], limit=1)
            if invoices and invoices.email:
                p_id=invoices
                email = invoices.email

        options['keep_summary'] = True

        if email and email.strip():
            # When printing we need te replace the \n of the summary by <br /> tags
            body_html = self.with_context(print_mode=True, mail=True, lang=partner.lang or self.env.user.lang).get_html(
                options)
            body_html = body_html.replace(b'o_account_reports_edit_summary_pencil',
                                          b'o_account_reports_edit_summary_pencil d-none')
            start_index = body_html.find(b'<span>', body_html.find(b'<div class="o_account_reports_summary">'))
            end_index = start_index > -1 and body_html.find(b'</span>', start_index) or -1
            if end_index > -1:
                replaced_msg = body_html[start_index:end_index].replace(b'\n', b'')
                body_html = body_html[:start_index] + replaced_msg + body_html[end_index:]
            partner.with_context(mail_post_autofollow=True).message_post(
                partner_ids=[p_id.id],
                body=body_html,
                subject=_('%(company)s Payment Reminder - %(customer)s', company=self.env.company.name,
                          customer=partner.name),
                subtype_id=self.env.ref('mail.mt_note').id,
                model_description=_('payment reminder'),
                email_layout_xmlid='mail.mail_notification_light',
                attachment_ids=partner.followup_level.join_invoices and partner.unpaid_invoices.message_main_attachment_id.ids or [],
            )
            return True
        raise UserError(_('Could not send mail to partner %s because it does not have any email address defined',
                          partner.display_name))
