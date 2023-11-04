from odoo import fields, models, api


class Department_Config(models.Model):
    _name = 'department.config'
    _rec_name = "dept_name"

    dept_name = fields.Char("Department Name")
    parent_dept = fields.Many2one('department.config', 'Parent Department')


    _sql_constraints = [
        ('unique_tag_name', 'unique (dept_name)', 'Please Department Should  Unique.')
    ]

