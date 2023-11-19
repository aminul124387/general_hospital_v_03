# -*- coding: utf-8 -*-
{
    'name': "Kolpolok General Hospital Demo",
    'summary': "",
    'description': "Kolpolok General Hospital",
    'sequence': '-01',
    'author': "Kolpolok Service Limited",
    'version': '0.1',
    'depends': ['base','mail','product','stock'],
    'assets': {'web.asset_backend':['lions_Hospital_v_03/static/src/css/custom.css',],'web.asset_fronted':['lions_Hospital_v_03/static/src/css/custom.css',],},

    'data': [
        'security/ir.model.access.csv',

        'admission/admission_report_wizard.xml',
        'admission/admission_reverse_form.xml',
        'money_receipt/wizard_money_receipt_view.xml',
        'investigation/investigation_reverse_form.xml',
        'appointment/report/appointment_wizard_details_report_format.xml',

        'profile/patient/patient_report_wizard.xml',

        'ambulance/ambulance_view.xml',
        'ambulance/ambulance_booking_view.xml',
        'ambulance/ambulance_expense_view.xml',

        'admission/pending_admission_form_view.xml',
        'admission/release_note/release_note.xml',
        # 'admission/item_entry_view.xml',
        'investigation/report/report_view.xml',
        'investigation/report/investigation_bill_print.xml',
        'investigation/report/invoice_bill_print.xml',


        'inventory/inventory_form_view.xml',

        'money_receipt/report/report_view.xml',
        'money_receipt/report/money_receipt_form_print.xml',
        'money_receipt/report/money_receipt_report_print_format.xml',
        #

        'admission/report/details_admission_report_print.xml',
        'admission/report/admission_form_print.xml',

        'diagnosis/diagnosis_form_view.xml',


        'admission/report/release_print_view.xml',
        'appointment/report/appointment_print_view.xml',
        'appointment/report/details_appointment_view.xml',
        'appointment/appointment_booking_view.xml',
        'appointment/appointment_paid_view.xml',
        'appointment/appointment_payment_view.xml',
        'appointment/investigation_payment_view.xml',
        'appointment/create_appointment_view.xml',

        'bill_payment/bill_payment_form.xml',
        'bill_payment/payment_type.xml',
        'bill_payment/advance_cash_view.xml',
        'money_receipt/money_receipt_view.xml',

        'blood_bank/blood_donor_view.xml',
        'blood_bank/blood_receiver_view.xml',

        'cash_collection/cash_collection_view.xml',
        'cash_collection/cc_collection_report_wizard.xml',
        'cash_collection/report/cc_collection_report_print_view.xml',
        'cash_collection/report/cc_collection_wizard_report_format_download.xml',

        'commission_configure/commission_configure_view.xml',
        'commission_configure/commission_payment_view.xml',

        'configure/prescriptions.xml',
        'configure/department_config.xml',
        'configure/item_entry_view.xml',
        'configure/package_view.xml',
        'configure/cancel_bill_view.xml',
        'configure/hospital_patient_disease.xml',
        'configure/hospital_pathology_category.xml',
        'configure/hospital_pathology.xml',
        # 'commission_configure/corporate_discount_configure_view.xml',

        'discount/pending_discount.xml',
        'discount/discount_category.xml',
        'discount/discount_configuration.xml',
        'discount/corporate_discount_configuration.xml',

        'medication/hospital_patient_medication.xml',
        'medication/hospital_medicament.xml',
        'medication/hospital_vaccination.xml',

        'hospital_drug/hospital_dose_unit.xml',
        'hospital_drug/hospital_drug_route.xml',


        'emergency_admission/emergency_admission_form_view.xml',

        'investigation/bill_view.xml',
        # 'investigation/reverse_bill_view.xml',

        'laundry_linen/linen_entry_view.xml',

        'labrotary/hospital_lab.xml',
        'labrotary/hospital_test_type.xml',
        'labrotary/hospital_test_critearea.xml',
        'labrotary/hospital_lab_test_units.xml',
        'labrotary/hospital_patient_lab_test.xml',


        'labrotary/report/report_view.xml',
        'labrotary/report/hospital_view_report_lab_result_demo_report.xml',
        #
        # 'labrotary/wizard/hospital_lab_test_invoice_wizard.xml',

        'money_receipt/journal/journal_receipt_view.xml',

        'opd/report/report_view.xml',
        'opd/report/opd_form_print.xml',

        # 'opd/inventory_form_view.xml',
        'opd/opd_ticket_item_view.xml',
        'opd/opd_ticket_form_view.xml',

        'optic_sale/optic_lens_view.xml',
        'optic_sale/optic_sale_view.xml',

        'profile/patient/patient_view.xml',
        'profile/patient/report/patient_card.xml',
        'profile/broker/broker_view.xml',
        'profile/doctor/doctors_view.xml',
        'profile/gaurantor/guarantor_form_view.xml',

        'profile/patient/report/patient_report_print_format.xml',
        'profile/patient/report/patient_diseases_document_report.xml',
        'profile/patient/report/patient_medications_document_report.xml',
        'profile/patient/report/patient_vaccinations_document_report.xml',

        'insurrance/hospital_insurance.xml',
        'insurrance/hospital_insurance_plan.xml',


        # 'configure/res_partner.xml',



        'prescription/hospital_prescription_line.xml',
        'prescription/hospital_prescription_order.xml',
        'prescription/report/hospital_prescription_demo_report.xml',
        'prescription/report/report_view.xml',


        'pharmacy_item/pharmacy_item_view.xml',

        'ward_management/ward_management_views.xml',
        'ward_management/bed_cabin_management.xml',
        'security/hospital_security.xml',

        'report/mail_template.xml',
        'report/mail_template_appointment.xml',
        # 'report/custom_header_footer.xml',
        'report/report_view.xml',


    ],
    'installable': True,
    'auto_install': False
}
