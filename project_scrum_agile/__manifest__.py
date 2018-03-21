# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Project Scrum Management',
    'version': '11.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.,David DRAPEAU',
    'category': 'Project Scrum Management',
    'website': "http://www.serpentcs.com",
    'description': '''
    This application respects the scrum.org protocol
    and has been developed and is maintained by ITIL Certified Member
    (in course of certification).
    * Linked to OpenERP native module 'project'

Manage
    * Project roles
        * Scrum Master
        * Product Owner
        * Development Team (inherits from project module)
    * Releases
    * Sprints
        * date_start and date_stop
        * standup meetings for each user of team (TODO)
        * sprint review
        * sprint retrospective
        * planned velocity (you write velocity desired and
        displayed on Sprint Velocity Chart)
        * effective velocity (it is computed by all users
        stories affected to the sprint)
        * effective velocity done (it is computed by all users stories done
        and displayed on Sprint Velocity Chart)
    * Product Backlog (users stories)
        * new kanban view
        * date_open and date_done
        * story complexity points
        * text area for describe tests acceptance
    * Display charts
        * Burdown Chart (based on story points)
        * Sprints Velocity (for each Scrum project)
    * Sandbox
        * a developer of development team can add a user story to sandbox
        * the product owner can valid it
        (transfer into product backlog) or delete it
    ''',
    'sequence': 1,
    'depends': [
                'sale_timesheet',
                'calendar',
                'document',
    ],
    'data': [
        'security/project_scrum_security.xml',
        'security/ir.model.access.csv',
        'views/email_template.xml',
        'views/hr_employee_view.xml',
        'views/project_scrum_view.xml',
        'views/account_analytic_line_view.xml',
        'views/project_view.xml',
        'wizard/user_story_sandbox_to_backlog_view.xml',
        'wizard/project_scrum_backlog_create_task_view.xml',
        'views/project_scrum_sandbox_view.xml',
        'views/project_scrum_release_view.xml',
        'views/project_scrum_role_view.xml',
        'wizard/project_scrum_email_view.xml',
        'wizard/analytic_timesheet_view.xml',
        'data/project_scrum_extended_data.xml',
        'views/project_scrum_devteam_view.xml',
    ],
    'images': ['static/description/img/ProjectScrumBanner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 45,
    'currency': 'EUR',
}
