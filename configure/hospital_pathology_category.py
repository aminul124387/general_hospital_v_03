# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class hospital_pathology_category(models.Model):
    _name = 'hospital.pathology.category'
    _description = 'Hospital pathology category'
    
    name = fields.Char(string="Category Name",required=True)
    active = fields.Boolean(string="Active" , default = True)
    parent_id = fields.Many2one('hospital.pathology.category', string="Parent Category")

