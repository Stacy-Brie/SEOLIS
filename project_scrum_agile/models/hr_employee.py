# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    product_id = fields.Many2one('product.product', 'Product')
    journal_id = fields.Many2one('account.journal', 'Analytic Journal')
    project_task = fields.Many2one('project.task', 'Task')
