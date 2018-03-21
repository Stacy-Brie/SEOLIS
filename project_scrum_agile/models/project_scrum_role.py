# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProjectScrumRole(models.Model):
    _name = 'project.scrum.role'

    name = fields.Char('Name', size=128)
    code = fields.Char('Code', size=16)
    project_id = fields.Many2one('project.project', "Project")
    person_name = fields.Char('Person Name', size=128)
    person_description = fields.Text('Person Description')
