# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime

class hospital_patients_medications(models.Model):
    _name = 'hospital.patient.medication'
    _description = 'hospital patient medication'
    _rec_name = 'medical_patients_medication_id'

    medical_medicament_id = fields.Many2one('hospital.medicament', string='Medicament', required=True)
    medical_patients_medication_id = fields.Many2one('patient.info', string='Medication')
    is_active = fields.Boolean(string='Active', default=True)
    start_treatment = fields.Datetime(string='Start Of Treatment', required=True)
    course_completed = fields.Boolean(string="Course Completed")
    doctor_physician_id = fields.Many2one('doctors.profile', string='Physician')
    indication_pathology_id = fields.Many2one('hospital.pathology', string='Indication')
    end_treatment = fields.Datetime(string='End Of Treatment', required=True)
    discontinued = fields.Boolean(string='Discontinued')
    drug_route_id = fields.Many2one('hospital.drug.route', string=" Administration Route ")
    dose = fields.Float(string='Dose')
    qty = fields.Integer(string='X')
    dose_unit_id = fields.Many2one('hospital.dose.unit', string='Dose Unit')
    duration = fields.Integer(string="Treatment Duration")
    duration_period = fields.Selection([('minutes', 'Minutes'),
                                        ('hours', 'hours'),
                                        ('days', 'Days'),
                                        ('months', 'Months'),
                                        ('years', 'Years'),
                                        ('indefine', 'Indefine')], string='Treatment Period')
    medication_dosage_id = fields.Many2one('hospital.medication.dosage', string='Frequency')
    admin_times = fields.Char(string='Admin Hours')
    frequency = fields.Integer(string='Frequency')
    frequency_unit = fields.Selection([('seconds', 'Seconds'),
                                       ('minutes', 'Minutes'),
                                       ('hours', 'hours'),
                                       ('days', 'Days'),
                                       ('weeks', 'Weeks'),
                                       ('wr', 'When Required')], string='Unit')
    notes = fields.Text(string='Notes')

# vim=expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
