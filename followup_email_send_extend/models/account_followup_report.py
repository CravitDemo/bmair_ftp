# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, tools
from odoo.tools.translate import _
from odoo.tools import append_content_to_html
from odoo.exceptions import UserError


class report_account_followup_report(models.AbstractModel):
    _inherit = "account.followup.report"

    @api.model
    def send_email(self, options):
        ctx = self._context.copy()
        if options.get('send_by_mail'):
            ctx.update({'mail_send_on_folllowup_mailid': True})
        """
        Send by mail the followup to the customer
        """
        partner = self.env['res.partner'].browse(options.get('partner_id'))
        non_blocked_invoices = partner.unpaid_invoices.filtered(lambda inv: not any(inv.line_ids.mapped('blocked')))
        non_printed_invoices = non_blocked_invoices.filtered(lambda inv: not inv.message_main_attachment_id)
        if non_printed_invoices and partner.followup_level.join_invoices:
            raise UserError(_('You are trying to send a followup report to a partner for which you didn\'t print all the invoices ({})').format(" ".join(non_printed_invoices.mapped('name'))))
        invoice_partner = self.env['res.partner'].browse(partner.address_get(['invoice'])['invoice'])
        email = invoice_partner.email
        options['keep_summary'] = True
        if partner.statement_account_email:
            email = partner.statement_account_email
        if email and email.strip():
            # When printing we need te replace the \n of the summary by <br /> tags
            body_html = self.with_context(print_mode=True, mail=True, lang=partner.lang or self.env.user.lang).get_html(options)
            body_html = body_html.replace(b'o_account_reports_edit_summary_pencil', b'o_account_reports_edit_summary_pencil d-none')
            start_index = body_html.find(b'<span>', body_html.find(b'<div class="o_account_reports_summary">'))
            end_index = start_index > -1 and body_html.find(b'</span>', start_index) or -1
            if end_index > -1:
                replaced_msg = body_html[start_index:end_index].replace(b'\n', b'')
                body_html = body_html[:start_index] + replaced_msg + body_html[end_index:]
            ctx.update({'mail_post_autofollow': True})
            partner.with_context(ctx).message_post(
                partner_ids=[invoice_partner.id],
                body=body_html,
                subject=_('%s Payment Reminder') % (self.env.company.name) + ' - ' + partner.name,
                subtype_id=self.env.ref('mail.mt_note').id,
                model_description=_('payment reminder'),
                email_layout_xmlid='mail.mail_notification_light',
                attachment_ids=partner.followup_level.join_invoices and non_blocked_invoices.message_main_attachment_id.ids or [],
            )
            return True
        raise UserError(_('Could not send mail to partner %s because it does not have any email address defined') % partner.display_name)
