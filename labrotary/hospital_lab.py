# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime
# classes under  menu of laboratry 

class Hospital_lab_System(models.Model):

    _name = 'hospital.lab'
    _description = 'Medical Lab'

    name = fields.Char('ID')
    test_id = fields.Many2one('hospital.test_type', 'Test Type', required = True)

    date_analysis =  fields.Datetime('Date of the Analysis' , default = datetime.now())
    patient_id = fields.Many2one('patient.info','Patient', required = True)
    date_requested = fields.Datetime('Date requested',  default = datetime.now())
    medical_lab_physician_id = fields.Many2one('doctors.profile','Pathologist')
    requestor_physician_id = fields.Many2one('doctors.profile','Physician', required = True)

    critearea_ids = fields.One2many('hospital_test.critearea','medical_lab_id', 'Critearea')
    results= fields.Text('Results')
    diagnosis = fields.Text('Diagnosis')
    is_invoiced = fields.Boolean(copy=False,default = False)
   
    
    @api.model
    def create(self,val):
        val['name'] = self.env['ir.sequence'].next_by_code('ltest_seq')
        result = super(Hospital_lab_System, self).create(val)
        if val.get('test_id'):
            critearea_obj= self.env['hospital_test.critearea']
            criterea_ids = critearea_obj.search([('test_id', '=',val['test_id'] )])
            for id in   criterea_ids:
                critearea_obj.write({'medical_lab_id':result})

        return result

    @api.onchange('critearea_ids')  # To Generate the item serial No dynamically
    def onchange_hospital_lab_test_case_line_ids(self):  #
        seq = 0  #
        for line in self.critearea_ids:
            seq += 1
            line.seq = seq

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
