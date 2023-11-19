from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.addons.general_hospital_v_03.blood_bank.blood_bank import _
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import ValidationError

from odoo import exceptions

class ModelName(models.Model):
    _name = "optics.sale"
    _rec_name = 'optic_sale_id'
    # _inherit = 'product.product'

    date = fields.Datetime("Date", default=fields.Datetime.now())
    optic_sale_id = fields.Char("Optic Sale ID", readonly=True)
    patient_name = fields.Many2one('patient.info', "Patient Name")
    patient_id = fields.Char(related='patient_name.patient_id', string="Patient Id", readonly=True)
    mobile = fields.Char(string="Mobile", readonly=True, related='patient_name.mobile')
    address = fields.Char("Address", related='patient_name.address')
    age = fields.Char("Age", related='patient_name.age')
    gender = fields.Selection("Gender", related='patient_name.gender')

    right_eye_sph = fields.Char('Right Eye SPH')
    right_eye_cyl = fields.Char('Right Eye CYL')
    right_eye_axis = fields.Char('Right Eye AXIS')
    right_eye_sph_n = fields.Char('Right Eye SPH -N')
    right_eye_cyl_n = fields.Char('Right Eye CYL -N')
    right_eye_axis_n = fields.Char('Right Eye AXIS -N')
    left_eye_sph = fields.Char('Left Eye SPH')
    left_eye_cyl = fields.Char('Left Eye CYL')
    left_eye_axis = fields.Char('Left Eye AXIS')
    left_eye_sph_n = fields.Char('Left Eye SPH -N')
    left_eye_cyl_n = fields.Char('Left Eye CYL -N')
    left_eye_axis_n = fields.Char('Left Eye AXIS -N')
    hard_cover = fields.Boolean("Cover", default=True)
    cell_pad = fields.Boolean("Cell Pad", default=True)

    product_frame_id = fields.Many2one('product.product',string='Frame')
    quantity = fields.Integer('Quantity', default=1)
    qty_available = fields.Float("Stock Quantity", related='product_frame_id.qty_available', compute='btn_action_confirm',  readonly=True)
    frame_price = fields.Float('Price', related='product_frame_id.list_price')
    total_frame_price = fields.Float('Total Frame Price', compute='_compute_opt_frame_qty_price')

    delivery_date = fields.Date(string="Delivery Date")
    optics_sale_item_line_id = fields.One2many(comodel_name='optics.sale.line', inverse_name='optics_lens_item_id', string='Lens Entry')
    optics_sale_payment_line_id = fields.One2many("optics.sale.payment.line", "optics_payment_item_id","Optics Payment ID")
    # optics_sale_journal_line_id = fields.One2many("optics.journal.relation.line", "journal_item_id","Journal Payment ID")
    money_receipt_id = fields.Many2one('money.receipt', string='Money Receipt')
    bill_payments = fields.One2many(string="Payments", comodel_name='bill.bill_pay', inverse_name='optic_sale_id')
    card_no = fields.Char('Card No.')
    bank_name = fields.Char('Bank Name')
    state = fields.Selection([
        ('pending', 'Pending')
        , ('confirmed', 'Confirmed')
        , ('cancelled', 'Cancelled')], 'Status', default='pending', readonly=True)
    # Payement wise Field start Here -------------------
    payment_type = fields.Selection([('cash', 'Cash'), ('card', 'Card'), ('m_cash', 'MFS')], default='cash')
    cash_amount = fields.Float(string='Cash Amount')
    psn = fields.Many2one('payment.type', string="Payment A/C")
    mcash_mobile_no_payment = fields.Char(string="M-Cash Mobile", placeholder='Enter Last 4 Digit', attrs={'invisible': [('payment_type', '!=', 'm_cash')]})
    mfs_amount = fields.Float(string='Cash Amount')
    ac_no = fields.Char("A/C No.")
    card_no_payment = fields.Char(string="Card Number",attrs={'invisible': [('payment_type', '!=', 'card')]})
    card_amount =fields.Float(string='Card Amount')
    total_without_discount = fields.Integer("Total Without Discount", digits='Discount', compute='_onchange_total_amount')
    discount_percent = fields.Integer("Discount (%)", default=0.0, digits='Discount')
    total = fields.Float("Grand Total")
    other_discount = fields.Integer("Fixed Discount", default=0.0, digits='Discount')
    adv = fields.Float(string="Advance", default=0.0)
    paid = fields.Float(string="Paid")
    due_amount = fields.Float("Due Amount")






    def btn_action_confirm(self):
        if self.state == 'confirmed':
            raise ValidationError("This Item is already confirmed.")
        elif self.state == 'cancelled':
            raise ValidationError("Sorry! You cannot Confirm the Cancel Bill!")

        if self.quantity > 0:  # Check if the quantity is 1 or more
            product = self.product_frame_id
            if product:
                product.with_context(increase=False).write({'qty_available': product.qty_available - self.quantity})

        self.state = 'confirmed'
        if self.adv > 0:
            money_receipt = self.env['money.receipt'].create({  # Investigation data transfer to the Money Receipt Model
                'date': self.date,
                'optic_sale_id': self.id,
                'total': self.total,
                'adv': self.adv,
                'due_amount': self.due_amount,
                'ac_no': self.ac_no,
                'psn': self.id,
                'mcash_mobile_no_payment': self.mcash_mobile_no_payment,
                'card_amount': self.card_amount,
                'mfs_amount': self.mfs_amount,
                'cash_amount': self.cash_amount,
                'card_no_payment': self.card_no_payment,
                'payment_type': 'adv'
            })
            payment_vals = {
                'money_receipt_id': money_receipt.id,
                'date': datetime.now(),
                'adv': self.adv,
                'payment_type': 'Advance',  # replace with actual payment type
                'optics_payment_item_id': self.id  # link to the bill record
            }
            self.env['optics.sale.payment.line'].create(payment_vals)

    # def btn_action_confirm(self):  # This function use to Confirm and Print report
    #     if self.status == 'confirmed':
    #         raise ValidationError("This Item is already confirmed.")
    #     elif self.status == 'cancelled':
    #         raise ValidationError("Sorry! You cannot Confirmed the Cancel Bill! ")
    #     self.status = 'confirmed'
    #     if self.adv > 0:
    #         money_receipt = self.env['money.receipt'].create({  # Investigation data transfer to the Money Receipt Model
    #             'date': self.date,
    #             'optic_sale_id': self.id,
    #             'total': self.total,
    #             'adv': self.adv,
    #             'due_amount': self.due_amount,
    #             'ac_no': self.ac_no,
    #             'psn': self.id,
    #             'mcash_mobile_no_payment': self.mcash_mobile_no_payment,
    #             'card_amount': self.card_amount,
    #             'mfs_amount': self.mfs_amount,
    #             'cash_amount': self.cash_amount,
    #             'card_no_payment': self.card_no_payment,
    #             'payment_type': 'adv'
    #         })
    #         payment_vals = {
    #             'money_receipt_id': money_receipt.id,
    #             'date': datetime.now(),
    #             'adv': self.adv,
    #             'payment_type': 'Advance',  # replace with actual payment type
    #             'optics_payment_item_id': self.id  # link to the bill record
    #         }
    #         self.env['optics.sale.payment.line'].create(payment_vals)

    def add_payment_btn(self):  # Add Payment Function by click the Add Payment Button
        if self.state == 'pending':
            raise ValidationError("First Confirm the Bill")
        if self.total <= self.paid:
            raise ValidationError("The bill is already Paid")
        template_id = self.env.ref('general_hospital_v_03.bill_pay_form_view').id

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': template_id,
            'res_model': 'bill.bill_pay',
            'target': 'new',
            'context': {
                # 'default_admission_id': self.id,
                # 'default_amount': self.due_amount
                'default_optic_sale_id': self.id,
                'default_amount': self.paid,
                'default_total': self.total,
                'default_due_amount': self.due_amount,
            }
        }


    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record:
            optic_name_text = 'OPT-010' + str(record.id)
            record.update({'optic_sale_id': optic_name_text})
        return record



    def btn_action_cancel(self):
        self.ensure_one()
        # if self.state == 'confirmed':
        #     raise UserError("Cannot Cancel a Confirmed admission.")
        self.state = 'cancelled'

    def btn_add_discount(self):
        pass
    def btn_pay_bill(self):
        pass

    @api.depends('frame_price', 'quantity')  # Frame price Amount Calculate
    def _compute_opt_frame_qty_price(self):
        for record in self:
            record.total_frame_price = record.frame_price * record.quantity
            if record.quantity < 0:
                raise ValidationError('Your Frame Quantity Cannot Be Negative!')

    @api.depends('optics_sale_item_line_id.total_amount', 'paid', 'total_without_discount', 'other_discount',
                 'card_amount', 'mfs_amount', 'cash_amount', 'total_frame_price')
    def _onchange_total_amount(self):
        for record in self:
            grand_total = sum(line.total_amount for line in record.optics_sale_item_line_id)
            record.total_without_discount = grand_total + record.total_frame_price
            record.total = record.total_without_discount
            record.adv = record.card_amount + record.mfs_amount + record.cash_amount
            if record.other_discount or record.adv:
                record.total = record.total - record.other_discount
            record.due_amount = record.total - record.paid - record.adv


