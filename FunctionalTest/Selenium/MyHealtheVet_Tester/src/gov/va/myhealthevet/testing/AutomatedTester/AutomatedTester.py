'''
Created on Nov 29, 2012

@author: afequiere004
'''

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
import time

import sys
import argparse
#sys.path = ['./Selenium/lib'] + sys.path
sys.path = ['./Selenium/MyHealtheVet_Tester'] +['./Selenium/lib'] + sys.path
import logging
import glob
import os, errno
import sched
import time

class AutomatedTester(object):    
    
    BROWSER_DRIVER = {'FIREFOX': webdriver.Firefox, 'IE': webdriver.Ie,'CHROME': webdriver.Chrome}
    driver = None
    driverName = None    
    
    #capabilites = DesiredCapabilities

    def __init__(self, driverType):
        self.setupDriver(driverType)
        
    def setupDriver(self, driverType):
        # checks browser type and assigns appropriate driver
        if driverType not in self.BROWSER_DRIVER.keys() :        
            self.driver = webdriver.Firefox
            self.driverName = "FIREFOX" 
        else:
            self.driver = self.BROWSER_DRIVER.get(driverType)
            self.driverName = driverType
            
    def openDriver(self):
        #self.driver = webdriver.Firefox
        instanceString = str(self.driver.__class__)
        logging.info(instanceString)
        
        if instanceString.find('type') == -1:
            self.driver = self.BROWSER_DRIVER.get(self.driverName)
        
        self.driver=self.driver()
        return self.driver        
            
    def closeDriver(self):
        self.driver.quit()    
    