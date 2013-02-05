'''
Created on Jun 14, 2012

@author: bcaine, pbradley
'''
import sys
sys.path = ['./FunctionalTest/RAS/lib'] + ['./dataFiles'] + ['./lib/vista'] + sys.path
from SCActions import SCActions
import TestHelper
import datetime
import logging

def sc_test001(resultlog, result_dir):
    '''Basic appointment managment options
    Make an Appointment, Check in, Check Out'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
        SC = SCActions(VistA, scheduling='Scheduling')
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
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test002(resultlog, result_dir):
    '''Basic appointment managment options
    Make an Appointment (Scheduled and Unscheduled),
    record a No-Show, Cancel an appointment and change patients'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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

def sc_test003(resultlog, result_dir):
    '''This tests clinic features such as change clinic, change daterange,
     expand the entry, add and edit, and Patient demographics'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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

def sc_test004(resultlog, result_dir):
    '''This tests clinic features such as expand the entry, add and edit, and Patient demographics'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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
                       vlist5=['Combat Veteran:', 'No check out information'], mult='2')
        SC.signon()
        SC.addedit(clinic=tclinic, name='354623902', icd='305.91')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test005(resultlog, result_dir):
    '''This test checks a patient into a clinic, then discharges him, then deletes his checkout'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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
                    vlist2=['305.91', 'RESULTING'], icd='305.91', mult='3')
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.deletecheckout(clinic=tclinic, appnum='3')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test006(resultlog, result_dir):
    '''This test will exercise the wait list functionality'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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


def sc_test007(resultlog, result_dir):
    '''Basic Apptments, similar to sc_test001 but specifying patient name not clinic at first prompt
       This test will also use the space-bar to check recall feature works
        Make an Appointment, Check in, Check Out'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_bypat(clinic=tclinic, patient='656454321', datetime=time)
        SC.signon()
        SC.use_sbar(clinic=tclinic, patient='656454321', fresh='No')
        time = SC.schtime(plushour=1)
        now = datetime.datetime.now()
        hour = now.hour + 1
        SC.signon()
        SC.checkin(clinic=tclinic, vlist=['Five', str(hour), 'CHECKED-IN:'],mult='4')
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['Five', str(hour), 'Checked In'], 
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91', mult='4')
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

def sc_test008(resultlog, result_dir):
    '''Make future appointments and verify, and use CLINICX and check use of case sensitivity (cLiNiCx, ClInIcX, etc.)'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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
        SC.verapp_bypat(patient='222559876', vlist=['SIXTEEN,PATIENT P', 'Clinicx', 'Future'])
        SC.signoff()        
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test009(resultlog, result_dir):
    '''Make appts with variable length. Make appt in distant future for EWL'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir)
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
                        ALvlist=['THIRTEEN,PATIENT M','Clinicx', 'Clinica', 'Clinica'], 
                        EPvlist=['THIRTEEN,PATIENT M','CLINICX', '8904', 'FUTURE', 'SCHEDULED', 'REGULAR'])
        SC.signoff()        
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')
                       
def startmon(resultlog, result_dir):
    '''Starts Coverage Monitor'''
    testname=sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1=connect_VistA(testname, result_dir)
        VistA1.startCoverage(routines=['SC*', 'SD*'])
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname+ ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def stopmon (resultlog, result_dir):
    ''' STOP MONITOR'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Connect to VistA
        VistA1=connect_VistA(testname, result_dir)
        VistA1.stopCoverage(path=(result_dir + '/' + 'Scheduling_coverage.txt'))
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def connect_VistA(testname, result_dir):
    # Connect to VistA
    from OSEHRAHelper import ConnectToMUMPS, PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + testname + '.txt', instance='', namespace='')
    if VistA.type == 'cache':
        try:
            VistA.ZN('VISTA')
        except IndexError, no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
