# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class BacklogCreateTask(models.TransientModel):
    _name = 'project.scrum.backlog.create.task'
    _description = 'Create Tasks from Product Backlogs'

    user_id = fields.Many2one(
        'res.users',
        'Assign To',
        help="Responsible user who can work on task"
    )

    @api.multi
    def do_create(self):
        """ Create Tasks from Product Backlogs
        @param self: The object pointer
        """
        context = self._context or {}
        task = self.env['project.task']
        backlog_id = self.env['project.scrum.product.backlog']
        document_pool = self.env['ir.attachment']
        ids_task = []
        backlogs = backlog_id.browse(context['active_ids'])
        search_view_ref = self.env.ref('project.view_task_search_form', False)
        for backlog in backlogs:
            task_id = task.create({
                'product_backlog_id': backlog.id,
                'name': backlog.name,
                'description': backlog.description,
                'project_id': backlog.project_id.id,
                'user_id': self.user_id and self.user_id.id or False,
                'planned_hours': backlog.expected_hours,
                'remaining_hours': backlog.expected_hours,
                'sequence': backlog.sequence,
            })
            document_ids = document_pool.search(
                [('res_id', '=', backlog.id),
                 ('res_model', '=', backlog_id._name)])
            for document_id in document_ids:
                document_id.copy(default={'res_id': task_id.id,
                                          'res_model': task._name})
            ids_task.append(task_id.id)
        return {
            'domain': "[('product_backlog_id','in',[" + ','.join(
                map(str, context['active_ids'])) + "])]",
            'name': 'Tasks',
            'res_id': ids_task,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'search_view_id': search_view_ref and search_view_ref.id
        }
