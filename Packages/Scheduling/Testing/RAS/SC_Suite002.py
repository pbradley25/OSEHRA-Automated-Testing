'''
Created on Mar 27, 2013

@author: afequiere
'''
import sys
sys.path = ['./Functional/RAS/lib'] + ['./dataFiles'] + ['./Python/vista'] + sys.path
from CompSCActions import CompSCActions
import TestHelper
import datetime
import logging

def comp_sc_test001(resultlog, result_dir, namespace):
    '''Objective: Use Case 1 - Configure and update scheduling component structure, file, and tables.'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        #time = SC.schtime()
        SC.signon(isFileman=True)
        SC.createCompSchedInsitutions()
        SC.signon(isFileman=True)
        SC.preAppointmentTemplateSetup()        
        SC.signon(isFileman=True)
        SC.appointmentTypeSetup()        
        SC.signon(optionType='Services')
        SC.standardServicesSetup()
        SC.signon(optionType='Holiday')
        SC.holidaySetup(holidayList=[{'name': 'National VA Organization Day','date': 'Jul 20 2012'},
                                     {'name': 'National VA Organization Day','date': 'Jul 22 2013'},
                                     {'name': 'National VA Organization Day','date': 'Jul 21 2014'},
                                     {'name': 'Valentines Day','date': 'Feb 13 2012'},
                                     {'name': 'Valentines Day','date': 'Feb 14 2013'},
                                     {'name': 'Valentines Day','date': 'Feb 14 2014'}])
        SC.signon(optionType='Clinic Setup')
        SC.clinicSetup(clinicList=[{'name': 'CALIFORNIA VA REGIONAL MED CTR','abr': 'CAVARMC','provider1': 'Alexander','provider2': 'Smith'},
                                   {'name': 'CALIFORNIA VA OUTPAT CLIN','abr': 'CAVAOPC','provider1': 'Smith','provider2': 'Alexander'},                                     
                                   {'name': 'TEMP CLINIC','abr': 'TC','provider1': 'Alexander','provider2': 'Smith'}])
        SC.signon(isFileman=True)
        SC.modifyClinicInst(clinicList=[{'name': 'CALIFORNIA VA REGIONAL MED CTR','facilityId': '7100'},
                                        {'name': 'CALIFORNIA VA OUTPAT CLIN','facilityId': '7102'}])                                    
        SC.signon(optionType='Supervisor')
        SC.deactivateClinic(clinic='TEMP CLINIC')
        SC.signon(optionType='Supervisor') 
        SC.reactivateClinic(clinic='TEMP CLINIC')                          
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def comp_sc_test002(resultlog, result_dir, namespace):
    '''Objective: Use Case 2 - Configure resources for a section (i.e., providers, rooms, equipment).
       Create schedules for resources in a section.  Hold a schedule that was created then release it manually and automatically. 
       Block a date/time range of schedules. Block a date/time range of schedule with existing appointments. '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        #time = SC.schtime()
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA REGIONAL MED CTR', appointments=[{'patient': 'ONE','datetime': 't+1@1200','mins': '30','note': 'Initial','fresh': None}, #+ SC.schtime('30m'),'mins': '30','note': 'Initial','fresh': None},
                                                                                {'patient': 'ONE','datetime': 't+1@1300', 'mins': '15','note': 'Follow-Up','fresh': 'True'}])#+SC.schtime('1h'),'mins': '15','note': 'Follow-Up','fresh': 'True'}])
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA OUTPAT CLIN', appointments=[{'patient': 'TWO','datetime': 't+1@1200', 'mins': '30','note': 'C&P','fresh': None}, #+SC.schtime('30m'),'mins': '30','note': 'C&P','fresh': None},
                                                                           {'patient': 'TWO','datetime': 't+1@1300' ,'mins': '15','note': 'Regular','fresh': 'True'}]) #+SC.schtime('1h'),'mins': '15','note': 'Regular','fresh': 'True'}])
        SC.signon()
        SC.copyMultiAppDateRange(clinic= 'CALIFORNIA VA REGIONAL MED CTR', appointment={'patient': 'ONE','datetime': '@0800','mins': '30','note': 'Schedule','fresh': None, 'nextAvailable': 'No'}, strDate='12/04/2013',endDate='01/15/2014')
        SC.signon(optionType='Supervisor')
        SC.blockApp(clinic='CALIFORNIA VA REGIONAL MED CTR',date='Jan 5 2014',note='block single appt')
        SC.signon(optionType='Supervisor')
        SC.restoreApp(clinic='CALIFORNIA VA REGIONAL MED CTR',date='Jan 5 2014') 
        SC.signon(optionType='Supervisor')
        SC.blockApp(clinic='CALIFORNIA VA REGIONAL MED CTR',date='Dec 5 2013',note='block half day',strTime='0900',endTime='1200')                                                                 
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA REGIONAL MED CTR', appointments=[{'patient': 'ONE','datetime': 't+1@1000','mins': '15','note': 'Medicine refills','fresh': None},
                                                                                {'patient': 'ONE','datetime': 't+1@1545','mins': '15','note': 'New appointment','fresh': 'True'}])
        '''SC.signon(optionType='Supervisor')
        SC.blockApp(clinic='CALIFORNIA VA REGIONAL MED CTR',date='Jan 14 2014',note='block multi days')
        SC.blockApp(clinic='CALIFORNIA VA REGIONAL MED CTR',date='Jan 15 2014',note='block multi days')'''
        SC.signon()
        SC.listAllAppointmentByDate(clinic='CALIFORNIA VA REGIONAL MED CTR',strDate='t',endDate='t+365')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def comp_sc_test003(resultlog, result_dir, namespace):
    '''Objective: Use Case 3 - Create an appointment. Once the appointment has been scheduled, the scheduler 
       provides the scheduled appointment information to the patient. Additional actions to be 
       demonstrated are detailed in the use case steps. Written appointment notifications need to be 
       provided to the patient either through the mail or by using e-mail and the method that was used to 
       notify the patient of their appointment is captured in the scheduling component.'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        #time = SC.schtime()
        SC.signon(optionType='Register a Patient')
        SC.patientRegistration(patient={'name':'Ryan, Mark A','sex':'M','dob':'09021987','ssn':'777888999','type':'NSC Veteran','veteran':'Y','service':'Y','isTwin':'N','maiden':'Brown','cityOB':'Manhattan','stateOB':'NY'})
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA OUTPAT CLIN', appointments=[{'patient': 'Ryan, Mark A','datetime': 'Jul 8 2013@0800','mins': '15','note': 'desired appointment'},
                                                                           {'patient': 'Ryan, Mark A','datetime': 'Jul 22 2013@0800','mins': '15','note': 'agreed upon date'}])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def comp_sc_test004(resultlog, result_dir, namespace):
    '''Objective: Use Case 4 - Check in a patient for an appointment and disposition a patient from an appointment.'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        #time = SC.schtime()
        SC.signon()
        SC.viewPatientDemographic(patient='Ryan, Mark A')
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA REGIONAL MED CTR', appointments=[{'patient': 'Ryan, Mark A','datetime': 'NOW','mins': '15','note': 'multi appt'}])       
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA OUTPAT CLIN', appointments=[{'patient': 'Ryan, Mark A','datetime': 't+1@1130','mins': '15','note': 'multi appt'}]) 
        SC.signon()
        SC.checkin(clinic='CALIFORNIA VA REGIONAL MED CTR', vlist=['CHECKED-IN:'],strDate='t',endDate='t') #SC.schtime('30m'), 'CHECKED-IN:'])
        SC.signon()
        SC.listAllAppointmentByDate(clinic='CALIFORNIA VA OUTPAT CLIN',strDate='t',endDate='t+1')
        SC.signon()
        SC.patientCheckout(clinic='CALIFORNIA VA REGIONAL MED CTR',strDate='t',endDate='t',provider='Alexander',diagnosis='305.91')
        '''SC.checkout(clinic='CALIFORNIA VA REGIONAL MED CTR', vlist1=['Ryan, Mark A', 'now', 'Checked In'],#SC.schtime('30m'), 'Checked In'],
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91',strDate='t',endDate='t')'''
        SC.signon()
        SC.listAllAppointmentByPatient(patient='Ryan, Mark A')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')       
        
