'''
Created on November 2012


@author: pbradley

'''
import sys
sys.path = ['./Functional/RAS/lib'] + ['./dataFiles'] + ['./Python/vista'] + sys.path
from ADTActions import ADTActions
import datetime
import time
import TestHelper
import logging

def adt_test001(resultlog, result_dir):
    ''' Admit 4 patients, verify, then discharge them '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        adt.signon()
        adt.admit_a_patient(ssn='888776666', bed='1-A')
        adt.roster_list(vlist=['TWO,PATIENT B', '1-A'])
        adt.det_inpatient_inquiry(ssn='888776666', item='1', vlist=['DIRECT', '1-A', 'ALEXANDER,ROBER', 'SMITH,MARY'])
        adt.switch_bed(ssn='888776666', bed='1-B')
        adt.admit_a_patient(ssn='656451234', bed='1-A')
        adt.roster_list(vlist=['SIX,PATIENT F', '1-A'])
        adt.switch_bed(ssn='656451234', bed='2-A', badbed='1-B')
        adt.admit_a_patient(ssn='656771234', bed='1-A')
        adt.roster_list(vlist=['SEVEN,PATIENT G', '1-A'])
        adt.admit_a_patient(ssn='444678924', bed='2-B')
        adt.roster_list(vlist=['FOURTEEN,PATIENT', '2-B'])
        time.sleep(10)
        adt.seriously_ill_list(ssnlist=['888776666', '656451234', '656771234', '444678924'],
                               vlist1=['FOURTEEN,PATIENT', 'SEVEN,PATIENT', 'SIX,PATIENT', 'TWO,PATIENT'],
                               vlist2=[['TWO,PATIENT', '888776666'],
                                       ['SIX,PATIENT', '656451234'],
                                       ['SEVEN,PATIENT', '656771234'],
                                       ['FOURTEEN,PATIENT', '444678924']])
        adt.treating_spcl_trans(ssn='888776666', spcl='CARDIAC SURGERY')
        time.sleep(10)
        adt.discharge_patient(ssn='888776666', dtime='NOW+1')
        adt.discharge_patient(ssn='656451234', dtime='NOW+10')
        adt.discharge_patient(ssn='656771234', dtime='NOW+100')
        adt.discharge_patient(ssn='444678924', dtime='NOW+1000')
        adt.signoff()
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    else:
        resultlog.write('Pass\n')

def adt_test002(resultlog, result_dir):
    ''' Schedule, Unschedule, Transfer Patient '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        adt.signon()
        adt.admit_a_patient(ssn='888776666', bed='1-A')
        adt.roster_list(vlist=['TWO,PATIENT B', '1-A'])
        adt.det_inpatient_inquiry(ssn='888776666', item='1', vlist=['DIRECT', '1-A', 'ALEXANDER,ROBER', 'SMITH,MARY'])
        adt.schedule_admission(ssn='656451234')
        adt.schedule_admission(ssn='656771234')
        adt.scheduled_admit_list(vlist=['SEVEN,PATIENT G', 'SIX,PATIENT F'])
        time.sleep(10)
        adt.provider_change(ssn='888776666')
        time.sleep(10)
        adt.transfer_patient(ssn='888776666')
        adt.cancel_scheduled_admission(ssn='656451234')
        adt.cancel_scheduled_admission(ssn='656771234')
        adt.signoff()
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    else:
        resultlog.write('Pass\n')

def adt_test003(resultlog, result_dir):
    ''' Wait list testing '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1)
        adt.signon()
        adt.waiting_list_entry(ssn='323554567')
        adt.signon()
        adt.waiting_list_entry(ssn='123455678')
        adt.signon()
        adt.waiting_list_output(vlist=['TWENTYFOUR,PATIENT', 'TWENTYTHREE,PATIENT'])
        adt.signon()
        adt.delete_waiting_list_entry(ssn='323554567')
        adt.signon()
        adt.delete_waiting_list_entry(ssn='123455678')
        adt.signoff()
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    else:
        resultlog.write('Pass\n')

def adt_test004(resultlog, result_dir):
    ''' Lodger checkin / checkout testing '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        adt.signon()
        adt.checkin_lodger(ssn='323554567', bed='1-A')
        adt.checkin_lodger(ssn='123455678', bed='1-B')
        time.sleep(10)
        adt.lodger_checkout(ssn='323554567')
        adt.lodger_checkout(ssn='123455678')
        # DRG Calculation
        adt.wwgeneric(dlist=[[['Option:'], ['bed control menu']],
                              [['Option:'], ['DRG Calculation']],
                              [['Effective Date:'], ['t']],
                              [['Choose Patient from PATIENT file'], ['Yes']],
                              [['Select PATIENT NAME:'], ['123455678']],
                              [['Transfer to an acute care facility'], ['No']],
                              [['Discharged against medical advice'], ['No']],
                              [['Enter PRINCIPAL diagnosis:'], ['heart']],
                              [['STOP or Select'], ['1']],
                              [['Enter SECONDARY diagnosis'], ['chest']],
                              [['STOP or Select'], ['1']],
                              [['Enter SECONDARY diagnosis'], ['']],
                              [['Enter Operation/Procedure'], ['stent']],
                              [['CHOOSE'], ['1']],
                              [['Enter Operation/Procedure'], ['']],
                              [['392', '2.7', '0.7241', '1', '99', '392- ESOPHAGITIS'], []],
                              [['Effective Date'], ['']],
                              [['Choose Patient from PATIENT file'], ['']],
                              [['Select PATIENT NAME:'], ['']],
                              [['Select Bed Control Menu Option'], ['']]])
        adt.signoff()
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    else:
        resultlog.write('Pass\n')

def adt_logflow(resultlog, result_dir):
    ''' Use XTFCR to log flow to file '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1)
        adt.logflow(['DGPMV', 'DGSWITCH'])
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    else:
        resultlog.write('Pass\n')


def setup_ward(resultlog, result_dir):
    ''' Set up ward for ADT testing '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1)
        adt.signon()
        adt.adt_setup()
        adt.signoff()
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    else:
        resultlog.write('Pass\n')


def startmon(resultlog, result_dir):
    '''Starts Coverage Monitor'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    print "startmon1"
    try:
        VistA1 = connect_VistA(testname, result_dir)
        print "startmon2"
        VistA1.startCoverage(routines=['DGPMV', 'DGSWITCH', 'DGSCHAD', 'DGPMEX', 'DGWAIT', 'DGSILL'])
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def stopmon (resultlog, result_dir, humanreadable):
    ''' STOP MONITOR'''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Connect to VistA
        VistA1 = connect_VistA(testname, result_dir)
        path = (result_dir + '/' + timeStamped('ADT_coverage.txt'))
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


def connect_VistA(testname, result_dir):
    # Connect to VistA
    logging.debug('Connect_VistA')
    from OSEHRAHelper import ConnectToMUMPS, PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + timeStamped(testname + '.txt'), instance='', namespace='')
    if VistA.type == 'cache':
        try:
            VistA.ZN('VISTA')
        except IndexError, no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
