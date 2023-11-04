import base64
import string

from odoo.addons.general_hospital_v_03.blood_bank.blood_bank import _
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.modules import get_module_resource


class PatientInfo(models.Model):
    _name = 'patient.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'patient_id desc'
    # _inherit = ['mail.thread']

    user_id = fields.Many2one('res.users', 'Created By:', default=lambda self: self.env.user.id)
    patient_id = fields.Char(string='Patient ID', readonly=True)
    photo = fields.Binary(string='Photo')
    name = fields.Char(string='Patient Name', tracking=True, required=True, index=True)
    mobile = fields.Char(string='Mobile', tracking=True)
    barcode = fields.Char(string='Barcode')
    email = fields.Char(string='Email')
    blood_group = fields.Selection([
        ('a+', 'A+')
        , ('a-', 'A-')
        , ('b+', 'B+')
        , ('b-', 'B-')
        , ('ab+', 'AB+')
        , ('ab+', 'AB-')
        , ('o+', 'O+')
        , ('none', 'None')
        , ('o-', 'O-')], 'Blood Group', default='none')
    marital_status = fields.Selection([
        ('married', 'Married'),
        ('single', 'Single'),
        ('none', 'None')
    ], 'Marital Status', default='none')
    parent_name = fields.Char(string='Parent Name')
    partner_name = fields.Char(string='Partner Name')
    rh = fields.Char(string='RH')
    family_physician = fields.Many2one('doctors.profile', string='Family Physician')
    address = fields.Char(string='Address')
    date_of_birth = fields.Date(string='Date Of Birth')
    age = fields.Char(string='Age')
    is_company = fields.Boolean(string='Is a Company?', default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], default='male')

    state = fields.Selection([
        ('created', 'Created'),
        ('confirmed', 'Confirmed'),
        ('draft', 'Draft'),
        ('cancelled', 'Cancelled')], 'Status', default='draft', readonly=True)

    # ------------------ Admission Line Item Relation --------------------------------------------
    patient_line_id = fields.One2many('patient.info.line', 'patient_item_id', required=True)
    # ----------------------------------------------------------------------------------------------
    total = fields.Char(string='Total')
    grand_total = fields.Char(string='Grand Total')
    paid_amount = fields.Float(string='Paid Amount')

    admission_info = fields.One2many('admission.info', 'patient_name', "Bill Register",
                                     domain=[('state', '=', 'confirmed')])
    admission_count = fields.Integer(string='Admission', compute='count_admission')
    bill_info =fields.One2many('bill.register','patient_name', "Bill Register", domain=[('state', '=', 'confirmed')])
    bill_count = fields.Integer(string='Investigation', compute='count_bills')
    appointment_info = fields.One2many('appointment.booking', 'patient_name', 'Appointment', domain=[('state', '=', 'reached')])
    appointment_count = fields.Integer(string='Appointment', compute='count_appointment')
    evaluation_count = fields.Integer(string='Evaluation Count')


    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])

        if name:
            args += ['|', '|', ('name', operator, name), ('patient_id', operator, name),
                                     ('mobile', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)



    @api.depends('appointment_info')
    def count_appointment(self):
        for record in self:
            count = self.env['appointment.booking'].search_count([('patient_name', '=', record.id)])
            record.appointment_count = count


    def button_patient_card_send_by_email(self):
        mail_template = self.env.ref('general_hospital_v_03.patient_card_email_template')
        for patient in self:
            mail_template.send_mail(patient.id, force_send=True)


    @api.depends('admission_info')# This fucntion use to admission count in patien form
    def count_admission(self):
        self.admission_count = len(self.admission_info)


    def unlink(self):# This Function is used for the Bill Delete Validation Error!
        for record in self:
            if self.appointment_info or self.admission_info or self.bill_info:
                raise ValidationError("You cannot delete this, it has Admission or Appointment or Investigation!")
        try:
            return super(PatientInfo, self).unlink()
        except Exception as e:
            raise ValidationError(_("Something went wrong during the deletion: %s") % str(e))


    @api.depends('bill_info')
    def count_bills(self):
        self.bill_count = len(self.bill_info)

    # This Fuction is used for the name first letter capital  ===----------------------------
    @api.onchange('name')
    def onchange_name(self):
        self.name = string.capwords(self.name) if self.name else None
    # This Fuction is used Patient Image Show ===----------------------------
    @api.model
    def _default_image(self):
        ''' --- Method to get default Image --- '''
        image_path = get_module_resource('hr', 'static/src/img',
                                         'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())


    # This Fuction is used for the Cancel Button =========================== item_cancel
    def btn_customer_cancel(self):
        self.ensure_one()
        self.state = 'cancelled'

    def btn_customer_confirm(self):
        self.ensure_one()
        self.state = 'confirmed'

    def btn_view_medicine(self):
        pass
    def btn_view_prescriptions(self):
        pass
    def btn_view_labtest(self):
        pass
    def btn_view_ward_info(self):
        pass



    # @api.depends('dob')
    # def _compute_age(self):
    #     for record in self:
    #         if record.dob:
    #             today = datetime.datetime.now().date()
    #             age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
    #             record.age = age

    # This Function is used for Patient ID Generate


    @api.model
    def create(self, vals):
        record = super().create(vals)
        if not record.patient_id and not vals.get('patient_id'):
            name_text = 'P-010' + str(record.id)
            record.update({'patient_id': name_text,'state': 'created'})
        return record

        # This Function is used for the field Name show with the Customer ID Generate



    # def name_get(self):
    #     res = []
    #     for record in self:
    #         patient_name = record.name
    #         patient_id = record.patient_id or '--'
    #         res.append((record.id, f"{patient_name} {' '} {patient_id}"))
    #     return res

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, f"{record.name} {' '} {record.patient_id or '--'}"))
        return res



    # this function is for the barcode generate
    # def generate_barcode(barcode_value, barcode_type='code128', width=600, height=300, filename='barcode.png'):
    #     barcode_image = barcode.get(barcode_type, barcode_value, writer=ImageWriter())
    #     barcode_image.save(filename, options={'width': width, 'height': height})
    #
    # # Usage example:
    # generate_barcode('123456789', barcode_type='code128', width=600, height=300, filename='barcode.png')



# --------------------------------------------------  Note book menu Iten code ----------------
# =============================================================================================
class PatientLineInfo(models.Model):
    _name = 'patient.info.line'

    department = fields.Many2one(string='Department', related='item_name.department')
    price = fields.Float(string='Price', related='item_name.price')
    total_amount = fields.Float(string='Total Amount', related='item_name.total_amount')
    # -------------------------------- Relation change please---------
    item_name = fields.Many2one("item.entry", "Item Name", ondelete='cascade')
    patient_item_id = fields.Many2one('patient.info', "Information")

    # -------------------------------   This part is used for the onchange value item of notebook -----------------------------
