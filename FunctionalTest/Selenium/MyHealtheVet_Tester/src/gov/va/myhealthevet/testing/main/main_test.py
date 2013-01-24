'''
Created on Nov 29, 2012

@author: afequiere004
'''
import sys,os
import logging
from selenium import webdriver
sys.path.append(os.path.abspath('MyHealtheVet_Tester'))
from src.gov.va.myhealthevet.testing.testSuite import SampleTestSuite
from src.gov.va.myhealthevet.testing.testSuite import TestSuite1
from src.gov.va.myhealthevet.testing.AutomatedTester.AutomatedTester import AutomatedTester
import errno
import argparse


LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}
BROWSER_NAMES = {'firefox':'FIREFOX', 'ie':'IE', 'chrome':'CHROME'}

def main():
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument('resultdir', help='Result Directory')
    parser.add_argument('-l', '--logging-level', help='Logging level')
    parser.add_argument('-f', '--logging-file', help='Logging file name')
    args = parser.parse_args()
    logging_level = LOGGING_LEVELS.get(args.logging_level, logging.NOTSET)
    
    if not os.path.isdir(args.resultdir):
        try:
            os.makedirs(args.resultdir)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
            
    logging.basicConfig(level=logging_level,
                      filename=args.resultdir +"/" +args.logging_file,
                      filemode='w',
                      format='%(asctime)s %(levelname)s: %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
    
    try:
        logging.debug('RESULTDIR: ' + args.resultdir)
        logging.debug('LOGGING:   ' + args.logging_level)
        """resfile = args.resultdir + '/ProblemList_results.txt'
        if not os.path.isabs(args.resultdir):
            logging.error('EXCEPTION: Absolute Path Required for Result Directory')
            raise
        resultlog = file(resfile, 'w')"""
        automatedTester = AutomatedTester(BROWSER_NAMES.get('firefox'))
        SampleTestSuite.pl_test001(automatedTester)
        TestSuite1.pl_test001(automatedTester)
        TestSuite1.pl_test002(automatedTester)       
        
    except Exception, e:        
        logging.error('*****exception*********' + str(e))
    finally:        
        logging.info('finished')

if __name__ == '__main__':
    main()
