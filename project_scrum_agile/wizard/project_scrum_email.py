# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo import tools
from odoo.exceptions import ValidationError


class ProjectScrumEmail(models.TransientModel):
    _name = 'project.scrum.email'

    @api.model
    def default_get(self, fields):
        """
        This function gets default values
        @param self: The object pointer
        """
        context = self._context or {}
        meeting_pool = self.env['project.scrum.meeting']
        record_ids = context.get('active_ids', []) or []
        res = super(ProjectScrumEmail, self).default_get(fields)
        for meeting in meeting_pool.browse(record_ids):
            sprint = meeting.sprint_id
            if 'scrum_master_email' in fields:
                res.update({'scrum_master_email': sprint.scrum_master_id and
                            sprint.scrum_master_id.partner_id.email or False})
            if 'product_owner_email' in fields:
                res.update({'product_owner_email': sprint.product_owner_id and
                            sprint.product_owner_id.partner_id.email or False})
            if 'subject' in fields:
                subject = _("Scrum Meeting : %s") % (meeting.start_datetime)
                res.update({'subject': subject})
            if 'message' in fields:
                message = _(
                    "Hello  , \nI am sending you Scrum Meeting :"
                    "%s for the Sprint  '%s' of Project '%s' ") \
                    % (meeting.start_datetime, sprint.name,
                       sprint.project_id and sprint.project_id.name or '')
                res.update({'message': message})
        return res

    scrum_master_email = fields.Char(
        'Scrum Master Email',
        size=64,
        help="Email Id of Scrum Master"
    )
    product_owner_email = fields.Char(
        'Product Owner Email',
        size=64,
        help="Email Id of Product Owner"
    )
    subject = fields.Char('Subject', size=64)
    message = fields.Text('Message')

    @api.multi
    def button_send_scrum_email(self):
        uid = self._uid
        context = self._context or {}
        resp = []
        active_id = context.get('active_id', False)
        scrum_meeting_pool = self.env['project.scrum.meeting']
        user_pool = self.env['res.users']
        meeting = scrum_meeting_pool.browse(active_id)
        vals = {}
        data_id = self.ids and self.ids[0] or False
        if not data_id or not active_id:
            return False
        data = self.browse(data_id)
        email_from = tools.config.get('email_from', False)
        user = user_pool.browse(uid)
        try:
            temp_id =\
                self.env['ir.model.data'].\
                get_object_reference('project_scrum',
                                     'email_template_project_scrum')[1]
        except ValueError:
            raise ValidationError(_('Email Template not Found'))
        if temp_id:
            mail_temp = self.env['mail.template'].browse(temp_id)
            user_email = email_from or user.partner_id.email
            body = """
                    <div>
                    <p>%s</p>
                    <p>Tasks since yesterday : %s</p>
                    <p>Task for Today : %s</p>
                    <p>Blocking points encountered : %s</p>
                    <p>Thank you, %s</p>
                    <p>%s</p>
                    </div>""" \
                    % (data.message, meeting.question_yesterday or '',
                       meeting.question_today or '',
                       meeting.question_blocks or '',
                       user.name, user.signature
                       )
            vals['subject'] = data.subject
            vals['email_from'] = user_email
            if mail_temp:
                vals['body_html'] = body
            if data.scrum_master_email == data.product_owner_email:
                data.product_owner_email = False
            if data.scrum_master_email:
                resp.append(data.scrum_master_email)
            if data.product_owner_email:
                resp.append(data.product_owner_email)
            vals['email_to'] = ','.join(x for x in resp)
            mail_temp.write(vals)
            mail_temp.send_mail(meeting.id, force_send=True)
        return {'type': 'ir.actions.act_window_close'}
