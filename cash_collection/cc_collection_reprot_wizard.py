from odoo import fields, models, api
from odoo.addons.test_convert.tests.test_env import data


class HospitalAppointmentReport(models.TransientModel):
    _name = 'cc.collection.report.wizard'
    _description = 'Print CC Report'

    date_from = fields.Datetime(string= "Date Form:")
    date_to = fields.Datetime(string= "Date To:")
    app_id = fields.Many2one('appointment.booking', string='Appointment Info')
    opd_id = fields.Many2one('opd.info', string='OPD Info')
    admission_id = fields.Many2one('admission.info', string='Admission Info')
    bill_id = fields.Many2one('bill.register', string='Bill Info')
    uid = fields.Many2one('res.users', 'Created By:', default=lambda self: self.env.user.id)
    # Create pdf report wizard from wizard report_wizard

    # def btn_cc_collection_report(self):
    #
    #     return self.env.ref('general_hospital_v_03.cc_collection_report_template_id').report_action(self, data)


    def btn_cc_collection_report(self, t_dat=None, end_date=None):
        st_dat = self.date_from
        end_date = self.date_to
        user_id = self.uid
        adm_info = {}

        bill_info = {}

        result = []
        if self.uid == 2:

            bill_q = "select sum(amount) as totla_collection, create_uid from leih_money_receipt where bill_id is not Null " \
                     "and state='confirm' and diagonostic_bill=TRUE and (create_date <= '%s') and (create_date >= '%s') group by create_uid"


            add_q = "select sum(amount) as totla_collection, create_uid from leih_money_receipt where admission_id is not Null" \
                    " and state='confirm' and (create_date <= '%s') and (create_date >= '%s') group by create_uid"


            self.cr.execute(bill_q % (end_date, st_dat))
            participant_ids = []
            bill_info = {}
            for items in self.cr.fetchall():
                if items[1] is not participant_ids:
                    participant_ids.append(items[1])
                bill_info[items[1]] = items[0]


            ## Bill Collction Ends Here
            ## It sis For Addmission Data Collction

            self.cr.execute(add_q % (end_date, st_dat))

            adm_info = {}
            for items in self.cr.fetchall():
                if items[1] is not participant_ids:
                    participant_ids.append(items[1])
                adm_info[items[1]] = items[0]

            ## Addmission Collction Ends Here

            ## OPD Data Query
            opd_q = "select sum(total) as total_b, create_uid from opd_ticket " \
                    "where state='confirmed' and (create_date <='%s') and (create_date >='%s') group by create_uid"

            self.cr.execute(opd_q % (end_date, st_dat))



        else:
            bill_q = "select sum(amount) as totla_collection, create_uid from money_receipt_id where bill_id is not Null " \
                     "and state='confirm' and diagonostic_bill=TRUE and (create_date <= '%s') and (create_date >= '%s') and (create_uid=%s) group by create_uid"


            add_q = "select sum(amount) as totla_collection, create_uid from leih_money_receipt where admission_id is not Null" \
                    " and state='confirm' and (create_date <= '%s') and (create_date >= '%s') and (create_uid=%s) group by create_uid"

            self.cr.execute(bill_q % (end_date, st_dat, user_id))
            participant_ids = []
            bill_info = {}
            for items in self.cr.fetchall():
                if items[1] is not participant_ids:
                    participant_ids.append(items[1])
                bill_info[items[1]] = items[0]



            ## Bill Collction Ends Here

            ## It sis For Addmission Data Collction

            self.cr.execute(add_q % (end_date, st_dat, user_id))

            adm_info = {}
            for items in self.cr.fetchall():
                if items[1] is not participant_ids:
                    participant_ids.append(items[1])
                adm_info[items[1]] = items[0]

            ## Addmission Collction Ends Here

            ## OPD Data Query
            opd_q = "select sum(total) as total_b, create_uid from opd_ticket " \
                    "where state='confirmed' and (create_date <='%s') and (create_date >='%s') and (create_uid=%s) " \
                    "group by create_uid"

            self.cr.execute(opd_q % (end_date, st_dat, user_id))



        participant_ids = list(set(participant_ids))
        ## Users Name Get

        user_q = "select res_partner.name,res_users.id from res_users, res_partner where res_users.partner_id=res_partner.id and res_users.id in %s"

        self.cr.execute(user_q, (tuple(participant_ids),))
        user_info = {}

        for items in self.cr.fetchall():
            user_info[items[1]] = items[0]
        ### Ends Here

        for user_id in participant_ids:
            b_amnt = bill_info.get(user_id) if bill_info.get(user_id) else 0
            adm_amnt = adm_info.get(user_id) if adm_info.get(user_id) else 0

            total = b_amnt + adm_amnt
            result.append({
                'user_name': user_info.get(user_id),
                'bill_collection': b_amnt,
                'admission_collection': adm_amnt,
                'total_collection': total,
            })

        return result