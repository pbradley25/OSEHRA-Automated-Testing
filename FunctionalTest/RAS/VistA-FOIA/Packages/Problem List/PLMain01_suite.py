'''
Created on Mar 9, 2012


@author: pbradley

'''
import sys
sys.path = ['./FunctionalTest/RAS/lib'] + ['./dataFiles'] + ['./lib/vista'] + sys.path
from PLActions import PLActions
from ORActions import ORActions
import TestHelper

def pl_test001(test_suite_details):
    ''' NIST Inpatient Test '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        ''' 
        If you want to use the config file to load the codes in you can use this code snippet
        but it would be best to let the method connect_Vista in TestHelper do this, as is the
        case with the tests RASR generates by default.
        
        p1 = PLActions(VistA1,
               user=TestHelper.fetch_access_code(test_suite_details, testname),
               code=TestHelper.fetch_verify_code(test_suite_details, testname))
        '''
        pl.signon()
        pl.addcsv(ssn='333224444', pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.editinactivate(ssn='333224444', probnum='4', resdate='08/29/2010')
        pl.editinactivate(ssn='333224444', probnum='3', resdate='08/29/2010')
        pl.verplist(ssn='333224444', vlist=['Essential Hypertension',
                                            'Chronic airway obstruction'])
        pl.verify(ssn='333224444', probnum='1', itemnum='1',
                     evalue='Essential Hypertension')
        pl.verify(ssn='333224444', probnum='2', itemnum='1',
                     evalue='Chronic airway obstruction')
        pl.verify(ssn='333224444', probnum='1', itemnum='1',
                     evalue='Acute myocardial', view='IA')
        pl.verify(ssn='333224444', probnum='2', itemnum='1',
                     evalue='Congestive Heart Failure', view='IA')
        for i in range(4):
            pl.rem(ssn='333224444')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test002(test_suite_details):
    ''' Restore Removed Problems '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='888776666', pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.editinactivate(ssn='888776666', probnum='4', resdate='08/29/2010')
        pl.editinactivate(ssn='888776666', probnum='3', resdate='08/29/2010')
        pl.verplist(ssn='888776666', vlist=['Essential Hypertension',
                                            'Chronic airway obstruction'])
        pl.verify(ssn='888776666', probnum='1', itemnum='1',
                     evalue='Essential Hypertension')
        pl.verify(ssn='888776666', probnum='2', itemnum='1',
                     evalue='Chronic airway obstruction')
        pl.verify(ssn='888776666', probnum='1', itemnum='1',
                     evalue='Acute myocardial', view='IA')
        pl.verify(ssn='888776666', probnum='2', itemnum='1',
                     evalue='Congestive Heart Failure', view='IA')
        for i in range(4):
            pl.rem(ssn='888776666')
        pl.checkempty(ssn='888776666')
        pl.replace(ssn='888776666', probnum='1')
        pl.verify(ssn='888776666', probnum='1', itemnum='1',
                     evalue='Essential Hypertension')
        pl.rem(ssn='888776666')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test003(test_suite_details):
    ''' Change Problem Data '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='656771234',
                     pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.editsimple(ssn='656771234', probnum='1', itemnum='1',
                        chgval='787.1')
        pl.editsimple(ssn='656771234', probnum='1', itemnum='2',
                        chgval='3/26/12')
        pl.editsimple(ssn='656771234', probnum='1', itemnum='4',
                        chgval='MANAGER')
        pl.editsimple(ssn='656771234', probnum='1', itemnum='5',
                        chgval='VISTA')
        pl.verify(ssn='656771234', probnum='1', itemnum='1',
                     evalue='Heartburn')
        pl.verify(ssn='656771234', probnum='1', itemnum='2',
                     evalue='3/26/12')
        pl.verify(ssn='656771234', probnum='1', itemnum='4',
                     evalue='MANAGER,SYSTEM')
        pl.verify(ssn='656771234', probnum='1', itemnum='5',
                     evalue='VISTA')
        for i in range(4):
            pl.rem(ssn='656771234')
        pl.checkempty(ssn='656771234')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test004(test_suite_details):
    ''' Create Problem Selection List, add/modify/remove categories and problems '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1)
        pl.signon()
        pl.createsellist(listname="List001", clinic='VISTA')
        pl.createcat(listname='List001', catname='cat001')
        pl.createcat(listname='List001', catname='cat002')
        pl.catad(listname='List001', catname='cat001', icd='787.1')
        pl.catad(listname='List001', catname='cat001', icd='786.50')
        pl.catad(listname='List001', catname='cat001', icd='100.0')
        pl.catad(listname='List001', catname='cat002', icd='780.50')
        pl.catad(listname='List001', catname='cat002', icd='292.0')
        pl.catad(listname='List001', catname='cat002', icd='304.90')
        pl.sellistad(listname='List001', catname='cat001')
        pl.sellistad(listname='List001', catname='cat002')
        pl.versellist(ssn='656454321', clinic='VISTA',
                      vlist=['List001', 'cat001', 'Heartburn', 'chest pain',
                             'Leptospirosis', 'cat002', 'Sleep Disturbance',
                             'Drug withdrawal', 'drug dependence'])
        pl.add(ssn='656454321', clinic='VISTA', probnum='1',
                  comment='this is a test', onsetdate='t', status='Active',
                  acutechronic='A', service='N', evalue='Heartburn')
        pl.verify(ssn='656454321', probnum='1', itemnum='1',
                     evalue='Heartburn')
        pl.rem(ssn='656454321')
        pl.sellistrm(listname='List001')
        pl.sellistrm(listname='List001')
        pl.catdl(listname='List001', catname='cat001')
        pl.catdl(listname='List001', catname='cat002')
        pl.sellistrfu(listname='List001', username='Alexander')
        pl.sellistdl(listname='List001')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test005(test_suite_details):
    ''' Create Problem Selection List, assign to user, and add problem '''
    '''Separate VistA Instances to allow concurrent logins in case of
    future use of tstart and trollback when these features are available'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        test_driver.testname = testname + "_01"
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl1 = PLActions(VistA1)
        pl1.signon()
        pl1.createsellist(listname="List002", clinic='')
        pl1.sellistgal(listname="List002", username='Alexander')
        pl1.createcat(listname='List002', catname='cat011')
        pl1.createcat(listname='List002', catname='cat022')
        pl1.catad(listname='List002', catname='cat011', icd='787.1')
        pl1.catad(listname='List002', catname='cat011', icd='786.50')
        pl1.catad(listname='List002', catname='cat011', icd='100.0')
        pl1.catad(listname='List002', catname='cat022', icd='780.50')
        pl1.catad(listname='List002', catname='cat022', icd='292.0')
        pl1.catad(listname='List002', catname='cat022', icd='304.90')
        pl1.sellistad(listname='List002', catname='cat011')
        pl1.sellistad(listname='List002', catname='cat022')

        test_driver.testname = testname + "_02"
        VistA2 = test_driver.connect_VistA(test_suite_details)
        pl2 = PLActions(VistA2, user='fakedoc1', code='1Doc!@#$')
        pl2.signon()
        pl2.versellist(ssn='345623902', clinic='',
                      vlist=['List002', 'cat011', 'Heartburn', 'chest pain',
                             'Leptospirosis', 'cat022', 'Sleep Disturbance',
                             'Drug withdrawal', 'drug dependence'])
        pl2.add(ssn='345623902', clinic='', probnum='1',
                   comment='this is a test', onsetdate='t',
                   status='Active', acutechronic='A', service='N',
                   evalue='Heartburn')
        pl2.verify(ssn='345623902', probnum='1', itemnum='1',
                      evalue='Heartburn')
        pl2.rem(ssn='345623902')
        pl1.sellistrm(listname='List002')
        pl1.sellistrm(listname='List002')
        pl1.catdl(listname='List002', catname='cat011')
        pl1.catdl(listname='List002', catname='cat022')
        pl1.sellistrfu(listname='List002', username='Alexander')
        pl1.sellistdl(listname='List002')
        pl2.signoff()
        pl1.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test006 (test_suite_details):
    ''' Create Selection List from IB Encounter Form'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA, user='fakenurse1', code='1Nur!@#$')
        pl.signon()
        pl.createibform('LAB', 'FORM1', 'Group1', ['428.0', '410.90', '401.9'])
        pl.sellistib('FORM1', 'List003', 'LAB')
        pl.versellist(ssn='345238901', clinic='LAB',
                   vlist=['List003', 'Group1', 'Congestive Heart Failure', 'Acute myocardial', 'Essential Hypertension'])
        pl.add(ssn='345238901', clinic='LAB', probnum='1',
                  comment='this is a test', onsetdate='t', status='Active',
                  acutechronic='A', service='N', evalue='Congestive')
        pl.verify(ssn='345238901', probnum='1', itemnum='1',
                     evalue='Congestive')
        pl.rem('345238901')
        pl.sellistrm(listname='List003')
        pl.catdl(listname='List003', catname='Group1')
        pl.sellistrfu(listname='List003', username='Alexander')
        pl.sellistdl(listname='List003')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test007 (test_suite_details):
    ''' Add problems and View Patients by Problems (PL menu items 4 & 5)'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='655447777', pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.addcsv(ssn='543236666', pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.addcsv(ssn='345678233', pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.verlistpats(vlist=['EIGHT,PATIENT', 'ONE,PATIENT', 'TWELVE,PATIENT'])
        pl.verpatsrch(prob='428.0', vlist=['EIGHT,PATIENT', 'ONE,PATIENT', 'TWELVE,PATIENT'])
        for i in range(4):
            pl.rem('655447777')
            pl.rem('543236666')
            pl.rem('345678233')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test008 (test_suite_details):
    ''' Add problem via data entry as clerk and change as doctor'''
    '''Multiple VistA instances to allow concurrent logins for when
    tstart and trollback become available and implemented'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        test_driver.testname = testname + "_01"
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl1 = PLActions(VistA1, user='fakeclerk1', code='1Cle!@#$')
        pl1.signon()
        pl1.dataentry(ssn='666551234', provider='Alexander', clinic='', problem='chest pain',
                      comment='test', onsetdate='t', status='Active', acutechronic='A',
                      service='N')
        pl1.signoff()

        test_driver.testname = testname + "_02"
        VistA2 = test_driver.connect_VistA(test_suite_details)
        pl2 = PLActions(VistA2, user='fakedoc1', code='1Doc!@#$')
        pl2.signon()
        pl2.editsimple(ssn='666551234', probnum='1', itemnum='1', chgval='786.50')
        pl2.verplist(ssn='666551234', vlist=['Unspecified chest pain'])
        pl2.rem('666551234')
        pl2.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test009 (test_suite_details):
    ''' Verify Problem List through Order Entry package'''
    '''Multiple VistA instances to allow concurrent logins for when
    tstart and trollback become available and implemented'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        test_driver.testname = testname + "_01"
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='323678904', pfile='./FunctionalTest/dataFiles/NISTinpatientdata0.csv')
        pl.verplist(ssn='323678904', vlist=['Essential Hypertension',
                                            'Chronic airway obstruction',
                                            'Acute myocardial',
                                            'Congestive Heart Failure'])
        pl.signoff()

        test_driver.testname = testname + "_02"
        VistA2 = test_driver.connect_VistA(test_suite_details)
        oentry = ORActions(VistA2)
        oentry.signon()
        oentry.verproblems(ssn='323678904', vlist=['Essential Hypertension',
                                            'Chronic airway obstruction',
                                            'Acute myocardial',
                                            'Congestive Heart Failure'])
        oentry.signoff()

        test_driver.testname = testname + "_03"
        VistA3 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA3, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        for i in range(4):
            pl.rem('323678904')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test010(test_suite_details):
    ''' Add problems to Problem List and then Remove them. '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='323554545', pfile='./FunctionalTest/dataFiles/probdata0.csv')
        pl.verplist(ssn='323554545', vlist=['drug abuse', 'Arterial embolism'])
        pl.rem(ssn='323554545')
        pl.rem(ssn='323554545')
        pl.checkempty(ssn='323554545')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test011(test_suite_details):
    ''' Add a problem, add comments, and then remove to/from Problem List. '''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='656451234', pfile='./FunctionalTest/dataFiles/probdata0.csv')
        pl.verplist(ssn='656451234', vlist=['drug abuse', 'Arterial embolism'])
        pl.comcm(ssn='656451234', probnum='1', comment='this is XZY a test')
        pl.rem(ssn='656451234')
        pl.rem(ssn='656451234')
        pl.checkempty(ssn='656451234')
        pl.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test012(test_suite_details):
    '''Problem List Menu Testing'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        test_driver.testname = testname + "_01"
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.addcsv(ssn='656451234', pfile='./FunctionalTest/dataFiles/probdata0.csv')
        pl.detview(ssn='656451234', probnum='2', vlist1=['ACTIVE', 'ALEXANDER', '444.21'], vlist2=['hurts'])
        pl.rem(ssn='656451234')
        pl.rem(ssn='656451234')
        pl.checkempty(ssn='656451234')
        pl.signoff()

        test_driver.testname = test_driver.testname + "_02"
        VistA2 = test_driver.connect_VistA(test_suite_details)
        p2 = PLActions(VistA2, user='fakeclerk1', code='1Cle!@#$')
        p2.signon()
        p2.dataentry(ssn='656451234', provider='Alexander', clinic='', problem='305.91', comment='Test', onsetdate='t', status='a', acutechronic='A', service='n')
        p2.signoff()

        test_driver.testname = testname + "_03"
        VistA3 = test_driver.connect_VistA(test_suite_details)
        p3 = PLActions(VistA3, user='fakedoc1', code='1Doc!@#$')
        p3.signon()
        p3.verifyproblem(ssn='656451234', problem='305.91')
        p3.signoff()

        test_driver.testname = testname + "_04"
        VistA4 = test_driver.connect_VistA(test_suite_details)
        p4 = PLActions(VistA4, user='fakedoc1', code='1Doc!@#$')
        p4.signon()
        p4.selectnewpatient(ssn1='656451234', name1='SIX,', ss2='323554545', name2='NINE,')
        p4.signoff()

        test_driver.testname = testname + "_05"
        VistA5 = test_driver.connect_VistA(test_suite_details)
        p5 = PLActions(VistA5, user='fakedoc1', code='1Doc!@#$')
        p5.signon()
        p5.addcsv(ssn='656451234', pfile='./FunctionalTest/dataFiles/probdata0.csv')
        p5.printproblemlist(ssn='656451234', vlist=['PROBLEM LIST', '305.91'])
        p5.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)

def pl_test013(test_suite_details):
    # Tests the remainder of the selection list Build menu options
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        pl = PLActions(VistA1, user='fakedoc1', code='1Doc!@#$')
        pl.signon()
        pl.createsellist(listname="List001", clinic='VISTA')
        pl.createsellist(listname="List002", clinic='VISTA')
        pl.createcat(listname='List001', catname='cat001')
        pl.createcat(listname='List001', catname='cat002')
        pl.catad(listname='List001', catname='cat001', icd='787.1')
        pl.catad(listname='List001', catname='cat001', icd='786.50')
        pl.catad(listname='List001', catname='cat001', icd='100.0')
        pl.catad(listname='List001', catname='cat002', icd='780.50')
        pl.catad(listname='List001', catname='cat002', icd='292.0')
        pl.catad(listname='List001', catname='cat002', icd='304.90')
        pl.sellistad(listname='List001', catname='cat001')
        pl.sellistad(listname='List001', catname='cat002')
        pl.resequencecat(listname='List001', catnames=['cat001', 'cat002'])
        pl.categorydisp(listname='List001', catname='cat001')
        pl.changesellist(list1='List001', list2='List002')
        pl.sellistrm(listname='List001')
        pl.sellistrm(listname='List001')
        pl.catdl(listname='List001', catname='cat001')
        pl.catdl(listname='List001', catname='cat002')
        pl.sellistrfu(listname='List001', username='Alexander')
        pl.sellistdl(listname='List001')
        pl.sellistdl(listname='List002')
        pl.signoff()

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
        VistA1 = test_driver.connect_VistA(test_suite_details)
        VistA1.stopCoverage(path=(test_suite_details.result_dir + '/' + 'ProblemList_coverage.txt'))

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
def test_driver.connect_VistA(testname, result_dir):
    # Connect to VistA
    logging.debug('Connect_VistA')
    from OSEHRAHelper import ConnectToMUMPS,PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + testname + '.txt', instance='', namespace='')
    if VistA.type=='cache':
        try:
            VistA.ZN('VISTA')
        except IndexError,no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
'''
