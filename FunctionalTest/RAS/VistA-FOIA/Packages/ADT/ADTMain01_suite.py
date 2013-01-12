'''
Created on November 2012


@author: pbradley

'''
import sys
sys.path = ['./FunctionalTest/RAS/lib'] + ['./dataFiles'] + ['./lib/vista'] + sys.path
from ADTActions import ADTActions
import TestHelper

def adt_test001(test_suite_details):
    ''' Admit 4 patients, verify, then discharge them '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
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

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def adt_test002(test_suite_details):
    ''' Schedule, Unschedule, Transfer Patient '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
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

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def setup_ward(test_suite_details):
    ''' Set up ward for ADT testing '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        adt = ADTActions(VistA1)
        adt.signon()
        adt.adt_setup()
        adt.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def startmon(test_suite_details):
    '''Starts Coverage Monitor'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        # Connect to VistA
        VistA1 = test_driver.connect_VistA(test_suite_details)
        VistA1.startCoverage(routines=['GMPL*'])

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)


def stopmon (test_suite_details):
    ''' STOP MONITOR'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        # Connect to VistA
        VistA1=connect_VistA(testname, result_dir)
        VistA1.stopCoverage(path=(test_suite_details.result_dir + '/' + 'ADT_coverage.txt'))

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)


'''
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
'''