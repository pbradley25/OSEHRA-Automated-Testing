'''
Created on Nov 29, 2012

@author: afequiere004
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from src.gov.va.myhealthevet.testing.AutomatedTester.AutomatedTester import AutomatedTester
import time
import datetime
import argparse
import logging
import sys
#sys.path = ['./Selenium/MyHealtheVet_Tester'] +['./Selenium/lib'] + sys.path
#sys.path = ['./Selenium/lib'] + sys.path


def pl_test001(automatedTester):
    ''' Sample Test '''
    testname = sys._getframe().f_code.co_name
    base_url = "https://www.myhealth.va.gov/mhv-portal-web/"
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Open driver    
        driver = automatedTester.openDriver()
        
        # go to MyHealtheVet login home  
        
        #driver.get(base_url + "mhv-portal-web/anonymous.portal?_nfpb=true&_nfto=false&_pageLabel=mhvHome")
        driver.get(base_url)
        driver.find_element_by_name("loginPortlet_homepage{actionForm.userName}").clear()
        driver.find_element_by_name("loginPortlet_homepage{actionForm.userName}").send_keys("afequiere")
        driver.find_element_by_name("loginPortlet_homepage{actionForm.password}").clear()
        driver.find_element_by_name("loginPortlet_homepage{actionForm.password}").send_keys("1vahealth!")
        driver.find_element_by_css_selector("input.mhv-input-button").click()
        driver.find_element_by_link_text("PERSONAL INFORMATION").click()
        driver.find_element_by_link_text("My Profile").click()
        driver.find_element_by_name("manageUserProfile_profilesactionOverride:cancelAction").click()
        driver.find_element_by_name("manageUserProfile_profilesactionOverride:anonymCancelAction").click()
        driver.find_element_by_link_text("Logout").click()
    except Exception as detail:
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result \n' + detail)
    else:
        logging.info('Pass\n')
    finally:
        automatedTester.closeDriver()
        
def pl_test002(automatedTester):
    ''' Sample Test '''
    testname = sys._getframe().f_code.co_name
    base_url = "https://www.myhealth.va.gov/mhv-portal-web/"
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Open driver    
        driver = automatedTester.openDriver()
        
        # go to MyHealtheVet login home  
        
        #driver.get(base_url + "mhv-portal-web/anonymous.portal?_nfpb=true&_nfto=false&_pageLabel=mhvHome")
        driver.get(base_url)
        driver.find_element_by_name("loginPortlet_homepage{actionForm.userName}").clear()
        driver.find_element_by_name("loginPortlet_homepage{actionForm.userName}").send_keys("afequiere")
        driver.find_element_by_name("loginPortlet_homepage{actionForm.password}").clear()
        driver.find_element_by_name("loginPortlet_homepage{actionForm.password}").send_keys("1vahealth!")
        driver.find_element_by_css_selector("input.mhv-input-button").click()
        driver.find_element_by_link_text("PERSONAL INFORMATION").click()
        driver.find_element_by_link_text("My Profile").click()        
        driver.find_element_by_link_text("Logout").click()
    except Exception as detail:
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result \n' + detail)
    else:
        logging.info('Pass\n')
    finally:
        automatedTester.closeDriver()             
