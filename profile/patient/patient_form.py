import base64
import string


from dateutil.relativedelta import relativedelta
from odoo.addons.general_hospital_v_03.blood_bank.blood_bank import _
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.modules import get_module_resource
from odoo.tools.safe_eval import datetime
from datetime import date,datetime



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
    report_date = fields.Date('Date', default=datetime.today().date())
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

    age = fields.Char(compute='onchange_age', string="Patient Age",store=True, readonly=True)
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

    street = fields.Char(readonly=False)
    street2 = fields.Char(readonly=False)
    zip_code = fields.Char( readonly=False)
    city = fields.Char( readonly=False)
    state_id = fields.Many2one("res.country.state", readonly=False)
    country_id = fields.Many2one('res.country', readonly=False)
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

    prescription_info = fields.One2many('hospital.prescription.order', 'patient_id', 'Prescription')
    prescriptions_count = fields.Integer(string='Prescription', compute='count_prescriptions')



    # New update Notebook field ----------
    date_of_birth = fields.Date(string="Date of Birth")
    deceased = fields.Boolean(string='Deceased')
    date_of_death = fields.Date(string="Date of Death")
    cause_of_death = fields.Char(string='Cause of Death')
    general_info = fields.Text(string="Info")
    patient_disease_ids = fields.One2many('hospital.patient.disease', 'hospital_patient_id')
    #-
    ses = fields.Selection([
        ('None', ''),
        ('0', 'Lower'),
        ('1', 'Lower-middle'),
        ('2', 'Middle'),
        ('3', 'Middle-upper'),
        ('4', 'Higher'),
    ], 'Socioeconomics', help="SES - Socioeconomic Status", sort=False)
    education = fields.Selection([('o', 'None'), ('1', 'Incomplete Primary School'),
                                  ('2', 'Primary School'),
                                  ('3', 'Incomplete Secondary School'),
                                  ('4', 'Secondary School'),
                                  ('5', 'University')], string='Education Level')
    housing = fields.Selection([
        ('None', ''),
        ('0', 'Shanty, deficient sanitary conditions'),
        ('1', 'Small, crowded but with good sanitary conditions'),
        ('2', 'Comfortable and good sanitary conditions'),
        ('3', 'Roomy and excellent sanitary conditions'),
        ('4', 'Luxury and excellent sanitary conditions'),
    ], 'Housing conditions', help="Housing and sanitary living conditions", sort=False)
    works_at_home = fields.Boolean('Works At Home')
    hours_outside = fields.Integer('Hours outside home',
                                   help="Number of hours a day the patient spend outside the house")
    hostile_area = fields.Boolean('Hostile Area')
    sewers = fields.Boolean('Sanitary Sewers')
    water = fields.Boolean('Running Water')
    trash = fields.Boolean('Trash recollection')
    electricity = fields.Boolean('Electrical supply')
    gas = fields.Boolean('Gas supply')
    telephone = fields.Boolean('Telephone')
    television = fields.Boolean('Television')
    internet = fields.Boolean('Internet')
    ses_notes = fields.Text('Notes')
    fam_apgar_help = fields.Selection([
        ('None', ''),
        ('0', 'None'),
        ('1', 'Moderately'),
        ('2', 'Very much'),
    ], 'Help from family',
        help="Is the patient satisfied with the level of help coming from the family when there is a problem ?",
        sort=False)
    fam_apgar_discussion = fields.Selection([
        ('None', ''),
        ('0', 'None'),
        ('1', 'Moderately'),
        ('2', 'Very much'),
    ], 'Problems discussion',
        help="Is the patient satisfied with the level talking over the problems as family ?", sort=False)
    fam_apgar_decisions = fields.Selection([
        ('None', ''),
        ('0', 'None'),
        ('1', 'Moderately'),
        ('2', 'Very much'),
    ], 'Decision making',
        help="Is the patient satisfied with the level of making important decisions as a group ?", sort=False)
    fam_apgar_timesharing = fields.Selection([
        ('None', ''),
        ('0', 'None'),
        ('1', 'Moderately'),
        ('2', 'Very much'),
    ], 'Time sharing',
        help="Is the patient satisfied with the level of time that they spend together ?", sort=False)
    fam_apgar_affection = fields.Selection([
        ('None', ''),
        ('0', 'None'),
        ('1', 'Moderately'),
        ('2', 'Very much'),
    ], 'Family affection',
        help="Is the patient satisfied with the level of affection coming from the family ?", sort=False)
    single_parent = fields.Boolean('Single parent family')
    domestic_violence = fields.Boolean('Domestic violence')
    working_children = fields.Boolean('Working children')
    teenage_pregnancy = fields.Boolean('Teenage pregnancy')
    sexual_abuse = fields.Boolean('Sexual abuse')
    drug_addiction = fields.Boolean('Drug addiction')
    school_withdrawal = fields.Boolean('School withdrawal')
    prison_past = fields.Boolean('Has been in prison')
    prison_current = fields.Boolean('Is currently in prison')
    relative_in_prison = fields.Boolean('Relative in prison',help="Check if someone from the nuclear family - parents sibblings  is or has been in prison")
    fertile = fields.Boolean('Fertile')
    currently_pregnant = fields.Boolean('Currently Pregnant')
    menarche = fields.Integer('Menarche age')
    menopausal = fields.Boolean('Menopausal')
    menopause = fields.Integer('Menopause age')
    breast_self_examination = fields.Boolean('Breast self-examination')
    mammography = fields.Boolean('Mammography')
    mammography_last = fields.Date('Last mammography')
    pap_test_last = fields.Date('Last PAP Test')
    pap_test = fields.Boolean('PAP test')
    colposcopy = fields.Boolean('Colpscopy')
    colposcopy_last = fields.Date('Last colposcopy')
    gpa = fields.Char('GPA')
    deaths_2nd_week = fields.Integer('Deceased after 2nd week')
    deaths_1st_week = fields.Integer('Deceased after 1st week')
    full_term = fields.Integer('Full Term')
    gravida = fields.Integer('Pregnancies')
    born_alive = fields.Integer('Born Alive')
    premature = fields.Integer('Premature')
    abortions = fields.Integer('Abortions')
    # perinatal_ids = fields.Many2many('medical.preinatal')
    excercise = fields.Boolean(string='Excercise')
    excercise_minutes_day = fields.Integer(string="Minutes/Day")
    sleep_hours = fields.Integer(string="Hours of sleep")
    sleep_during_daytime = fields.Boolean(string="Sleep at daytime")
    number_of_meals = fields.Integer(string="Meals per day")
    coffee = fields.Boolean('Coffee')
    coffee_cups = fields.Integer(string='Cups Per Day')
    eats_alone = fields.Boolean(string="Eats alone")
    soft_drinks = fields.Boolean(string="Soft drinks(sugar)")
    salt = fields.Boolean(string="Salt")
    diet = fields.Boolean(string=" Currently on a diet ")
    diet_info = fields.Integer(string=' Diet info ')
    lifestyle_info = fields.Text('Lifestyle Information')
    #-
    smoking = fields.Boolean(string="Smokes")
    smoking_number = fields.Integer(string="Cigarretes a day")
    ex_smoker = fields.Boolean(string="Ex-smoker")
    second_hand_smoker = fields.Boolean(string="Passive smoker")
    age_start_smoking = fields.Integer(string="Age started to smoke")
    age_quit_smoking = fields.Integer(string="Age of quitting")
    drug_usage = fields.Boolean(string='Drug Habits')
    drug_iv = fields.Boolean(string='IV hospital_drug user')
    ex_drug_addict = fields.Boolean(string='Ex hospital_drug addict')
    age_start_drugs = fields.Integer(string='Age started drugs')
    age_quit_drugs = fields.Integer(string="Age quit drugs")
    alcohol = fields.Boolean(string="Drinks Alcohol")
    ex_alcohol = fields.Boolean(string="Ex alcoholic")
    age_start_drinking = fields.Integer(string="Age started to drink")
    alcohol_beer_number = fields.Integer(string="Beer / day")
    alcohol_wine_number = fields.Integer(string="Wine / day")
    alcohol_liquor_number = fields.Integer(string="Liquor / day")
    #-
    sexual_preferences = fields.Selection([
        ('h', 'Heterosexual'),
        ('g', 'Homosexual'),
        ('b', 'Bisexual'),
        ('t', 'Transexual'),
    ], 'Sexual Orientation', sort=False)
    sexual_practices = fields.Selection([
        ('s', 'Safe / Protected sex'),
        ('r', 'Risky / Unprotected sex'),
    ], 'Sexual Practices', sort=False)
    sexual_partners = fields.Selection([
        ('m', 'Monogamous'),
        ('t', 'Polygamous'),
    ], 'Sexual Partners', sort=False)
    sexual_partners_number = fields.Integer('Number of sexual partners')
    first_sexual_encounter = fields.Integer('Age first sexual encounter')
    anticonceptive = fields.Selection([
        ('0', 'None'),
        ('1', 'Pill / Minipill'),
        ('2', 'Male condom'),
        ('3', 'Vasectomy'),
        ('4', 'Female sterilisation'),
        ('5', 'Intra-uterine device'),
        ('6', 'Withdrawal method'),
        ('7', 'Fertility cycle awareness'),
        ('8', 'Contraceptive injection'),
        ('9', 'Skin Patch'),
        ('10', 'Female condom'),
    ], 'Anticonceptive Method', sort=False)
    #-
    sex_oral = fields.Selection([('0', 'None'),
                                 ('1', 'Active'),
                                 ('2', 'Passive'),
                                 ('3', 'Both')], string='Oral Sex')
    sex_anal = fields.Selection([('0', 'None'),
                                 ('1', 'Active'),
                                 ('2', 'Passive'),
                                 ('3', 'Both')], string='Anal Sex')
    prostitute = fields.Boolean(string='Prostitute')
    sex_with_prostitutes = fields.Boolean(string=' Sex with prostitutes ')
    sexuality_info = fields.Text('Extra Information')
    motorcycle_rider = fields.Boolean('Motorcycle Rider', help="The patient rides motorcycles")
    helmet = fields.Boolean('Uses helmet', help="The patient uses the proper motorcycle helmet")
    traffic_laws = fields.Boolean('Obeys Traffic Laws', help="Check if the patient is a safe driver")
    car_revision = fields.Boolean('Car Revision', help="Maintain the vehicle. Do periodical checks - tires,breaks ...")
    car_seat_belt = fields.Boolean('Seat belt', help="Safety measures when driving : safety belt")
    car_child_safety = fields.Boolean('Car Child Safety',
                                      help="Safety measures when driving : child seats, proper seat belting, not seating on the front seat, ....")
    home_safety = fields.Boolean('Home safety',
                                 help="Keep safety measures for kids in the kitchen, correct storage of chemicals, ...")
    ex_alcoholic = fields.Boolean('Ex alcoholic')
    age_quit_drinking = fields.Integer(string="Age quit drinking")
    medication_ids = fields.One2many('hospital.patient.medication','medical_patients_medication_id')
    medical_vaccination_ids = fields.One2many('hospital.vaccination','medical_patient_vaccines_id')







    @api.depends('date_of_birth') # Calculate the patient age from the Date of Birth!
    def onchange_age(self):
        for rec in self:
            if rec.date_of_birth:
                d1 = rec.date_of_birth
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
            else:
                rec.age = "No Date Of Birth!!"

    @api.constrains('date_of_death') # Check Patient Death against the patient date of birth
    def _check_date_death(self):
        for rec in self:
            if rec.date_of_birth:
                if rec.deceased == True:
                    if rec.date_of_death <= rec.date_of_birth:
                        raise UserError(_('Date Of Death Can Not Less Than Date Of Birth.'))

    @api.model# This Function is use for the Patient Name Search!
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

    @api.depends('prescription_info')
    def count_prescriptions(self):
        for record in self:
            count = self.env['hospital.prescription.order'].search_count([('patient_id', '=', record.id)])
            record.prescriptions_count = count


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
