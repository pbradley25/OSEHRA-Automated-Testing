'''
Created on Nov 29, 2012

@author: afequiere004
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from src.gov.va.myhealthevet.testing.AutomatedTester.AutomatedTester import AutomatedTester
import time
import datetime
import argparse
import logging
import sys,os
#sys.path = ['./Selenium/MyHealtheVet_Tester'] +['./Selenium/lib'] + sys.path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#sys.path = ['./Selenium/lib'] + sys.path


def pl_test001(automatedTester):
    ''' Sample Test '''
    testname = sys._getframe().f_code.co_name
    #resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Open driver    
        driver = automatedTester.openDriver()
        
        # go to the google home page
        driver.get("http://www.google.com")
        
        # find the element that's name attribute is q (the google search box)
        inputElement = object()
        inputElement = driver.find_element_by_name("q")
        
        # type in the search
        inputElement.send_keys("Cheese!")
        
        # submit the form (although google automatically searches now without submitting)
        inputElement.submit()
        
        # the page is ajaxy so the title is originally this:
        logging.info( driver.title)
        
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 10).until(lambda driver : driver.title.lower().startswith("cheese!"))

        # You should see "cheese! - Google Search"
        logging.info(driver.title)
    except Exception as detail:
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result \n' + detail)
    else:
        logging.info('Pass\n')
    finally:
        automatedTester.closeDriver()    
