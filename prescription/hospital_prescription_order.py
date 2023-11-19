# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime

class hospital_prescription_order(models.Model):
    _name = "hospital.prescription.order"
    _description = 'hospital Prescription order'

    name = fields.Char('Prescription ID')
    patient_id = fields.Many2one('patient.info','Patient Name')
    prescription_date = fields.Datetime('Prescription Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users','Login User',readonly=True, default=lambda self: self.env.user)
    no_invoice = fields.Boolean('Invoice exempt')
    inv_id = fields.Many2one('account.invoice', 'Invoice')
    invoice_to_insurer = fields.Boolean('Invoice to Insurance')
    doctor_id = fields.Many2one('doctors.profile','Prescribing Doctor')
    medical_appointment_id = fields.Many2one('appointment.booking','Appointment')
    state = fields.Selection([('invoiced','To Invoiced'),('tobe','To Be Invoiced')], 'Invoice Status')
    pharmacy_partner_id = fields.Many2one('res.users', string='Pharmacy')
    prescription_line_ids = fields.One2many('hospital.prescription.line','name','Prescription Line')
    invoice_done= fields.Boolean('Invoice Done')
    notes = fields.Text('Prescription Note')

    appointment_id = fields.Many2one('appointment.booking')
    is_invoiced = fields.Boolean(copy=False,default = False)
    insurer_id = fields.Many2one('hospital.insurance', 'Insurer')
    is_shipped = fields.Boolean(default  =  False,copy=False)


    @api.model
    def create(self , vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.prescription.order') or '/'
        return super(hospital_prescription_order, self).create(vals)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record:
            name_text = 'Prs-010' + str(record.id)
            record.update({'name': name_text, 'state': 'invoiced'})
        return record


    def prescription_report(self):
        return self.env.ref('general_hospital_v_03.action_report_print_prescription').report_action(self)

    @api.onchange('name')
    def onchange_name(self):
        ins_obj = self.env['hospital.insurance']
        ins_record = ins_obj.search([('medical_insurance_partner_id', '=', self.patient_id.id)])
        self.insurer_id = ins_record.id or False

    def btn_customer_cancel(self):
        self.ensure_one()
        self.state = 'cancelled'

    def btn_customer_invoice(self):
        self.ensure_one()
        self.state = 'create_invoice'

    def btn_consultancy_invoice(self):
        self.ensure_one()
        self.state = 'consultancy_invoice'

    def btn_medicine_send_pharmacy(self):
        self.ensure_one()
        self.state = 'send_to_pharmacy'

    def btn_print_prescription(self):
        self.ensure_one()
        self.state = 'print_prescription'


