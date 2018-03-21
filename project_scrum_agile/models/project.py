# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_scrum = fields.Boolean('Is it a Scrum Project ?', default=True)
    goal = fields.Text(
        'Goal',
        help="The document that includes the project,"
        "jointly between the team and the customer")
    scrum_master_id = fields.Many2one('res.users', 'Scrum Master')
    product_owner_id = fields.Many2one('res.users', 'Product Owner')
    team_id = fields.Many2one('project.scrum.devteam', 'Team')
    backlog_count = fields.Integer(
        compute='_compute_backlog_count',
        string="Number of Backlog"
    )

    @api.model
    def create(self, vals):
        res = super(ProjectProject, self).create(vals)
        domain = ['|', ('default_view', '=', True), ('fold', '=', True)]
        for stage_ids in self.env['project.task.type'].search(domain):
            stage_ids.write({'project_ids': [(4, res.id)]})
        return res

    @api.multi
    def _compute_backlog_count(self):
        for project in self:
            project.backlog_count =\
                self.env['project.scrum.product.backlog'].search_count(
                    [('project_id', '=', project.id)])


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    default_view = fields.Boolean(
        'Default View',
        help="This stage will show you in kanban and form as well"
    )
