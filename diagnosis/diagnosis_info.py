from odoo import fields, models, api


class Diagnosis_Info(models.Model):
    _name = 'diagnosis.info'
    _description = 'Diagnosis Info'
    _rec_name = 'diagnosis'

    diagnosis = fields.Char(string="Diagnosis Name")
    diag_id = fields.Char(string="Diagnosis No.", readonly=True)
    patient_id = fields.Many2one('patient.info', string="Patient Info")








    @api.model
    def create(self, vals):
        record = super().create(vals)
        if not record.diag_id and not vals.get('diag_id'):
            name_text = 'Diag-010' + str(record.id)
            record.update({'diag_id': name_text})
        return record