class OpticsLensInfo(models.Model):
    _name = 'optics.sale.line'

    lens_name = fields.Many2one("optic.lens", "Lens Name", ondelete='cascade')
    price = fields.Float("Unit Price", related='lens_name.sell_price')
    qty = fields.Integer("Quantity", default=1)
    total_amount = fields.Integer("Total Amount", compute='_compute_opt_qty_price')
    optics_lens_item_id = fields.Many2one('optics.sale', 'Optics Lens Item Info')

    @api.depends('price', 'qty')
    def _compute_opt_qty_price(self):
        for record in self:
            record.total_amount = record.price * record.qty
            if record.qty < 0:
                raise ValidationError('Your Product Quantity Cannot Be Negative!')


class OpticSalePaymentLine(models.Model):
    _name = 'optics.sale.payment.line'


    optics_payment_item_id = fields.Many2one('optics.sale', 'bill register payment')
    date = fields.Datetime(string='Payment Date')
    paid = fields.Float(string='Payment Amount')
    adv = fields.Float(string='Advance')
    payment_type = fields.Char(string='Payment Type')
    card_no_payment = fields.Char(string='Card No.')
    user_id = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user.id)
    due_amount = fields.Float("Due Amount")
    money_receipt_id = fields.Many2one('money.receipt', 'Money Receipt ID')
    optics_bill_pay_id = fields.Many2one('bill.bill_pay', string='Optics Bill Pay')




# class OpticsJournalRelation(models.Model):
#     _name = 'optics.journal.relation.line'
#
#     journal_id = fields.Many2one('journal.receipt', string="Journal ID", ondelete='cascade')
#     jr_bill_pay_id = fields.Many2one('bill.bill_pay', string='Optics Bill Payment')
#     journal_item_id = fields.Many2one("optics.sale", "Information")
