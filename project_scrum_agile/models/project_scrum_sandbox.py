# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProjectScrumSandbox(models.Model):
    _name = 'project.scrum.sandbox'

    role_id = fields.Many2one('res.partner', "Who")
    name = fields.Char('Wants', size=128)
    for_then = fields.Char('For', size=128)
    project_id = fields.Many2one(
        'project.project',
        "Project",
        required=True,
        domain=[('is_scrum', '=', True)]
    )
    developer_id = fields.Many2one(
        'res.users',
        'Author',
        default=lambda self: self.env.user
    )
    create_date = fields.Date('Date taken')
    meeting_id = fields.Many2one(
        'project.scrum.meeting',
        'Meeting'
    )
