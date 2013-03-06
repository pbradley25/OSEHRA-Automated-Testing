'''
Created on November 2012

ADT Manager Menu Actions for Registration package testing

@author: pbradley
'''
import time
# import TestHelper
from Actions import Actions
import logging

class ADTActions (Actions):
    def __init__(self, VistAconn, scheduling=None, user=None, code=None):
        Actions.__init__(self, VistAconn, scheduling, user, code)

    def signon (self):
        if self.acode is None:
            self.VistA.wait('');
            self.VistA.write('S DUZ=1 D ^XUP')
        else:
            self.VistA.wait('')
            self.VistA.write('D ^ZU')
            self.VistA.wait('ACCESS CODE:')
            self.VistA.write(self.acode)
            self.VistA.wait('VERIFY CODE:')
            self.VistA.write(self.vcode)
            self.VistA.wait('//')
            self.VistA.write('')
            self.VistA.wait('Option:')
            self.VistA.write('ADT MANAGER MENU')
            self.VistA.wait('continue')
            self.VistA.write('')

    def write(self, string):
        self.VistA.write(string)

    def adt_setup(self):
        self.VistA.wait('OPTION NAME:')
        # DEFINE THE WARD
        self.VistA.write('WARD DEFINITION ENTRY')
        self.VistA.wait('NAME:')
        self.VistA.write('TESTWARD1')
        self.VistA.wait('No//')
        self.VistA.write('YES')
        self.VistA.wait('POINTER:')
        self.VistA.write('ClinicX')
        self.VistA.wait('ORDER:')
        self.VistA.write('5')
        self.VistA.wait('TESTWARD1//')
        self.VistA.write('')
        self.VistA.wait('WRISTBAND:')
        self.VistA.write('YES')
        self.VistA.wait('DIVISION:')
        self.VistA.write('VISTA MEDICAL CENTER')
        self.VistA.wait('INSTITUTION:')
        self.VistA.write('VISTA HEALTH CARE')
        self.VistA.wait('6100')
        self.VistA.write('')
        self.VistA.wait('BEDSECTION:')
        self.VistA.write('bedselect')
        self.VistA.wait('SPECIALTY:')
        self.VistA.write('Cardiac Surgery')
        self.VistA.wait('SERVICE:')
        self.VistA.write('S')
        self.VistA.wait('LOCATION:')
        self.VistA.write('north')
        self.VistA.wait('WARD:')
        self.VistA.write('1')
        self.VistA.wait('DATE:')
        self.VistA.write('T')
        self.VistA.wait('No//')
        self.VistA.write('YES')
        self.VistA.wait('BEDS:')
        self.VistA.write('20')
        self.VistA.wait('ILL:')
        self.VistA.write('1')
        self.VistA.wait('SYNONYM:')
        self.VistA.write('')
        self.VistA.wait('5//')
        self.VistA.write('')
        self.VistA.wait('TOTALS:')
        self.VistA.write('')
        self.VistA.wait('NAME:')
        self.VistA.write('')
        self.VistA.wait(self.VistA.prompt)
        self.VistA.write('D ^XUP')
        # SETUP BEDS
        self.VistA.wait('OPTION NAME:')
        self.VistA.write('ADT SYSTEM')
        self.VistA.wait('Option:')
        self.VistA.write('ADD')
        for sitem in [['1-A', 'bed1'], ['1-B', 'bed2'], ['2-A', 'bed3'], ['2-B', 'bed4']]:
            self.VistA.wait('NAME:')
            self.VistA.write(sitem[0])
            self.VistA.wait('No//')
            self.VistA.write('yes')
            self.VistA.wait('NAME:')
            self.VistA.write('')
            self.VistA.wait('DESCRIPTION:')
            self.VistA.write(sitem[1])
            self.VistA.wait('No//')
            self.VistA.write('yes')
            self.VistA.wait('ASSIGN:')
            self.VistA.write('TESTWARD1')
            self.VistA.wait('No//')
            self.VistA.write('yes')
            self.VistA.wait('ASSIGN:')
            self.VistA.write('')
        self.VistA.wait('NAME:')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')
        self.VistA.wait('YES//')
        self.VistA.write('')
        self.VistA.wait(self.VistA.prompt)
        self.VistA.write('D ^XUP')
        # ADD ENTRY TO FILE 395 DVB PARAMETERS
        self.VistA.wait('NAME:')
        self.VistA.write('ZZFILEMAN')
        self.VistA.wait('OPTION:')
        self.VistA.write('1')
        self.VistA.wait('INPUT TO WHAT FILE')
        self.VistA.write('395')
        self.VistA.wait('EDIT WHICH FIELD')
        self.VistA.write('ALL')
        self.VistA.wait('Select DVB PARAMETERS ONE:')
        self.VistA.write('1')
        self.VistA.wait('No//')
        self.VistA.write('yes')
        self.VistA.wait('SCREENS?:')
        self.VistA.write('NO')
        self.VistA.wait('DAY:')
        self.VistA.write('^NEW IDCU INTERFACE')
        self.VistA.wait('INTERFACE:')
        self.VistA.write('0')
        self.VistA.wait('Difference:')
        self.VistA.write('')
        self.VistA.wait('DIVISION:')
        self.VistA.write('YES')
        self.VistA.wait('GROUP:')
        self.VistA.write('^')
        self.VistA.wait('Select DVB PARAMETERS ONE:')
        self.VistA.write('')
        self.VistA.wait('OPTION:')
        self.VistA.write('')
        # ADD ENTRY TO MAS PARAMETER
        self.VistA.wait(self.VistA.prompt)
        self.VistA.write('D ^XUP')
        self.VistA.write('1')
        self.VistA.wait('Select OPTION NAME')
        self.VistA.write('ADT SYSTEM')
        self.VistA.wait('Select ADT System Definition Menu Option')
        self.VistA.write('MAS Parameter Entry')
        self.VistA.wait('Enter 1-3 to EDIT, or RETURN to QUIT')
        self.VistA.write('1')
        self.VistA.wait('MEDICAL CENTER NAME')
        self.VistA.write('VISTA MEDICAL CENTER')
        self.VistA.wait('AFFILIATED')
        self.VistA.write('NO')
        self.VistA.wait('MULTIDIVISION MED CENTER')
        self.VistA.write('NO')
        self.VistA.wait('NURSING HOME WARDS')
        self.VistA.write('')
        self.VistA.wait('DOMICILIARY WARDS')
        self.VistA.write('')
        self.VistA.wait('SYSTEM TIMEOUT')
        self.VistA.write('30')
        self.VistA.wait('AUTOMATIC PTF MESSAGES')
        self.VistA.write('')
        self.VistA.wait('PRINT PTF MESSAGES')
        self.VistA.write('')
        self.VistA.wait('DEFAULT PTF MESSAGE PRINTER')
        self.VistA.write('')
        self.VistA.wait('SHOW STATUS SCREEN')
        self.VistA.write('YES')
        self.VistA.wait('USE HIGH INTENSITY ON SCREENS')
        self.VistA.write('^^')
        self.VistA.wait('Enter 1-3 to EDIT, or RETURN to QUIT')
        self.VistA.write('2')
        self.VistA.wait('DAYS TO UPDATE MEDICAID')
        self.VistA.write('365')
        self.VistA.wait('DAYS TO MAINTAIN G&L CORR')
        self.VistA.write('30')
        self.VistA.wait('TIME FOR LATE DISPOSITION')
        self.VistA.write('30')
        self.VistA.wait('SUPPLEMENTAL 10/10')
        self.VistA.write('0')
        self.VistA.wait(':')
        self.VistA.write('^ASK DEVICE IN REGISTRATION')
        self.VistA.wait('ASK DEVICE IN REGISTRATION')
        self.VistA.write('YES')
        self.VistA.wait('DAYS TO MAINTAIN SENSITIVITY')
        self.VistA.write('30')
        self.VistA.wait(':')
        self.VistA.write('^^')
        self.VistA.wait('Enter 1-3 to EDIT, or RETURN to QUIT')
        self.VistA.write('3')
        self.VistA.wait(':')
        self.VistA.write('^INSTITUTION FILE POINTER')
        self.VistA.wait('INSTITUTION FILE POINTER')
        self.VistA.write('VISTA HEALTH CARE')
        self.VistA.wait(':')
        self.VistA.write('^^')
        self.VistA.wait('Enter 1-3 to EDIT, or RETURN to QUIT')
        self.VistA.write('')
        self.VistA.wait('Select ADT System Definition Menu Option')
        self.VistA.write('')
        self.VistA.wait('YES//')
        self.VistA.write('')
        self.VistA.wait(self.VistA.prompt)
        self.VistA.write('')

    def admit_a_patient(self, ssn, bed):
        self.VistA.wait('Option:')
        self.VistA.write('Bed Control Menu')
        self.VistA.wait('Option:')
        self.VistA.write('admit a patient')
        self.VistA.wait('PATIENT:')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('C')
        self.VistA.wait('NOW//')
        self.VistA.write('NOW')
        self.VistA.wait('AS A NEW ADMISSION DATE')
        self.VistA.write('YES')
        self.VistA.wait('EXCLUDED FROM THE FACILITY DIRECTORY')
        self.VistA.write('NO')
        self.VistA.wait('ADMITTING REGULATION:')
        self.VistA.write('OBSERVATION')
        rval = self.VistA.multiwait(['CONDITION', 'ADMISSION'])
        if rval == 0:
            self.VistA.write('NO')
            self.VistA.wait('ADMISSION:')
            self.VistA.write('DIRECT')
        elif rval == 1:
            self.VistA.write('DIRECT')
        self.VistA.wait('[SHORT]:')
        self.VistA.write('TESTCONDITION')
        self.VistA.wait('LOCATION:')
        self.VistA.write('TESTWARD1')
        self.VistA.wait('ROOM-BED:')
        self.VistA.write(bed)
        self.VistA.wait('SPECIALTY:')
        self.VistA.write('MEDICAL OBSERVATION')
        self.VistA.wait('PHYSICIAN:')
        self.VistA.write('Alexander')
        self.VistA.wait('PHYSICIAN:')
        self.VistA.write('Smith')
        self.VistA.wait('Edit')
        self.VistA.write('No')
        self.VistA.wait('ADMISSION:')
        self.VistA.write('VA MEDICAL CENTER')
        self.VistA.wait('CONDITION: SERIOUSLY ILL//')
        self.VistA.write('')
        self.VistA.wait('PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option:')
        self.VistA.write('')

    def roster_list(self, vlist):
        self.VistA.wait('Option:')
        self.VistA.write('ADT Outputs Menu')
        self.VistA.wait('Option:')
        self.VistA.write('inpatient/lodger report menu')
        self.VistA.wait('Option:')
        self.VistA.write('inpatient listing')
        self.VistA.wait('SORT BY')
        self.VistA.write('ward')
        self.VistA.wait('START WITH WARD LOCATION')
        self.VistA.write('TESTWARD1')
        self.VistA.wait('GO TO WARD LOCATION')
        self.VistA.write('LAST')
        self.VistA.wait('PRINT WITH WARD BREAKOUT')
        self.VistA.write('NO')
        # self.VistA.wait('PRINT WITH DRG BREAKOUT')
        # self.VistA.write('YES')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('80')
        for vitem in vlist:
            self.VistA.wait(vitem)
        self.VistA.wait('Continue')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')

    def discharge_patient(self, ssn, dtime):
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('discharge a patient')
        self.VistA.wait('PATIENT:')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('C')
        self.VistA.wait('DISCHARGE DATE')
        self.VistA.write(dtime)
        self.VistA.wait('TYPE OF DISCHARGE:')
        self.VistA.write('regular')
        self.VistA.wait('Primary Care')
        self.VistA.write('NO')
        self.VistA.wait('PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')

    def scheduled_admit_list(self, vlist):
        self.VistA.wait('Option:')
        self.VistA.write('adt outputs menu')
        self.VistA.wait('Option:')
        self.VistA.write('scheduled admissions list')
        self.VistA.wait('//')
        self.VistA.write('T+1')
        self.VistA.wait('//')
        self.VistA.write('T+5')
        self.VistA.wait('BOTH//')
        self.VistA.write('BOTH')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('80')
        for vitem in vlist:
                self.VistA.wait(vitem)
        self.VistA.wait('Option:')
        self.VistA.write('')


    def transfer_patient(self, ssn):
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('transfer a patient')
        self.VistA.wait('PATIENT:')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('C')
        self.VistA.wait('TRANSFER DATE')
        self.VistA.write('now')
        self.VistA.wait('TRANSFER DATE')
        self.VistA.write('yes')
        self.VistA.wait('TRANSFER:')
        self.VistA.write('TO AUTHORIZED ABSENCE')
        self.VistA.wait('CHOOSE 1-2:')
        self.VistA.write('1')
        self.VistA.wait('RETURN DATE:')
        self.VistA.write('T+5')
        self.VistA.wait('CONDITION')
        self.VistA.write('')
        self.VistA.wait('PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')

    def schedule_admission(self, ssn):
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option')
        self.VistA.write('schedule an admission')
        self.VistA.wait('patient:')
        self.VistA.write(ssn)
        self.VistA.wait('SCHEDULED ADMISSION')
        self.VistA.write('yes')
        self.VistA.wait('DATE/TIME:')
        self.VistA.write('T+1@10am')
        self.VistA.wait('//')
        self.VistA.write('')
        self.VistA.wait('SPECIALTY:')
        self.VistA.write('ward')
        self.VistA.wait('WARD:')
        self.VistA.write('testward1')
        self.VistA.wait('DIVISION')
        self.VistA.write('')
        self.VistA.wait('EXPECTED:')
        self.VistA.write('5')
        self.VistA.wait('DIAGNOSIS:')
        self.VistA.write('medical observation')
        self.VistA.wait('PROVIDER:')
        self.VistA.write('alexander')
        self.VistA.wait('SURGERY:')
        self.VistA.write('NO')
        self.VistA.wait('STATUS:')
        self.VistA.write('')
        self.VistA.wait('patient:')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')

    def cancel_scheduled_admission(self, ssn):
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('cancel a scheduled admission')
        self.VistA.wait('patient:')
        self.VistA.write(ssn)
        self.VistA.wait('Yes//')
        self.VistA.write('yes')
        self.VistA.wait('CANCELLED:')
        self.VistA.write('NOW')
        self.VistA.wait('CANCELLED:')
        self.VistA.write('NO available BEDS')
        self.VistA.wait('NOTIFIED:')
        self.VistA.write('YES')
        self.VistA.wait('patient:')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('')

    def checkin_lodger(self, ssn, bed):
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Check-in Lodger')
        self.VistA.wait('Check-in PATIENT')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('')
        self.VistA.wait('Select LODGER CHECK-IN DATE')
        self.VistA.write('now')
        self.VistA.wait('CHECK-IN DATE')
        self.VistA.write('yes')
        self.VistA.wait('CHECK-IN TYPE')
        self.VistA.write('43')
        self.VistA.wait('WARD LOCATION')
        self.VistA.write('TESTWARD1')
        self.VistA.wait('ROOM-BED')
        self.VistA.write(bed)
        self.VistA.wait('REASON FOR LODGING')
        self.VistA.write('early')
        self.VistA.wait('LODGING COMMENTS')
        self.VistA.write('testing 1...2...3')
        self.VistA.wait('Check-in PATIENT')
        self.VistA.write(ssn)
        self.VistA.wait(bed)  # verify bed
        self.VistA.wait('CONTINUE//')
        self.VistA.write('Quit')
        self.VistA.wait('Check-in PATIENT')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('Admit a Patient')
        self.VistA.wait('PATIENT')
        self.VistA.write(ssn)
        self.VistA.wait('Patient is a lodger...you can not add an admission')  # verify lodger can't be admitted
        self.VistA.wait('Press RETURN to continue')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')

    def lodger_checkout(self, ssn):
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Lodger Check-out')
        self.VistA.wait('Check-out PATIENT')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('')
        self.VistA.wait('CHECK-OUT LODGER DATE')
        self.VistA.write('now+10')
        self.VistA.wait('DISPOSITION')
        self.VistA.write('DISMISSED')
        self.VistA.wait('Check-out PATIENT')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')

    def waiting_list_entry(self, ssn):
        ''' waiting list entry, via XUP  '''
        self.VistA.wait('Select OPTION NAME')
        self.VistA.write('ADT MANAGER MENU')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Waiting List Entry')
        self.VistA.wait('Select WAIT LIST DIVISION')
        self.VistA.write('VISTA MEDICAL CENTER')
        rval = self.VistA.multiwait(['as a new WAIT LIST', '...OK'])
        if rval == 0:
            self.VistA.write('Yes')
        elif rval == 1:
            self.VistA.write('yes')
        else:
            self.VistA.wait('SPECIALERROR')
        self.VistA.wait('Select PATIENT')
        self.VistA.write(ssn)
        self.VistA.wait('TIME OF APPLICATION')
        self.VistA.write('now')
        self.VistA.wait('TIME OF APPLICATION')
        self.VistA.write('now')
        self.VistA.wait('NHCU APPLICATION')
        self.VistA.write('hospital')
        self.VistA.wait('CATEGORY OF NEED')
        self.VistA.write('GENERAL')
        self.VistA.wait('BEDSECTION APPLYING TO')
        self.VistA.write('MEDICINE')
        self.VistA.wait('TREATING SPECIALTY')
        self.VistA.write('MEDICAL OBSERVATION')
        self.VistA.wait('IN ANOTHER HOSPITAL')
        self.VistA.write('NO')
        self.VistA.wait('ACTION')
        self.VistA.write('PENDING')
        self.VistA.wait('PRIORITY GROUPING')
        self.VistA.write('11')
        self.VistA.wait('COMMENTS')
        self.VistA.write('testing 1.2.3\r')
        self.VistA.wait('EDIT Option')
        self.VistA.write('')
        self.VistA.wait('Select PATIENT')
        self.VistA.write('')
        self.VistA.wait('Select WAIT LIST DIVISION')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')
        self.VistA.wait('Option')
        self.VistA.write('\r')


    def waiting_list_output(self, vlist):
        ''' show wait list, via XUP '''
        self.VistA.wait('Select OPTION NAME')
        self.VistA.write('ADT MANAGER MENU')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('adt outputs menu')
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('Waiting List Output')
        self.VistA.wait('DEVICE')
        self.VistA.write('')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('80')
        for vitem in vlist:
            self.VistA.wait(vitem)
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('')
        self.VistA.wait('Option')
        self.VistA.write('\r')


    def delete_waiting_list_entry(self, ssn):
        ''' delete wait list entry, via XUP  '''
        self.VistA.wait('Select OPTION NAME')
        self.VistA.write('ADT MANAGER MENU')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Delete Waiting List Entry')
        self.VistA.wait('Delete WAITING LIST entry from which DIVISION')
        self.VistA.write('VISTA MEDICAL CENTER')
        self.VistA.wait('Delete WAITING LIST entry for which patient')
        self.VistA.write(ssn)
        self.VistA.wait('OK to delete')
        self.VistA.write('yes')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')
        self.VistA.wait('Option')
        self.VistA.write('\r')

    def det_inpatient_inquiry(self, ssn, item, vlist):
        ''' Detailed Inpatient Inquiry Test'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Detailed Inpatient Inquiry')
        self.VistA.wait('Select PATIENT NAME:')
        self.VistA.write(ssn)
        self.VistA.wait('CHOOSE')
        self.VistA.write(item)
        for vitem in vlist:
            self.VistA.wait(vitem)
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')

    def drg_calc(self, ssn, diag, dnum, sdiag, sdnu, oper, onum):
        ''' DRG Calculation Test'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('DRG Calculation')
        self.VistA.wait('Effective Date:')
        self.VistA.write('t')
        self.VistA.wait('Choose Patient from PATIENT file')
        self.VistA.write('Yes')
        self.VistA.wait('Select PATIENT NAME:')
        self.VistA.write(ssn)
        self.VistA.wait('Transfer to an acute care facility')
        self.VistA.write('No')
        self.VistA.wait('Discharged against medical advice')
        self.VistA.write('No')
        self.VistA.wait('Enter PRINCIPAL diagnosis:')
        self.VistA.write(diag)
        self.VistA.wait('STOP or Select')
        self.VistA.write(dnum)
        self.VistA.wait('Enter SECONDARY diagnosis')
        self.VistA.write(sdiag)
        self.VistA.wait('STOP or Select')
        self.VistA.write(sdnum)
        self.VistA.wait('Enter SECONDARY diagnosis')
        self.VistA.write('')
        self.VistA.wait('Enter Operation/Procedure')
        self.VistA.write(oper)
        self.VistA.wait('CHOOSE')
        self.VistA.write(onum)
        self.VistA.wait('Enter Operation/Procedure')
        self.VistA.write('')
        self.VistA.wait('Effective Date')
        self.VistA.write('')
        self.VistA.wait('Choose Patient from PATIENT file')
        self.VistA.write('')
        self.VistA.wait('Select PATIENT NAME:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')

    def wwgeneric(self, dlist):
        ''' This is a generic method that receives a list of write and expect values'''
        ''' This handles lists of lists, so that a series of expect values can be checked before writing'''
        for wwset in dlist:
            for writeitem in wwset[0]:
                self.VistA.wait(writeitem)
            for expectitem in wwset[1]:
                self.VistA.write(expectitem)

    def provider_change(self, ssn):
        ''' Provider Change Test in Bed Control'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Provider Change')
        self.VistA.wait('Provider Change for PATIENT:')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('')
        self.VistA.wait('Select PROVIDER CHANGE DATE')
        self.VistA.write('')
        self.VistA.wait('AS A NEW PROVIDER CHANGE DATE')
        self.VistA.write('yes')
        self.VistA.wait('PRIMARY PHYSICIAN:')
        self.VistA.write('smith')
        self.VistA.wait('ATTENDING PHYSICIAN')
        self.VistA.write('alexander')
        self.VistA.wait('Edit')
        self.VistA.write('no')
        self.VistA.wait('Provider Change for PATIENT')
        self.VistA.write(ssn)
        self.VistA.wait('Provider')
        self.VistA.wait('SMITH,MARY')
        self.VistA.wait('Attending')
        self.VistA.wait('ALEXANDER,ROBERT')
        self.VistA.wait('CONTINUE')
        self.VistA.write('Q')
        self.VistA.wait('Provider Change for PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option')
        self.VistA.write('')

    def seriously_ill_list(self, ssnlist, vlist1, vlist2):
        ''' Detailed Inpatient Inquiry Test in Bed Control'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Seriously Ill List Entry')
        self.VistA.wait('Select PATIENT NAME:')
        self.VistA.write('??')
        for vitem in vlist1:
            self.VistA.wait(vitem)
        for i, ssnitem in enumerate(ssnlist):
            self.VistA.wait('Select PATIENT NAME:')
            self.VistA.write(ssnitem)
            for vitem in vlist2[i]:
                self.VistA.wait(vitem)
            self.VistA.wait('//')
            self.VistA.write('')
            self.VistA.wait('//')
            self.VistA.write('')
        self.VistA.wait('Select PATIENT NAME:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option:')
        self.VistA.write('')

    def switch_bed(self, ssn, bed, badbed=None):
        ''' Switch Bed Test in Bed Control'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Switch Bed')
        self.VistA.wait('SWITCH BED FOR PATIENT:')
        self.VistA.write(ssn)
        if badbed is not None:
            self.VistA.wait('ROOM-BED:')
            self.VistA.write(badbed)
            self.VistA.wait('ROOM-BED:')
            self.VistA.write(bed)
        else:
            self.VistA.wait('ROOM-BED:')
            self.VistA.write(bed)
        self.VistA.wait('SWITCH BED FOR PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option:')
        self.VistA.write('')

    def extended_bed_ctrl(self, ssn, action, bed, badbed=None):
        ''' Extended Bed Control Test in Bed Control'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Switch Bed')
        self.VistA.wait('SWITCH BED FOR PATIENT:')
        self.VistA.write(ssn)
        if badbed is not None:
            self.VistA.wait('ROOM-BED:')
            self.VistA.write(badbed)
            self.VistA.wait('ROOM-BED:')
            self.VistA.write(bed)
        else:
            self.VistA.wait('ROOM-BED:')
            self.VistA.write(bed)
        self.VistA.wait('SWITCH BED FOR PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option:')
        self.VistA.write('')

    def treating_spcl_trans(self, ssn, spcl):
        ''' Treadting Specialty Transfer Test in Bed Control'''
        self.VistA.wait('Option:')
        self.VistA.write('bed control menu')
        self.VistA.wait('Option:')
        self.VistA.write('Treating Specialty Transfer')
        self.VistA.wait('Specialty Change for PATIENT:')
        self.VistA.write(ssn)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('')
        self.VistA.wait('Select SPECIALTY TRANSFER DATE:')
        self.VistA.write('Now')
        self.VistA.wait('AS A NEW SPECIALTY TRANSFER DATE')
        self.VistA.write('Yes')
        self.VistA.wait('FACILITY TREATING SPECIALTY:')
        self.VistA.write(spcl)
        self.VistA.wait('PRIMARY PHYSICIAN:')
        self.VistA.write('Alexander')
        self.VistA.wait('ATTENDING PHYSICIAN:')
        self.VistA.write('Smith')
        self.VistA.wait('NO//')
        self.VistA.write('No')
        self.VistA.wait('Specialty Change for PATIENT:')
        self.VistA.write(ssn)
        self.VistA.wait(spcl)
        self.VistA.wait('CONTINUE//')
        self.VistA.write('Quit')
        self.VistA.wait('Specialty Change for PATIENT:')
        self.VistA.write('')
        self.VistA.wait('Select Bed Control Menu Option:')
        self.VistA.write('')

    def adt_menu_smoke(self, ssn):
        # Veteran ID Card
        self.VistA.wait('Option:')
        self.VistA.write('veteran id card menu')
        self.VistA.wait('Select Veteran ID Card Menu Option')
        self.VistA.write('single patient download request')
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write(ssn)
        self.VistA.wait('Do you still wish to download data')
        self.VistA.write('yes')
        self.VistA.wait('Data Download successfully to VIC')
        #
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write('')
        self.VistA.wait('Select Veteran ID Card Menu Option')
        self.VistA.write('Problem List Mgt Menu')
        self.VistA.wait('Select Problem List Mgt Menu Option')
        self.VistA.write('Patient Problem List')
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write(ssn)
        self.VistA.wait('No data available meeting criteria.')
        self.VistA.wait('Select Action')
        self.VistA.write('Quit')
        self.VistA.wait('Select Problem List Mgt Menu Option')
        self.VistA.write('')
        self.VistA.wait('Select Veteran ID Card Menu Option')
        self.VistA.write('')
        # ADT Outputs
        self.VistA.wait('Select ADT Manager Menu Option')
        self.VistA.write('ADT Outputs Menu')
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('10-10')
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write(ssn)
        self.VistA.wait('PRINT 10-10EZ')
        self.VistA.write('yes')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('80')
        self.VistA.wait('VA FORM 10-10EZ')
        self.VistA.wait('PAGE 4')
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write('')
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('ADT Third Party Output Menu')
        self.VistA.wait('Select ADT Third Party Output Menu Option')
        self.VistA.write('Patient Review Document')
        self.VistA.wait('Select PATIENT NAME')
        self.VistA.write(ssn)
        self.VistA.wait('No scheduled admissions on file')
        self.VistA.wait('Select ADT Third Party Output Menu Option')
        self.VistA.write('Review Document')
        self.VistA.wait('START WITH DATE')
        self.VistA.write('')
        self.VistA.wait('DEVICE')
        self.VistA.write('')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('80')
        self.VistA.wait('NO RECORDS TO PRINT')
        self.VistA.wait('Select ADT Third Party Output Menu Option')
        self.VistA.write('Veteran Patient Insurance Information')
        self.VistA.wait('Sort by Discharge or Admission')
        self.VistA.write('')
        self.VistA.wait('START DATE')
        self.VistA.write('t')
        self.VistA.wait('END DATE')
        self.VistA.write('t+10')
        self.VistA.wait('DEVICE')
        self.VistA.write('')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        self.VistA.wait('Select ADT Third Party Output Menu Option')
        self.VistA.write('')
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('')
        # show bed availability
        self.VistA.wait('Select ADT Manager Menu Option')
        self.VistA.write('ADT Outputs')
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('Bed Availability')
        self.VistA.wait('Availability Listing')
        self.VistA.write('A')
        self.VistA.wait('Select WARD LOCATION NAME:')
        self.VistA.write('TESTWARD1')
        self.VistA.wait('display room-bed descriptions')
        self.VistA.write('yes')
        for vitem in ['TESTWARD1', '1-A', '(bed1)', '1-B', '(bed2)', '2-A', '(bed3)', '2-B', '(bed4)']:
            self.VistA.wait(vitem)
        self.VistA.wait('Select WARD LOCATION NAME:')
        self.VistA.write('')
        # Dispositions
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('Disposition Outputs Menu')
        self.VistA.wait('Select Disposition Outputs Menu Option')
        self.VistA.write('Log of Dispositions')
        self.VistA.wait('I//')
        self.VistA.write('ALL')
        self.VistA.wait('START WITH LOG IN DATE/TIME: FIRST//')
        self.VistA.write('')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        self.VistA.wait('CARTER,DAVID JR')
        self.VistA.wait('Select Disposition Outputs Menu Option')
        self.VistA.write('Disposition')
        self.VistA.wait('EARLIEST REGISTRATION ON FILE IS')
        self.VistA.wait('Start with REGISTRATION DATE:')
        self.VistA.write('')
        self.VistA.wait('Select Disposition Outputs Menu Option')
        self.VistA.write('Summary')
        self.VistA.wait('START DATE:')
        self.VistA.write('t-100')
        self.VistA.wait('END DATE')
        self.VistA.write('t')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        for vitem in ['REGISTRATION DISPOSITION SUMMARY', 'ADMIT', 'SCHEDULED ADMISSION', 'SCHEDULE FUTURE APPOINTMENT', 'INELIGIBLE']:
            self.VistA.wait(vitem)
        self.VistA.write('')
        for vitem in ['REGISTRATION DISPOSITION SUMMARY', 'DEAD ON ARRIVAL', 'FEE BASIS REFERAL', 'COMMUNITY RESOURCES', 'LOW PRIORITY-DISP COMMUNITY']:
            self.VistA.wait(vitem)
        self.VistA.write('')
        for vitem in ['REGISTRATION DISPOSITION SUMMARY', 'LOW PRIORITY-DISP OTHER VA', 'HOSPITAL ADMISSION', 'CANCEL WITHOUT EXAM']:
            self.VistA.wait(vitem)
        self.VistA.write('')
        for vitem in ['REGISTRATION DISPOSITION SUMMARY', 'TOTAL']:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Disposition Outputs Menu Option')
        self.VistA.write('')
        # Enrollment Reports
        self.VistA.wait('Select ADT Outputs Menu Option')
        self.VistA.write('Enrollment')
        self.VistA.wait('Select Enrollment Reports Option:')
        self.VistA.write('Enrolled Veterans')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        for vitem in ['Enrolled Veterans Report', 'CURRENTLY ENROLLED', 'In Process', 'Total', 'Total']:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Enrollment Reports Option:')
        self.VistA.write('Pending Applications')
        self.VistA.wait('Enter Beginning Date:')
        self.VistA.write('t-100')
        self.VistA.wait('Enter Ending Date')
        self.VistA.write('')
        self.VistA.wait('Do you want the report for ALL facilities')
        self.VistA.write('YES')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        for vitem in ['Pending Applications', 'AppDt', 'Name', 'PatientID', 'DOB']:
            self.VistA.wait(vitem)
        self.VistA.wait('Enter RETURN to continue or')
        self.VistA.write('')
        self.VistA.wait('Select Enrollment Reports Option:')
        self.VistA.write('Enrollees by Status')
        self.VistA.wait('Preferred Facilities')
        self.VistA.write('YES')
        self.VistA.wait('selected patients')
        self.VistA.write('no')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        for vitem in ['Enrollments by Status', 'SUMMARY STATISTICS', 'Run Date', 'TOTAL FOR ALL SELECTED FACILITIES']:
            self.VistA.wait(vitem)
        self.VistA.wait('Enter RETURN to continue or')
        self.VistA.write('')
        self.VistA.wait('Select Enrollment Reports Option:')
        self.VistA.write('Upcoming')
        self.VistA.wait('Enter beginning date')
        self.VistA.write('')
        self.VistA.wait('Enter ending date')
        self.VistA.write('')
        self.VistA.wait('in the report')
        self.VistA.write('ALL')
        self.VistA.wait('first be listed')
        self.VistA.write('NO')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        for vitem in ['Appointments for Veterans with no Enrollment Application', 'Run Date', 'Name', 'PatientID', 'DOB', 'Appt Dt', 'Enroll Cat']:
            self.VistA.wait(vitem)
        self.VistA.wait('Enter RETURN to continue or')
        self.VistA.write('')
        self.VistA.wait('Select Enrollment Reports Option:')
        self.VistA.write('EGT')
        self.VistA.wait('Select Actual or Preliminary')
        self.VistA.write('A')
        self.VistA.wait('Select Detail or Summary')
        self.VistA.write('Summary')
        self.VistA.wait('Report Begin Date')
        self.VistA.write('t-100')
        self.VistA.wait('Report End Date')
        self.VistA.write('t+100')
        self.VistA.wait('DEVICE')
        self.VistA.write('HOME')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        for vitem in ['EGT Actual Summary Impact Report', 'Date Range', 'EGT Setting', 'Date/Time', 'IMPORTANT NOTE', 'ENROLLMENT PRIORITY', 'TOTAL PATIENTS']:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Enrollment Reports Option:')
        self.VistA.write('Non-Treating')
        self.VistA.wait('NON TREATING PREFERRED FACILITY CLEAN UP REPORT')
        self.VistA.wait('Do you want to continue')
        self.VistA.write('Yes')
        self.VistA.wait('Requested Start Time')
        self.VistA.write('')
        self.VistA.wait('TaskMan Task')
        self.VistA.wait('Select Enrollment Reports Option')
        self.VistA.write('')
        self.VistA.wait('Option')
        self.VistA.write('')
