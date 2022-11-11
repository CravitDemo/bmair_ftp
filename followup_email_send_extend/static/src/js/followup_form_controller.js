odoo.define('followup_email_send_extend.FollowupFormController', function (require) {
"use strict";
var core = require('web.core');
var Dialog = require('web.Dialog');
var UserMenu = require('web.UserMenu');
var _t = core._t;
var QWeb = core.qweb;
var FollowupFormController = require('account_followup.FollowupFormController');

FollowupFormController.include({

    _onSendMail: function () {
        var self = this;
        this.model.doSendMail(this.handle);
        this.options = {
            partner_id: this._getPartner(),
            send_by_mail : true
        };
        
        this._rpc({
            model: 'account.followup.report',
            method: 'send_email',
            args: [this.options],
        })
        .then(function () {
            self._removeHighlightEmail();
            self._displayDone();
            self.renderer.renderMailAlert();
        });
    },

    })

});
