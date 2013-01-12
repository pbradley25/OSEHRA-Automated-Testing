'''
Created on November, 2012
@author: pbradley
This is the main test script that calls the underlying ADT functional tests
located in ADTMain01_suite.
'''
import os
import sys
sys.path = ['./RAS/lib'] + ['./dataFiles'] + ['../lib/vista'] + sys.path
import ADTMain01_suite
import TestHelper

def main():
    test_suite_driver = TestHelper.TestSuiteDriver(__file__)
    test_suite_details = test_suite_driver.generate_test_suite_details()

    try:
        test_suite_driver.pre_test_suite_run(test_suite_details)

        # Begin Tests
        ADTMain01_suite.startmon(test_suite_details)
        ADTMain01_suite.setup_ward(test_suite_details)
        ADTMain01_suite.adt_test001(test_suite_details)
        ADTMain01_suite.adt_test002(test_suite_details)
        ADTMain01_suite.stopmon(test_suite_details)
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
