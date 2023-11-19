# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class hospital_drug_route(models.Model):
    _name = 'hospital.drug.route'
    _description = 'hospital Drug Route'

    name = fields.Char(string="Route",required=True)
    code = fields.Char(string="Code")