def comp_sc_test005(resultlog, result_dir, namespace):
    '''Objective: Use Case 5 - Manage a patient that requires an unscheduled appointment (walk-in).'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        #time = SC.schtime()
        SC.signon()
        SC.viewPatientDemographic(patient='TEN')
        SC.signon()
        SC.unschPatientVisit(clinic='CALIFORNIA VA OUTPAT CLIN', patient='TEN')
        #SC.unschvisit(clinic='CALIFORNIA VA OUTPAT CLIN', patient='777888999', patientname='Ryan, Mark A')
        SC.signon()
        SC.listAllAppointmentByDate(clinic='CALIFORNIA VA OUTPAT CLIN',strDate='t',endDate='t+1')
        SC.signon()
        SC.patientCheckout(clinic='CALIFORNIA VA OUTPAT CLIN',strDate='t',endDate='t',provider='Smith',diagnosis='305.91')
        '''SC.checkout(clinic='CALIFORNIA VA OUTPAT CLIN', vlist1=['Ryan, Mark A', SC.schtime('0m'), 'Checked In'],
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91')'''
        SC.signon()
        SC.listAllAppointmentByPatient(patient='TEN')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def comp_sc_test007(resultlog, result_dir, namespace):
    '''Objective: Use Case 7 - Reschedule appointment.'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        #time = SC.schtime()
        SC.signon()
        SC.makeMultiApp(clinic= 'CALIFORNIA VA OUTPAT CLIN', appointments=[{'patient': 'TEN','datetime': 't+2@0800','mins': '15','note': 'appt'}])
        SC.signon()
        SC.canapp(clinic='CALIFORNIA VA OUTPAT CLIN', rebook=True,strDate='t+2',endDate='t+2')
        SC.signon()
        SC.noshow(clinic='CALIFORNIA VA OUTPAT CLIN')
        SC.signon()
        SC.listNoShowByDate(clinic='CALIFORNIA VA REGIONAL MED CTR',strDate='t',endDate='t+3')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')
                                 
def sc_test001(resultlog, result_dir, namespace):
    '''Basic appointment managment options
    Make an Appointment, Check in, Check Out'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = CompSCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp(patient='333224444', clinic=tclinic, datetime=time)
        time = SC.schtime(plushour=1)
        now = datetime.datetime.now()
        hour = now.hour + 1
        SC.signon()
        SC.checkin(clinic=tclinic, vlist=['Three', str(hour), 'CHECKED-IN:'])
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['Three', str(hour), 'Checked In'],
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91')
        SC.signon()
        SC.makeapp_bypat(clinic=tclinic, patient='333224444', datetime=time, fresh='No', prevCO='yes')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')        

def sc_test002(resultlog, result_dir, namespace):
    '''Basic appointment managment options
    Make an Appointment (Scheduled and Unscheduled),
    record a No-Show, Cancel an appointment and change patients'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp(clinic=tclinic, patient='655447777', datetime=time)
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.unschvisit(clinic=tclinic, patient='345678233', patientname='Twelve')
        SC.signon()
        SC.noshow(clinic=tclinic, appnum='3')
        SC.signon()
        SC.canapp(clinic=tclinic, mult='1')
        SC.signon()
        SC.chgpatient(clinic=tclinic, patient1='345678233', patient2='345238901',
                      patientname1='Twelve', patientname2='Ten')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test003(resultlog, result_dir, namespace):
    '''This tests clinic features such as change clinic, change daterange,
     expand the entry, add and edit, and Patient demographics'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        SC.signon()
        tclinic = SC.getclinic()
        SC.chgclinic()
        SC.signon()
        SC.chgdaterange(clinic=tclinic)
        SC.signon()
        SC.teaminfo(clinic=tclinic)
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test004(resultlog, result_dir, namespace):
    '''This tests clinic features such as expand the entry, add and edit, and Patient demographics'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime(plushour=1)
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp(clinic=tclinic, patient='345238901', datetime=time)
        SC.signon()
        SC.patdem(clinic=tclinic, name='Ten', mult='2')
        SC.signon()
        SC.expandentry(clinic=tclinic, vlist1=['TEN', 'SCHEDULED', '30'],
                       vlist2=['Event', 'Date', 'User', 'TESTMASTER'],
                       vlist3=['NEXT AVAILABLE', 'NO', '0'], vlist4=['1933', 'MALE', 'UNANSWERED'],
                       vlist5=['Combat Veteran:', 'No check out information'], mult='3')
        SC.signon()
        SC.addedit(clinic=tclinic, name='354623902', icd='305.91')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test005(resultlog, result_dir, namespace):
    '''This test checks a patient into a clinic, then discharges him, then deletes his checkout'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA)
        SC.signon()
        tclinic = SC.getclinic()
        SC.enroll(clinic=tclinic, patient='543236666')
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.makeapp(clinic=tclinic, patient='543236666', datetime=time)
        SC.signon()
        SC.discharge(clinic=tclinic, patient='543236666', appnum='3')
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['One', 'No Action'],
                    vlist2=['305.91', 'RESULTING'], icd='305.91', mult='4')
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.deletecheckout(clinic=tclinic, appnum='3')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test006(resultlog, result_dir, namespace):
    '''This test will exercise the wait list functionality'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        tclinic = SC.getclinic()
        SC.waitlistentry(clinic=tclinic, patient='323123456')
        SC.waitlistdisposition(clinic=tclinic, patient='323123456')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')


def sc_test007(resultlog, result_dir, namespace):
    '''Basic Apptments, similar to sc_test001 but specifying patient name not clinic at first prompt
       This test will also use the space-bar to check recall feature works
        Make an Appointment, Check in, Check Out'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_bypat(clinic=tclinic, patient='656454321', datetime=time, loopnum=2)
        SC.signon()
        SC.use_sbar(clinic=tclinic, patient='656454321', fresh='No')
        time = SC.schtime(plushour=1)
        now = datetime.datetime.now()
        hour = now.hour + 1
        SC.signon()
        SC.checkin(clinic=tclinic, vlist=['Five', str(hour), 'CHECKED-IN:'], mult='5')
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['Five', str(hour), 'Checked In'],
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91', mult='5')
        SC.signon()
        SC.ver_actions(clinic=tclinic, patient='4444',
                       PRvlist=['THREE,PATIENT C', 'ALEXANDER,ROBERT'],
                       DXvlist=['305.91', 'OTHER DRUG', 'RESULTING'],
                       CPvlist=['THREE,PATIENT C'])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test008(resultlog, result_dir, namespace):
    '''Make future appointments and verify, and use CLINICX and check use of case sensitivity (cLiNiCx, ClInIcX, etc.)'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_bypat(clinic='cLiNiCx', patient='323678904', datetime='t+5@8PM')
        SC.signon()
        SC.verapp_bypat(patient='323678904', vlist=['THIRTEEN,PATIENT M', 'Clinicx', 'Future'])
        SC.signon()
        SC.makeapp_bypat(clinic='cLiNiCx', patient='222559876', datetime='t+6@8PM', CLfirst='Yes')
        SC.signon()
        SC.verapp_bypat(patient='222559876', vlist=['SIXTEEN,PATIENT P', 'Clinicx', 'Future'],
                        CInum=['1', '1'], COnum=['1', '2'])
        SC.signon()
        SC.verapp(clinic='cLiNiCx',
                  vlist=['Thirteen,Patient M', 'Future', 'Sixteen,Patient P', 'Future'],
                  CInum=['2', '1'], COnum=['2', '2'])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test009(resultlog, result_dir, namespace):
    '''Make appts with variable length. Make appt in distant future for EWL'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_var(clinic='CLInicA', patient='323678904', datetime='t+7@7AM', fresh='No')
        SC.signon()
        SC.verapp_bypat(patient='323678904', vlist=['THIRTEEN,PATIENT M', 'Clinica', '7:00', 'Future'],)
        SC.signon()
        SC.makeapp_var(clinic='CLInicA', patient='323678904', datetime='t+122@6AM', fresh='No')
        SC.signon()
        SC.makeapp_var(clinic='CLInicA', patient='323678904', datetime='t+10@4AM', fresh='No', nextaval='No')
        SC.signon()
        SC.verapp_bypat(patient='323678904', vlist=['THIRTEEN,PATIENT M', 'Clinica', '4:00', 'Future'],
                        ALvlist=['THIRTEEN,PATIENT M', 'Clinicx', 'Clinica', 'Clinica'],
                        EPvlist=['THIRTEEN,PATIENT M', 'CLINICX', '8904', 'FUTURE', 'SCHEDULED', 'REGULAR'])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test010(resultlog, result_dir, namespace):
    '''Make appts and save demographics'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        # this signon() and fix_demographics() is a workaround for gtm bug
        if VistA.type == 'GTM':
            SC.signon()
            SC.fix_demographics(clinic='CLInicA', patient='323123456',
                                dgrph=[['COUNTRY', ''],
                                     ['STREET ADDRESS', ''],
                                     ['ZIP', '20005'],
                                     ['CITY', 'WASHINGTON'],
                                     ['PHONE NUMBER', ''],
                                     ['PHONE NUMBER', ''],
                                     ['BAD ADDRESS INDICATOR', ''],
                                     ['save the above changes', 'yes']])
        #
        SC.signon()
        tclinic = SC.getclinic()
        SC.set_demographics(clinic='CLInicA', patient='323123456',
                        dgrph=[['COUNTRY', ''],
                                 ['STREET ADDRESS', '123 SMITH STREET'],
                                 ['STREET ADDRESS', ''],
                                 ['ZIP', '20005'],
                                 ['CITY', 'WASHINGTON'],
                                 ['PHONE NUMBER', '2021112222'],
                                 ['PHONE NUMBER', ''],
                                 ['BAD ADDRESS INDICATOR', ''],
                                 ['save the above changes', 'yes'],
                                 ['Press ENTER to continue', ''],
                                 ['SEX', 'MALE'] ,
                                 ['Select ETHNICITY', 'N'],
                                 ['Select RACE', 'Black'],
                                 ['new RACE INFORMATION', 'Yes'],
                                 ['RACE', ''],
                                 ['MARITAL STATUS', 'MARRIED'],
                                 ['RELIGIOUS PREFERENCE', 'CELTICISM'],
                                 ['TEMPORARY ADDRESS ACTIVE', 'NO'],
                                 ['PHONE NUMBER', ''],
                                 ['PAGER NUMBER', ''],
                                 ['EMAIL ADDRESS', '']])
        SC.signon()
        SC.get_demographics(patient='323123456',
                        vlist=[['COUNTRY: UNITED STATES', ''],
                                 ['123 SMITH STREET', ''],
                                 ['STREET ADDRESS', ''],
                                 ['20005', ''],
                                 ['CITY: WASHINGTON', ''],
                                 ['2021112222', ''],
                                 ['PHONE NUMBER', ''],
                                 ['BAD ADDRESS INDICATOR', ''],
                                 ['save the above changes', 'no'],
                                 ['Press ENTER to continue', ''],
                                 ['SEX: MALE', ''],
                                 ['Select ETHNICITY INFORMATION: NOT HISPANIC OR LATINO', ''],
                                 ['ETHNICITY: NOT HISPANIC OR LATINO', ''],
                                 ['Select RACE INFORMATION: BLACK OR AFRICAN AMERICAN', ''],
                                 ['RACE: BLACK OR AFRICAN AMERICAN', ''],
                                 ['Select RACE INFORMATION', ''],
                                 ['MARITAL STATUS', 'MARRIED'],
                                 ['RELIGIOUS PREFERENCE: CELTICISM', ''],
                                 ['ADDRESS ACTIVE', ''],
                                 ['PHONE NUMBER', ''],
                                 ['PAGER NUMBER', ''],
                                 ['EMAIL ADDRESS', '']])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def startmon(resultlog, result_dir, namespace):
    '''Starts Coverage Monitor'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir, namespace)
        VistA1.startCoverage(routines=['SC*', 'SD*'])
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def stopmon (resultlog, result_dir, humanreadable, namespace):
    ''' STOP MONITOR'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Connect to VistA
        VistA1 = connect_VistA(testname, result_dir, namespace)
        path = (result_dir + '/' + timeStamped('Scheduling_coverage.txt'))
        VistA1.stopCoverage(path, humanreadable)
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def connect_VistA(testname, result_dir, namespace):
    # Connect to VistA
    logging.debug('Connect_VistA' + ', Namespace: ' + namespace)
    from OSEHRAHelper import ConnectToMUMPS, PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + timeStamped(testname + '.txt'), instance='', namespace=namespace)
    if VistA.type == 'cache':
        try:
            VistA.ZN(namespace)
        except IndexError, no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
