'''
Created on November, 2012
@author: pbradley
This is the main test script that calls the underlying ADT functional tests
located in ADT_Suite001.
'''
import os
import sys
sys.path = ['./RAS/lib'] + ['./dataFiles'] + ['../lib/vista'] + sys.path
import ADT_Suite001
import TestHelper

def main():
    test_suite_driver = TestHelper.TestSuiteDriver(__file__)
    test_suite_details = test_suite_driver.generate_test_suite_details()

    try:
        test_suite_driver.pre_test_suite_run(test_suite_details)

        # Begin Tests
        ADT_Suite001.startmon(resultlog, args.resultdir)
        ADT_Suite001.setup_ward(resultlog, args.resultdir)
        ADT_Suite001.adt_test001(resultlog, args.resultdir)
        ADT_Suite001.adt_test002(resultlog, args.resultdir)
        ADT_Suite001.stopmon(resultlog, args.resultdir)
        # End Tests

        test_suite_driver.post_test_suite_run(test_suite_details)
    except Exception, e:
        test_suite_driver.exception_handling(test_suite_details, e)
    else:
        test_suite_driver.try_else_handling(test_suite_details)
    finally:
        test_suite_driver.finally_handling(test_suite_details)

    test_suite_driver.end_method_handling(test_suite_details)

if __name__ == '__main__':
  main()
