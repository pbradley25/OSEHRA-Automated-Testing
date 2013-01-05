'''
Created on November 2012


@author: pbradley

'''
import sys
sys.path = ['./FunctionalTest/RAS/lib'] + ['./dataFiles'] + ['./lib/vista'] + sys.path
from ADTActions import ADTActions
import datetime
import TestHelper
import logging

def adt_test001(resultlog, result_dir):
    ''' Admit 4 patients, verify, then discharge them '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1=connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        adt.signon()
        adt.admit_a_patient(ssn='888776666', bed='1-B')
        adt.roster_list(vlist=['TWO,PATIENT B    6666', '1-B'])        
        adt.admit_a_patient(ssn='333224444', bed='1-A')
        adt.roster_list(vlist=['THREE,PATIENT C    4444', '1-A'])
        adt.admit_a_patient(ssn='656771234', bed='2-A')
        adt.roster_list(vlist=['SEVEN,PATIENT G    1234', '1-C'])
        adt.admit_a_patient(ssn='345623902', bed='2-B')
        adt.roster_list(vlist=['ELEVEN,PATIENT K    3902', '1-D'])
        adt.discharge_patient(ssn='333224444')
        adt.discharge_patient(ssn='888776666')
        adt.discharge_patient(ssn='656771234')
        adt.discharge_patient(ssn='345623902')
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
        VistA1=connect_VistA(testname, result_dir)
        adt = ADTActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        adt.signon()
        adt.admit_a_patient(ssn='333224444', bed='1-A')
        adt.roster_list(vlist=['THREE,PATIENT C    4444', '1-A'])
        adt.schedule_admission(ssn='888776666')
        adt.schedule_admission(ssn='656771234')
        adt.schedule_admit_list(vlist=['TWO,PATIENT B    6666', 'SEVEN,PATIENT G    1234'])
        adt.transfer_patient(ssn='333224444')
        adt.cancel_scheduled_admission(ssn='888776666')
        adt.cancel_scheduled_admission(ssn='656771234')
        adt.signoff()
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
        VistA1=connect_VistA(testname, result_dir)
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
    testname=sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    print "startmon1"
    try:
        VistA1=connect_VistA(testname, result_dir)
        print "startmon2"
        VistA1.startCoverage(routines=['GMPL*'])
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
        VistA1.stopCoverage(path=(result_dir + '/' + 'ADT_coverage.txt'))
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
    print "connect_VistA"
    logging.debug('Connect_VistA')
    from OSEHRAHelper import ConnectToMUMPS,PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + testname + '.txt', instance='', namespace='')
    if VistA.type=='cache':
        try:
            print "connect_VistA1"
            VistA.ZN('VISTA')
        except IndexError,no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
