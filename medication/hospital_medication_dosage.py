# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class hospital_medication_dosage(models.Model):
    _name = 'hospital.medication.dosage'
    _description = 'hospital medication dosage'
    
    name = fields.Char(string="Frequency",required=True)
    abbreviation = fields.Char(string="Abbreviation")
    code = fields.Char(string="Code")

