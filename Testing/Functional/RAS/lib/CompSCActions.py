'''
Created on Jun 14, 2012

@author: afequiere
'''
from Actions import Actions
import TestHelper
import datetime
from datetime import timedelta
import time
import sys
import logging
import tkMessageBox

class CompSCActions (Actions):
    # Object for different Option types
    options = {'Holiday': 'SDHOLIDAY', 'Services': 'ECTP LOCAL SERVICES', 'Clinic Setup': 'SDBUILD', 'Supervisor': 'SDSUP', 'Register a Patient': 'Register a Patient'}
    
    def __init__(self, VistAconn, scheduling=None, user=None, code=None):
        Actions.__init__(self, VistAconn, scheduling, user, code)

    def signon (self, isFileman=None, optionType=None):
        if self.acode is None:
            if isFileman is None:
                self.VistA.wait('')
                self.VistA.write('S DUZ=1 D ^XUP')
                if optionType is None:
                    self.VistA.wait('OPTION NAME:')
                    self.VistA.write('SDAM APPT MGT')
                else:
                    self.VistA.wait('OPTION NAME:')
                    self.VistA.write(self.options[optionType])    #.get(optionType,'undefined'))    
            else:
                self.VistA.wait('')
                self.VistA.write('S DUZ=1 S XUMF=1 D Q^DI')
                self.VistA.wait('OPTION:')
                self.VistA.write('1')       
        else:
            self.VistA.wait('');
            self.VistA.write('D ^ZU')
            self.VistA.wait('ACCESS CODE:');
            self.VistA.write(self.acode)
            self.VistA.wait('VERIFY CODE:');
            self.VistA.write(self.vcode)
            self.VistA.wait('//');
            self.VistA.write('')
            self.VistA.wait('Option:')
            self.VistA.write('Scheduling')

    def schtime(self, delta):
        '''Calculates a time for the next hour or mins'''
        if 'h' in delta:
            ttime = datetime.datetime.now() + datetime.timedelta(hours=int(delta.rstrip('h')))
        elif 'm' in delta:    
            ttime = datetime.datetime.now() + datetime.timedelta(minutes=int(delta.rstrip('m')))
        return ttime.strftime("%H%M")#.lstrip('0')

    def getclinic(self):
        '''Determines which clinic to use based on the time of day'''
        now = datetime.datetime.now()
        hour = now.hour
        if (hour >= 23 and hour <= 24) or (hour >= 0 and hour <= 6):
            clinic = 'Clinic1'
        elif hour >= 7 and hour <= 14:
            clinic = 'Clinic2'
        elif hour >= 15 and hour <= 22:
            clinic = 'CLINICX'
        return clinic

    def dateformat(self, dayadd=0):
        '''Currently not used, needs to be able to handle when the added days
        puts the total days over the months total (ei change 8/35/12 to 9/3/12).
        Idea is to use for date verification'''
        now = datetime.datetime.now()
        month = now.month
        day = now.day + dayadd
        year = now.year % 20
        date = str(month) + '/' + str(day) + '/' + str(year)
        return date
    
    def createCompSchedInsitutions(self):
        '''Creates specific institutions for Scheduling Competition'''
        self.VistA.wait('INPUT TO WHAT FILE:')
        self.VistA.write('4')
        self.VistA.wait('EDIT WHICH FIELD')
        self.VistA.write('STATION NUMBER')
        self.VistA.wait('THEN EDIT FIELD')
        self.VistA.write('')
        self.VistA.wait('Select INSTITUTION NAME:')
        self.VistA.write('CALIFORNIA VA HEALTH CARE SYS')
        self.VistA.wait('Are you adding')
        self.VistA.write('Y')
        self.VistA.wait('STATION NUMBER:')
        self.VistA.write('7100')
        self.VistA.wait('Select INSTITUTION NAME:')
        self.VistA.write('CALIFORNIA VA OUTPAT CLIN')
        self.VistA.wait('Are you adding')
        self.VistA.write('Y')
        self.VistA.wait('STATION NUMBER:')
        self.VistA.write('7102')
        self.VistA.wait('Select INSTITUTION NAME:')
        self.VistA.write('')
        self.VistA.wait('Select OPTION:')
        self.VistA.write('1')
        self.VistA.wait('INPUT TO WHAT FILE:')
        self.VistA.write('40.8')
        self.VistA.wait('EDIT WHICH FIELD')
        self.VistA.write('FACILITY NUMBER')
        self.VistA.wait('THEN EDIT FIELD')
        self.VistA.write('INSTITUTION FILE POINTER')
        self.VistA.wait('THEN EDIT FIELD')
        self.VistA.write('')
        self.VistA.wait('DIVISION NAME')
        self.VistA.write('CALIFORNIA VA REGIONAL MED CTR')
        self.VistA.wait('Are you adding')
        self.VistA.write('Y')
        self.VistA.wait('MEDICAL CENTER DIVISION NUM:')
        self.VistA.write('')
        self.VistA.wait('FACILITY NUMBER')
        self.VistA.write('7101')
        self.VistA.write('')
        self.VistA.wait('INSTITUTION FILE POINTER')
        self.VistA.write('7100')
        self.VistA.write('')
        self.VistA.wait('Select OPTION:')
        self.VistA.write('1')
        self.VistA.wait('INPUT TO WHAT FILE:')
        self.VistA.write('4')
        self.VistA.wait('EDIT WHICH FIELD')
        self.VistA.write('ASSOCIATIONS')
        self.VistA.wait('ASSOCIATIONS SUB-FIELD:')
        self.VistA.write('PARENT OF ASSOCIATION')
        self.VistA.wait('ASSOCIATIONS SUB-FIELD:')
        self.VistA.write('')
        self.VistA.wait('THEN EDIT FIELD:')
        self.VistA.write('')
        self.VistA.wait('Select INSTITUTION NAME:')
        self.VistA.write('CALIFORNIA VA HEALTH CARE SYS')
        self.VistA.wait('Select ASSOCIATIONS:')
        self.VistA.write('2')
        self.VistA.wait('INSTITUTION)?')
        self.VistA.write('y')
        self.VistA.wait('PARENT OF ASSOCIATION:')
        self.VistA.write('CALIFORNIA VA OUTPAT CLIN\r\r')
        
    
    def standardServicesSetup(self):
        '''Standard Services Setup for Scheduling Competition'''
        self.VistA.wait('Select a number (1 - 5):')
        self.VistA.write('1')
        while True:           
            output = self.VistA.wait_re(['LOCAL SERVICE','VISTA>'])
            currentIndex = output[0]
            currentText = output[2]
            currentMatch = output[1]            
            if currentIndex == 1:
                break
            elif "\nMEDICINE\r" in currentText or "\nPSYCHIATRY\r" in currentText or "\nSURGERY\r" in currentText:
                self.VistA.write('YES')
            else:
                self.VistA.write('')
                
    def holidaySetup(self, holidayList):
        '''Holiday Setup for Scheduling Competition'''
        for x in range (0, len(holidayList)):   
            output = self.VistA.wait_re(['ADD/EDIT HOLIDAY'])            
            self.VistA.write(holidayList[x].get('date'))
            self.VistA.wait('as a new HOLIDAY')
            self.VistA.write('Yes')
            self.VistA.wait('HOLIDAY NAME:')
            if x == len(holidayList)-1:
                self.VistA.write(holidayList[x].get('name') + '\r\r')
            else:    
                self.VistA.write(holidayList[x].get('name') + '\r')
                
    def preAppointmentTemplateSetup(self):
        '''pre-Appointment Template Setup for Scheduling Competition'''
        self.VistA.wait('INPUT TO WHAT FILE:')
        self.VistA.write('LETTER')
        self.VistA.wait('1-2:')
        self.VistA.write('1')
        self.VistA.wait('EDIT WHICH FIELD:')
        self.VistA.write('ALL')
        self.VistA.wait('Select LETTER NAME:')
        self.VistA.write('NEW APPOINTMENT')
        self.VistA.wait(')?')
        self.VistA.write('yes')
        self.VistA.wait('TYPE:')
        self.VistA.write('P\r')
        self.VistA.wait('INITIAL SECTION OF LETTER:')
        self.VistA.write('This is a test pre-appointment letter\r\r')
        self.VistA.wait('FINAL SECTION OF LETTER:')
        self.VistA.write('Thanks\r\r')
        self.VistA.wait('Select LETTER NAME:')
        self.VistA.write('\r')
    
    def appointmentTypeSetup(self):
        '''Standard Appointment Type Setup for Scheduling Competition'''
        self.VistA.wait('INPUT TO WHAT FILE:')
        self.VistA.write('appointment type')
        self.VistA.wait('EDIT WHICH FIELD')
        self.VistA.write('ALL')
        self.VistA.wait('Select APPOINTMENT TYPE NAME:')
        self.VistA.write('??')
        
        output = self.VistA.wait_re(['Select APPOINTMENT TYPE NAME:'])
        currentText = output[2]
        if "COMPENSATION & PENSION" in currentText and "EMPLOYEE" in currentText and "REGULAR" in currentText:
            ''' then good '''
        else:
            ''' add them '''
        self.VistA.write('\r\r')
    
    def clinicSetup(self, clinicList):
        '''Clinic setup for Scheduling Competition'''
        for i in range(0, len(clinicList)):            
            self.VistA.wait('CLINIC NAME:')
            self.VistA.write(clinicList[i].get('name'))
            self.VistA.wait('LOCATION?')
            self.VistA.write('Yes')
            self.VistA.wait('NAME:')
            self.VistA.write('')
            self.VistA.wait('ABBREVIATION')
            self.VistA.write(clinicList[i].get('abr'))
            self.VistA.wait('FACILITY?')
            self.VistA.write('')
            self.VistA.wait('SERVICE:')
            self.VistA.write('MEDICINE')
            self.VistA.wait('CLINIC?')
            self.VistA.write('N')
            self.VistA.wait('NUMBER:')
            self.VistA.write('323')
            self.VistA.wait('TYPE:')
            self.VistA.write('')
            self.VistA.wait('MEDS?')
            self.VistA.write('')
            self.VistA.wait('TELEPHONE')
            self.VistA.write('')
            self.VistA.wait('FILMS?')
            self.VistA.write('Yes')
            self.VistA.wait('PROFILES?')
            self.VistA.write('Yes')
            for x in range(0, 4):
                output = self.VistA.wait_re(['LETTER:'])
                currentText = output[2]
                if "\nPRE-APP" in currentText:
                    self.VistA.write('New Appointment')
                else:
                    self.VistA.write('')    
            self.VistA.wait('TIME:')
            self.VistA.write('Yes')
            self.VistA.wait('PROVIDER:')
            self.VistA.write(clinicList[i].get('provider1'))
            self.VistA.wait(')?')
            self.VistA.write('Yes')
            self.VistA.wait('DEFAULT PROVIDER:')
            self.VistA.write('yes')
            self.VistA.wait('PROVIDER:')
            self.VistA.write(clinicList[i].get('provider2'))
            self.VistA.wait(')?')
            self.VistA.write('Yes')
            self.VistA.wait('DEFAULT PROVIDER:')
            self.VistA.write('no')
            self.VistA.wait('PROVIDER:')
            self.VistA.write('')
            self.VistA.wait('PRACTITIONER?')
            self.VistA.write('')
            self.VistA.wait('DIAGNOSIS')
            self.VistA.write('')
            self.VistA.wait('CHK OUT:')
            self.VistA.write('')
            self.VistA.wait('NO-SHOWS:')
            self.VistA.write('10')
            self.VistA.wait('BOOKING')
            self.VistA.write('365')
            self.VistA.wait('BEGINS:')
            self.VistA.write('8')
            self.VistA.wait('REBOOK:')
            self.VistA.write('')
            self.VistA.wait('REBOOK:')
            self.VistA.write('365')
            self.VistA.wait('HOLIDAYS')
            self.VistA.write('Yes')
            self.VistA.wait('CODE:')
            self.VistA.write('450')
            self.VistA.wait('CLINIC')
            self.VistA.write('')
            self.VistA.wait('LOCATION')
            self.VistA.write('')
            self.VistA.wait('CLINIC')
            self.VistA.write('')
            self.VistA.wait('MAXIMUM')
            self.VistA.write('4')
            self.VistA.wait('INSTRUCTIONS')
            self.VistA.write('')
            self.VistA.wait('LENGTH')
            self.VistA.write('15')
            self.VistA.wait('LENGTH')
            self.VistA.write('yes')
            self.VistA.wait('HOUR')
            self.VistA.write('4')
            for a in range(0, 7):
                self.VistA.wait('DATE:')
                if a == 0:       
                    self.VistA.write('t')
                else:
                    self.VistA.write('t+' + str(a))    
                self.VistA.wait('TIME:')
                self.VistA.write('0800-1600')
                self.VistA.wait('SLOTS:')
                self.VistA.write('16')
                self.VistA.wait('TIME:')
                self.VistA.write('')
                self.VistA.wait('INDEFINITELY')
                self.VistA.write('Yes')
            self.VistA.wait('DATE:')
            self.VistA.write('')
        self.VistA.write('')
    
    def modifyClinicInst(self, clinicList):
        '''Modify Clinic Institution mapping file for Scheduling Competition'''
        self.VistA.wait('INPUT TO WHAT FILE:')
        self.VistA.write('Hospital Location')
        self.VistA.wait('EDIT WHICH FIELD')
        self.VistA.write('Institution\r')
        for i in range(0,len(clinicList)):            
            self.VistA.wait('LOCATION NAME:')
            self.VistA.write(clinicList[i].get('name'))
            self.VistA.wait('INSTITUTION:')
            self.VistA.write(clinicList[i].get('facilityId'))
        self.VistA.wait('LOCATION NAME:')
        self.VistA.write('\r')    
    
    def deactivateClinic(self, clinic):
        '''Deactivates a clinic for Scheduling Competition'''
        self.VistA.wait('Menu Option:')
        self.VistA.write('Inactivate')
        self.VistA.wait('CLINIC NAME:')
        self.VistA.write(clinic)
        self.VistA.wait('to be Inactivated:')
        self.VistA.write('t' + '\r')
        self.VistA.wait('halt?')
        self.VistA.write('yes' )       
        
    def reactivateClinic(self, clinic):
        '''Reactivates a clinic for Scheduling Competition'''
        self.VistA.wait('Menu Option:')
        self.VistA.write('Reactivate')    
        self.VistA.wait('CLINIC NAME:')
        self.VistA.write(clinic)
        self.VistA.wait('to be reactivated:')
        self.VistA.write('t+1')
        self.VistA.wait('TIME:')
        self.VistA.write('0800-1600')
        self.VistA.wait('SLOTS:')
        self.VistA.write('16')
        self.VistA.wait('TIME:')
        self.VistA.write('')
        self.VistA.wait('INDEFINITELY')
        self.VistA.write('Yes')
        self.VistA.wait('now?')
        self.VistA.write('Yes')
        for a in range(2, 8):
            self.VistA.wait('DATE:')
            self.VistA.write('t+' + str(a))
            self.VistA.wait('TIME:')
            self.VistA.write('0800-1600')
            self.VistA.wait('SLOTS:')
            self.VistA.write('16')
            self.VistA.wait('TIME:')
            self.VistA.write('')
            self.VistA.wait('INDEFINITELY')
            self.VistA.write('Yes')
        self.VistA.wait('DATE:')
        self.VistA.write('\r')
        self.VistA.wait('halt?')
        self.VistA.write('yes' )
    
    def copyMultiAppDateRange(self, clinic, appointment, strDate, endDate):
        '''Makes Multiple Appointment for specified user at specified time'''
        dateFormat = "%m/%d/%Y"
        d1 = datetime.datetime.strptime(strDate, dateFormat)
        d2 = datetime.datetime.strptime(endDate, dateFormat)
        length = (d2-d1).days
        currentDate = d1
        originalDateTime = appointment['datetime']
        #tkMessageBox.showinfo("length of Days: ",str(length) + " || currentDate: " + str(currentDate))   
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+365')
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        print "this is a bug"
        for i in range(0,length+1):
            appointment['datetime'] = str(currentDate.strftime("%b %d %Y")) + originalDateTime
            #tkMessageBox.showinfo("appointment datetime: ",appointment['datetime'])
            self.makeAppForLoop(appointment.get('patient'), appointment.get('datetime'), appointment.get('mins'), appointment.get('note'), appointment.get('fresh'), appointment.get('nextAvailable'))
            currentDate += timedelta(days=1)
            #tkMessageBox.showinfo("next date: ",str(currentDate)) 
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
            
    def makeMultiApp(self, clinic, appointments):
        '''Makes Multiple Appointment for specified user at specified time'''
        number = len(appointments)
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+365')
        for i in range(0,number):
            self.makeAppForLoop(appointments[i].get('patient'), appointments[i].get('datetime'), appointments[i].get('mins'), appointments[i].get('note'), appointments[i].get('fresh'),appointments[i].get('nextAvailable')) 
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
           
        
    def makeAppForLoop(self, patient, datetime, mins, note, fresh=None, nextAvailable=None):
        '''Makes Appointment for specified user at specified time used in loops'''
        self.VistA.wait('Select Action:')
        self.VistA.write('MA')
        '''self.VistA.wait('PATIENT NAME:')
        self.VistA.write('??')
        if self.VistA.wait('TO STOP:'):        
            self.VistA.write('^')'''
        self.VistA.wait('PATIENT NAME:')
        self.VistA.write(patient)
        self.VistA.wait('TYPE:')
        self.VistA.write('Regular')        
        option = self.VistA.wait_re(['DISPLAY PENDING APPOINTMENTS:','ETHNICITY:'])
        currentIndex = option[0]
        currentText = option[2]
        #tkMessageBox.showinfo("output: ",str(output[0]) + " || " + str(output[2]))
        if currentIndex == 0 or 'PENDING APPOINTMENTS:' in currentText:
            #self.VistA.wait('APPOINTMENTS:')
            self.VistA.write('Yes')
            output = self.VistA.wait_re(['to escape','ETHNICITY:'])
            nextIndex = output[0]
            if nextIndex == 0:
                self.VistA.write('^')
                self.VistA.wait('ETHNICITY:')
            #if fresh is not None:
            #self.VistA.wait('APPOINTMENTS:')
            #self.VistA.write('Yes')
        #else:
            #self.VistA.wait('APPOINTMENTS:')
            #self.VistA.write('no')              
        self.VistA.write('')
        self.VistA.wait('RACE:')
        self.VistA.write('')
        self.VistA.wait('COUNTRY:')
        self.VistA.write('')
        self.VistA.wait('STREET ADDRESS')
        self.VistA.write('')
        self.VistA.wait('ZIP')
        self.VistA.write('')
        for x in range(0, 2):
            self.VistA.wait('PHONE NUMBER')
            self.VistA.write('')
        self.VistA.wait('BAD ADDRESS')
        self.VistA.write('')
        self.VistA.wait('above changes')
        self.VistA.write('No')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('REQUEST')
        if nextAvailable is None:
            self.VistA.write('Yes')
            self.VistA.wait('DATE/TIME')
        else:
            self.VistA.write(nextAvailable)    
            self.VistA.wait('APPOINTMENT:')
        self.VistA.write(datetime)
        output = self.VistA.wait_re(['OK?','IN MINUTES:'])
        currentIndex = output[0]
        if currentIndex == 0:
            self.VistA.write('Yes')
        #self.VistA.wait('IN MINUTES')
        self.VistA.write(mins)
        self.VistA.wait('CORRECT')
        self.VistA.write('Yes')
        self.VistA.wait('STOPS')
        self.VistA.write('No')
        self.VistA.wait('OTHER INFO:')
        self.VistA.write(note)
        self.VistA.wait('continue:')
        self.VistA.write('')
        output = self.VistA.wait_re(['Check In or Check Out:',':'])
        currentIndex = output[0]
        if currentIndex == 0:#self.VistA.wait('Check In or Check Out:'):#currentIndex == 0:
            self.VistA.write('^')
        
    
    def blockMultiApp(self, appointments):
        '''Blocks Multiple Appointment for specified user at specified time'''
        number = len(appointments)
        for i in range(0,number):
            self.blockApp(appointments[i].get('clinic'), appointments[i].get('date'), appointments[i].get('note'), appointments[i].get('strTime'), appointments[i].get('endTime')) 
    
    def blockApp(self, clinic, date, note, strTime=None, endTime=None, multi=None):
        '''Blocks Appointment for specified user at specified time or full day'''
        self.VistA.wait('Menu Option:')
        self.VistA.write('cancel clinic')    
        self.VistA.wait('CLINIC NAME:')
        self.VistA.write(clinic)
        self.VistA.wait('DATE:')
        self.VistA.write(date)        
        rval = self.VistA.multiwait(['WHOLE DAY?', 'DEVICE:'])
        if rval == 1:
            self.VistA.write('\r')
            option = self.VistA.multiwait(['WHOLE DAY?', 'exit:'])
            if option == 1:
                self.VistA.write('^')
                self.VistA.wait('WHOLE DAY?')    
        if strTime is None or endTime is None:
            #self.VistA.wait('WHOLE DAY?:')
            self.VistA.write('Yes')
            self.VistA.wait('cancellation:')
            self.VistA.write(note)
        else:
            #self.VistA.wait('WHOLE DAY?:')
            self.VistA.write('no')
            self.VistA.wait('PART OF THE DAY?')
            self.VistA.write('YES')
            self.VistA.wait('STARTING TIME:')
            self.VistA.write(strTime)
            self.VistA.wait('ENDING TIME:')
            self.VistA.write(endTime)
            self.VistA.wait('cancellation:')
            self.VistA.write(note)            
        
        option = self.VistA.multiwait(['continue:', ':'])          
        if option == 0:
            self.VistA.write('')
            self.VistA.wait('APPOINTMENTS NOW?')
            self.VistA.write('no')
            self.VistA.wait('PRINTED NOW?')
            self.VistA.write('no') 
        if multi is None:    
            self.VistA.write('\r')    
        
    def restoreMultiApp(self, appointments):
        '''Restores Multiple Blocked Appointment for specified user at specified time'''
        number = len(appointments)
        for i in range(0,number):
            self.restoreApp(appointments[i].get('clinic'), appointments[i].get('date'), appointments[i].get('period'),multi='Yes') 
    
    def restoreApp(self, clinic, date, period=None, multi=None):
        '''restores Blocked Appointment for specified user at specified time or full day'''
        self.VistA.wait('Menu Option:')
        self.VistA.write('restore clinic')    
        self.VistA.wait('CLINIC NAME:')
        self.VistA.write(clinic)
        self.VistA.wait('DATE:')
        self.VistA.write(date)
        option = self.VistA.multiwait(['WHICH PERIOD?', ':'])
        if option == 0 and period is not None:
            self.VistA.write(period)
        elif option == 0 and period is None:
            self.VistA.write('1')
        if multi is None:
            self.VistA.write('\r')        
            
    def listAllAppointmentByDate(self, clinic, strDate, endDate):
        '''Makes Appointment for specified user at specified time'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write(strDate)
        self.VistA.wait('Date:')
        self.VistA.write(endDate)
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('List:')
        self.VistA.write('TA')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
   
    def listAllAppointmentByPatient(self, patient):
        '''Makes Appointment for specified user at specified time'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        '''self.VistA.wait('Date:')
        self.VistA.write(strDate)
        self.VistA.wait('Date:')
        self.VistA.write(endDate)'''
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('List:')
        self.VistA.write('TA')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')     
        
    def listNoShowByDate(self, clinic, strDate, endDate):
        '''Makes Appointment for specified user at specified time'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write(strDate)
        self.VistA.wait('Date:')
        self.VistA.write(endDate)
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('List:')
        self.VistA.write('NS')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')    
    
    def patientRegistration(self, patient):
        '''Patient Registration for a specific user '''        
        self.VistA.wait('PATIENT NAME');
        self.VistA.write(patient.get('name'))
        self.VistA.wait('NEW PATIENT');
        self.VistA.write('YES')
        self.VistA.wait('SEX');
        self.VistA.write(patient.get('sex'))
        self.VistA.wait('DATE OF BIRTH');
        self.VistA.write(patient.get('dob'))
        self.VistA.wait('SOCIAL SECURITY NUMBER');
        self.VistA.write(patient.get('ssn'))
        self.VistA.wait('TYPE');
        self.VistA.write(patient.get('type'))
        self.VistA.wait('PATIENT VETERAN');
        self.VistA.write(patient.get('veteran'))
        self.VistA.wait('SERVICE CONNECTED');
        self.VistA.write(patient.get('service'))
        self.VistA.wait('MULTIPLE BIRTH INDICATOR');
        self.VistA.write(patient.get('isTwin'))
        self.VistA.wait('//');
        self.VistA.write('^\r')
        self.VistA.wait('MAIDEN NAME');
        self.VistA.write(patient.get('maiden'))
        self.VistA.wait('PLACE OF BIRTH');
        self.VistA.write(patient.get('cityOB'))
        self.VistA.wait('PLACE OF BIRTH');
        self.VistA.write(patient.get('stateOB'))
        self.VistA.wait('');
        self.VistA.write('\r\r\r')
    
    def viewPatientDemographic(self, patient):
        '''View specific patient demographic '''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        #self.VistA.wait('Date:')
        #self.VistA.write('t')
        #self.VistA.wait('Date:')
        #self.VistA.write('t+365')
        self.VistA.wait('Select Action:')
        self.VistA.write('PD')
        while True:
            output = self.VistA.wait_re(['Select Action:','changes?','MARITAL STATUS',':'])
            currentText = output[2]
            currentMatch = output[1]
            currentIndex = output[0]
            if currentIndex == 0:
                self.VistA.write('Quit')
                break
            elif currentIndex == 1:                
                self.VistA.write('no')
            elif currentIndex == 2:                
                if '//' in currentText:                    
                    self.VistA.write('')
                else:
                    self.VistA.write('unknown') 
            else:                
                self.VistA.write('')          
    
    def patientCheckin(self, patient, strDate, endDate, appointmentNum):
        '''Patient Checkin now'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write(strDate)
        self.VistA.wait('Date:')
        self.VistA.write(endDate)
        self.VistA.wait('Select Action:')
        self.VistA.write('CI')
        self.VistA.wait('Appointmnet(s)')
        self.VistA.write(appointmentNum)
        self.VistA.wait('CHECKED-IN:')
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
    
    def patientCheckout(self, clinic, strDate, endDate, provider, diagnosis):
        '''Patient Checkout now without follow up'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write(strDate)
        self.VistA.wait('Date:')
        self.VistA.write(endDate)
        self.VistA.wait('Select Action:')
        self.VistA.write('CO')
        '''self.VistA.wait('Appointmnet(s)')
        self.VistA.write(appointmentNum)'''        
        self.VistA.wait('follow-up appointment?')
        self.VistA.write('no')
        self.VistA.wait('Check out date and time:')
        self.VistA.write('now')
        self.VistA.wait('PROVIDER')
        self.VistA.write(provider)
        self.VistA.wait('this ENCOUNTER?')
        self.VistA.write('yes')
        self.VistA.wait('PROVIDER')
        self.VistA.write('')
        self.VistA.wait('Diagnosis')
        self.VistA.write(diagnosis)
        self.VistA.wait('Ok')
        self.VistA.write('yes')
        self.VistA.wait('ENCOUNTER?')
        self.VistA.write('yes')
        self.VistA.wait('Ordering or Resulting:')
        self.VistA.write('R')
        self.VistA.wait('Diagnosis')
        self.VistA.write('')
        self.VistA.wait('Problem List?')
        self.VistA.write('no')
        self.VistA.wait('PROCEDURE')
        self.VistA.write('')
        self.VistA.wait('continue')
        self.VistA.write('')
        self.VistA.wait('check out screen?')
        self.VistA.write('no')
        self.VistA.wait('Clinic:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
    
    def displayPatientAppointments(self, patient, strDate, endDate):
        '''Display Patient appointments'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write(strDate)
        self.VistA.wait('Date:')
        self.VistA.write(endDate)
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
    
    def unschPatientVisit(self, clinic, patient):
        '''Makes a walk-in appointment. Automatically checks in'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('UN')
        self.VistA.wait('Select Patient:')
        self.VistA.write(patient)
        self.VistA.wait('TIME:')
        self.VistA.write('')
        self.VistA.wait('TYPE:')
        self.VistA.write('REGULAR')
        self.VistA.wait('to continue:',40)
        self.VistA.write('')
        self.VistA.wait('Check In or Check Out:')
        self.VistA.write('CI')
        self.VistA.wait('CHECKED-IN:')
        self.VistA.write('')
        self.VistA.wait('to continue:')
        self.VistA.write('')
        self.VistA.wait('SLIP NOW?')
        self.VistA.write('No')    
        self.VistA.wait('Checked In')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
                                                   
    def makeapp(self, clinic, patient, datetime, fresh=None):
        '''Makes Appointment for specified user at specified time'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('MA')
        self.VistA.wait('PATIENT NAME:')
        self.VistA.write('??')
        self.VistA.wait('TO STOP:')
        self.VistA.write('^')
        self.VistA.wait('PATIENT NAME:')
        self.VistA.write(patient)
        self.VistA.wait('TYPE:')
        self.VistA.write('Regular')
        if fresh is not None:
            self.VistA.wait('APPOINTMENTS:')
            self.VistA.write('Yes')
        self.VistA.wait('ETHNICITY:')
        self.VistA.write('')
        self.VistA.wait('RACE:')
        self.VistA.write('')
        self.VistA.wait('COUNTRY:')
        self.VistA.write('')
        self.VistA.wait('STREET ADDRESS')
        self.VistA.write('')
        self.VistA.wait('ZIP')
        self.VistA.write('')
        for x in range(0, 2):
            self.VistA.wait('PHONE NUMBER')
            self.VistA.write('')
        self.VistA.wait('BAD ADDRESS')
        self.VistA.write('')
        self.VistA.wait('above changes')
        self.VistA.write('No')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('REQUEST')
        self.VistA.write('Yes')
        self.VistA.wait('DATE/TIME')
        self.VistA.write('t+5')
        self.VistA.wait('DATE/TIME')
        self.VistA.write(datetime)
        self.VistA.wait('CORRECT')
        self.VistA.write('Yes')
        self.VistA.wait('STOPS')
        self.VistA.write('No')
        self.VistA.wait('OTHER INFO:')
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')

    def makeapp_bypat(self, clinic, patient, datetime, loopnum=1, fresh=None, CLfirst=None, prevCO=None):
        '''Makes Appointment for specified user at specified time'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        for _ in range(loopnum):
            self.VistA.wait('Select Action:')
            if CLfirst is not None:
                self.VistA.write('CL')
                self.VistA.wait('Select Clinic:')
                self.VistA.write(clinic)
                self.VistA.wait('Select Action:')
                self.VistA.write('MA')
                self.VistA.wait('PATIENT NAME:')
                self.VistA.write(patient)
            else:
                self.VistA.write('MA')
                self.VistA.wait('Select CLINIC:')
                self.VistA.write(clinic)
            self.VistA.wait('TYPE:')
            self.VistA.write('Regular')
            if fresh is not None:
                self.VistA.wait('APPOINTMENTS:')
                self.VistA.write('Yes')
            elif _ >= 1:
                self.VistA.wait('APPOINTMENTS:')
                self.VistA.write('Yes')
            self.VistA.wait('ETHNICITY:')
            self.VistA.write('')
            self.VistA.wait('RACE:')
            self.VistA.write('')
            self.VistA.wait('COUNTRY:')
            self.VistA.write('')
            self.VistA.wait('STREET ADDRESS')
            self.VistA.write('')
            self.VistA.wait('ZIP')
            self.VistA.write('')
            for x in range(0, 2):
                self.VistA.wait('PHONE NUMBER')
                self.VistA.write('')
            self.VistA.wait('BAD ADDRESS')
            self.VistA.write('')
            self.VistA.wait('above changes')
            self.VistA.write('No')
            self.VistA.wait('continue:')
            self.VistA.write('')
            self.VistA.wait('REQUEST')
            self.VistA.write('Yes')
            self.VistA.wait('DATE/TIME')
            self.VistA.write(datetime)
            if _ >= 1:
                self.VistA.wait('DO YOU WANT TO CANCEL IT')
                self.VistA.write('Yes')
                self.VistA.wait('Press RETURN to continue:')
                self.VistA.write('')
            if prevCO is not None:
                self.VistA.wait('A check out date has been entered for this appointment!')
                self.VistA.wait('DATE/TIME:')
                self.VistA.write('')
            else:
                self.VistA.wait('CORRECT')
                self.VistA.write('Yes')
                self.VistA.wait('STOPS')
                self.VistA.write('No')
                self.VistA.wait('OTHER INFO:')
                self.VistA.write('')
                self.VistA.wait('continue:')
                self.VistA.write('')
            if CLfirst is not None:
                self.VistA.wait('Select Action:')
                self.VistA.write('?\r')
            else:
                self.VistA.wait('Select CLINIC:')
                self.VistA.write('')
                self.VistA.wait('Select Action:')
                self.VistA.write('?\r')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')

    def makeapp_var(self, clinic, patient, datetime, fresh=None, nextaval=None):
        '''Makes Appointment for clinic that supports variable length appts (CLInicA)'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Select Action:')
        self.VistA.write('CL')
        self.VistA.wait('Select Clinic:')
        self.VistA.write(clinic)
        self.VistA.wait('Select Action:')
        self.VistA.write('MA')
        self.VistA.wait('PATIENT NAME:')
        self.VistA.write(patient)
        self.VistA.wait('TYPE:')
        self.VistA.write('Regular')
        if fresh is not None:
            self.VistA.wait('APPOINTMENTS:')
            self.VistA.write('Yes')
        self.VistA.wait('ETHNICITY:')
        self.VistA.write('')
        self.VistA.wait('RACE:')
        self.VistA.write('')
        self.VistA.wait('COUNTRY:')
        self.VistA.write('')
        self.VistA.wait('STREET ADDRESS')
        self.VistA.write('')
        self.VistA.wait('ZIP')
        self.VistA.write('')
        for x in range(0, 2):
            self.VistA.wait('PHONE NUMBER')
            self.VistA.write('')
        self.VistA.wait('BAD ADDRESS')
        self.VistA.write('')
        self.VistA.wait('above changes')
        self.VistA.write('No')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('REQUEST')
        if nextaval is not None:
            self.VistA.write('No')
            self.VistA.wait('APPOINTMENT')
        else:
            self.VistA.write('Yes')
            self.VistA.wait('DATE/TIME')
        self.VistA.write(datetime)
        if 't+122' in datetime:
            self.VistA.wait('Add to EWL')
            self.VistA.write('Yes')
            self.VistA.wait('continue')
            self.VistA.write('')
            self.VistA.wait('Select Action:')
            self.VistA.write('Quit')
            self.VistA.wait('')
        else:
            self.VistA.wait('LENGTH OF APPOINTMENT')
            self.VistA.write('15')
            self.VistA.wait('increment minutes per hour')
            self.VistA.wait('LENGTH OF APPOINTMENT')
            self.VistA.write('60')
            self.VistA.wait('CORRECT')
            self.VistA.write('Yes')
            self.VistA.wait('STOPS')
            self.VistA.write('No')
            self.VistA.wait('OTHER INFO:')
            self.VistA.write('')
            self.VistA.wait('continue:')
            self.VistA.write('')
            self.VistA.wait('Select Action:')
            self.VistA.write('Quit')
            self.VistA.wait('')


    def set_mademographics(self, clinic, patient, datetime, dgrph, CLfirst=None):
        ''' This test sets demographics via MA action.  This test crashes on SAVE in gtm'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Select Action:')
        if CLfirst is not None:
            self.VistA.write('CL')
            self.VistA.wait('Select Clinic:')
            self.VistA.write(clinic)
            self.VistA.wait('Select Action:')
            self.VistA.write('MA')
            self.VistA.wait('PATIENT NAME:')
            self.VistA.write(patient)
        else:
            self.VistA.write('MA')
            self.VistA.wait('Select CLINIC:')
            self.VistA.write(clinic)
        self.VistA.wait('TYPE:')
        self.VistA.write('Regular')
        for wwset in dgrph:
            self.VistA.wait(wwset[0])
            self.VistA.write(wwset[1])
        self.VistA.wait('REQUEST?')
        self.VistA.write('yes')
        self.VistA.wait('DATE/TIME:')
        self.VistA.write(datetime)
        rval = self.VistA.multiwait(['LENGTH OF APPOINTMENT', 'CORRECT'])
        if rval == 0:
            self.VistA.write('')
            self.VistA.wait('CORRECT')
            self.VistA.write('Yes')
        elif rval == 1:
            self.VistA.write('Yes')
        self.VistA.wait('STOPS')
        self.VistA.write('No')
        self.VistA.wait('OTHER INFO:')
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        if CLfirst is not None:
            self.VistA.wait('Select Action:')
        else:
            self.VistA.wait('Select CLINIC:')
            self.VistA.write('')
            self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')

    def fix_demographics(self, clinic, patient, dgrph,):
        ''' this is a workaround for the demographic bug in gtm'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Select Action:')
        self.VistA.write('PD')
        for wwset in dgrph:
            self.VistA.wait(wwset[0])
            self.VistA.write(wwset[1])

    def set_demographics(self, clinic, patient, dgrph, CLfirst=None, patidx=None):
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        if CLfirst is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('CL')
            self.VistA.wait('Select Clinic:')
            self.VistA.write(clinic)
            self.VistA.wait('Select Action:')
            self.VistA.write('PD')
            self.VistA.wait('Select Appointments')
            self.VistA.write(patidx)
        else:
            self.VistA.wait('Select Action:')
            self.VistA.write('PD')
        for wwset in dgrph:
            self.VistA.wait(wwset[0])
            self.VistA.write(wwset[1])
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')

    def get_demographics(self, patient, vlist):
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Select Action:')
        self.VistA.write('PD')
        for wwset in vlist:
            self.VistA.wait(wwset[0])
            self.VistA.write(wwset[1])
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')


    def verapp_bypat(self, patient, vlist, ALvlist=None, EPvlist=None, COnum=None, CInum=None):
        '''Verify previous Appointment for specified user at specified time'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(patient)  # <--- by patient
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        for vitem in vlist:
            self.VistA.wait(vitem)
        if ALvlist is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('AL')
            self.VistA.wait('Select List:')
            self.VistA.write('TA')
            for vitem in ALvlist:
                self.VistA.wait(vitem)
        if EPvlist is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('EP')
            self.VistA.wait('Select Appointment(s):')
            self.VistA.write('1')
            for vitem in EPvlist:
                self.VistA.wait(vitem)
            self.VistA.wait('Select Action:')
            self.VistA.write('^')
        if COnum is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('AL')
            self.VistA.wait('Select List:')
            self.VistA.write('FU')
            self.VistA.wait('Select Action:')
            self.VistA.write('CO')
            if COnum[0] is not '1':
                self.VistA.wait('Select Appointment(s):')
                self.VistA.write(COnum[1])
            self.VistA.wait('It is too soon to check out this appointment')
            self.VistA.write('')
        if CInum is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('AL')
            self.VistA.wait('Select List:')
            self.VistA.write('FU')
            self.VistA.wait('Select Action:')
            self.VistA.write('CI')
            if CInum[0] is not '1':
                self.VistA.wait('Select Appointment(s):')
                self.VistA.write(CInum[1])
            self.VistA.wait('It is too soon to check in this appointment')
            self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')


    def verapp(self, clinic, vlist, COnum=None, CInum=None):
        '''Verify previous Appointments by clinic and with CI/CO check '''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('CD')
        self.VistA.wait('Select Beginning Date:')
        self.VistA.write('')
        self.VistA.wait('Ending Date:')
        self.VistA.write('t+100')
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        for vitem in vlist:
            self.VistA.wait(vitem)
        if COnum is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('AL')
            self.VistA.wait('Select List:')
            self.VistA.write('FU')
            self.VistA.wait('Select Action:')
            self.VistA.write('CO')
            if COnum[0] is not '1':
                self.VistA.wait('Select Appointment(s):')
                self.VistA.write(COnum[1])
            rval = self.VistA.multiwait(['It is too soon to check out this appointment',
                                         'You can not check out this appointment'])
            if rval == 0:
                self.VistA.write('')
            elif rval == 1:
                self.VistA.write('')
            else:
                self.VistA.wait('SPECIALERROR, rval: ' + str(rval))  # this should cause a timeout
        if CInum is not None:
            self.VistA.wait('Select Action:')
            self.VistA.write('AL')
            self.VistA.wait('Select List:')
            self.VistA.write('FU')
            self.VistA.wait('Select Action:')
            self.VistA.write('CI')
            if CInum[0] is not '1':
                self.VistA.wait('Select Appointment(s):')
                self.VistA.write(CInum[1])
            self.VistA.wait('It is too soon to check in this appointment')
            self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')

    def ver_actions(self, clinic, patient, PRvlist, DXvlist, CPvlist):
        ''' verify action in menu, patient must be checked out'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        # EC
        self.VistA.wait('Select Action:')
        self.VistA.write('EC')
        self.VistA.wait('Select Appointment(s)')
        self.VistA.write('2')
        self.VistA.wait('Enter RETURN to continue')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        # RT
        self.VistA.write('RT')
        for vitem in ['Chart Request', 'Fill Next Clinic Request', 'Profile of Charts', 'Recharge a Chart']:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Record Tracking Option:')
        self.VistA.write('^')
        # PR
        self.VistA.wait('Select Action:')
        self.VistA.write('PR')
        self.VistA.wait('CHOOSE 1-2:')
        self.VistA.write('1')
        self.VistA.wait('Select Appointment(s):')
        self.VistA.write('1')
        for vitem in PRvlist:
            self.VistA.wait(vitem)
        self.VistA.wait('Enter PROVIDER:')
        self.VistA.write('')
        self.VistA.wait('for this ENCOUNTER')
        self.VistA.write('')
        self.VistA.wait('Enter PROVIDER:')
        self.VistA.write('')
        # DX
        self.VistA.wait('Select Action:')
        self.VistA.write('DX')
        self.VistA.wait('Select Appointment(s):')
        self.VistA.write('1')
        for vitem in DXvlist:
            self.VistA.wait(vitem)
        self.VistA.wait('Enter Diagnosis :')
        self.VistA.write('')
        self.VistA.wait('Problem List')
        self.VistA.write('no')
        # CP
        self.VistA.wait('Select Action:')
        self.VistA.write('CP')
        self.VistA.wait('Select Appointment(s):')
        self.VistA.write('1')
        for vitem in CPvlist:
            self.VistA.wait(vitem)
        self.VistA.wait('Enter PROCEDURE')
        self.VistA.write('')
        # PC
        self.VistA.wait('Select Action:')
        self.VistA.write('PC')
        self.VistA.wait('is locked')
        self.VistA.write('')

    def use_sbar(self, clinic, patient, fresh=None):
        '''Use the space bar to get previous clinic or patient '''
        self.VistA.wait('Clinic name:')
        self.VistA.write(' ')  # spacebar to test recall
        self.VistA.wait(patient)  # check to make sure expected patient SSN is recalled
        self.VistA.write('No')
        self.VistA.wait(clinic)  # check to make sure expected clinic is recalled
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('MA')
        self.VistA.wait('Select PATIENT NAME:')
        self.VistA.write(' ')  # spacebar to test recall
        self.VistA.wait(patient)  # check to make sure expected patient SSN is recalled
        self.VistA.wait('TYPE:')
        self.VistA.write('Regular')
        if fresh is not None:
            self.VistA.wait('APPOINTMENTS:')
            self.VistA.write('Yes')
        self.VistA.wait('ETHNICITY:')
        self.VistA.write('')
        self.VistA.wait('RACE:')
        self.VistA.write('')
        self.VistA.wait('COUNTRY:')
        self.VistA.write('')
        self.VistA.wait('STREET ADDRESS')
        self.VistA.write('')
        self.VistA.wait('ZIP')
        self.VistA.write('')
        for x in range(0, 2):
            self.VistA.wait('PHONE NUMBER')
            self.VistA.write('')
        self.VistA.wait('BAD ADDRESS')
        self.VistA.write('')
        self.VistA.wait('above changes')
        self.VistA.write('No')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('REQUEST')
        self.VistA.write('Yes')
        self.VistA.wait('DATE/TIME')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')
        self.VistA.wait('')

    def canapp(self, clinic, mult=None, rebook=None, strDate=None, endDate=None):
        '''Cancel an Appointment, if there are multiple apts on schedule, send a string to the parameter "first"'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        if strDate is not None and endDate is not None:
            self.VistA.write(strDate)
            self.VistA.wait('Date:')
            self.VistA.write(endDate)
        else:
            self.VistA.write('t')
            self.VistA.wait('Date:')
            self.VistA.write('t+1')  
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        self.VistA.wait('Select Action:')
        self.VistA.write('CA')
        if mult is not None:
            # If there are more than 1 appointments
            self.VistA.wait('Select Appointment')
            self.VistA.write(mult)
        self.VistA.wait('linic:')
        self.VistA.write('Clinic')
        self.VistA.wait('REASONS NAME')
        self.VistA.write('Clinic Cancelled')
        self.VistA.wait('REMARKS:')
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        if rebook is not None:
            self.VistA.wait('CANCELLED')
            self.VistA.write('Y')
            self.VistA.wait('REBOOKED APPT(S)')
            self.VistA.write('')
            self.VistA.wait('REBOOKED:')
            self.VistA.write('1')
            self.VistA.wait('DATE:')
            self.VistA.write('')
            self.VistA.wait('continue')
            self.VistA.write('')
            self.VistA.wait('continue')
            self.VistA.write('')
            self.VistA.wait('CONTINUE')
            self.VistA.write('')
            self.VistA.wait('APPOINTMENT(S)?')
            self.VistA.write('N')
        else:                
            self.VistA.wait('CANCELLED')
            self.VistA.write('')
            self.VistA.wait('CANCELLED')
            self.VistA.write('')
        self.VistA.wait('exit:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def noshow(self, clinic, appnum=None):
        '''Registers a patient as a no show'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('NS')
        if appnum is not None:
            self.VistA.wait('Select Appointment')
            self.VistA.write(appnum)
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('NOW')
        self.VistA.write('no')
        self.VistA.wait('NOW')
        self.VistA.write('no')
        self.VistA.wait('exit:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def checkin(self, clinic, vlist, strDate=None, endDate=None, mult=None):
        '''Checks a patient in'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        if strDate is not None and endDate is not None:
            self.VistA.write(strDate)
            self.VistA.wait('Date:')
            self.VistA.write(endDate)
        else:
            self.VistA.write('t')
            self.VistA.wait('Date:')
            self.VistA.write('t')    
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        self.VistA.wait('Select Action:')
        self.VistA.write('CI')
        if mult is not None:
            self.VistA.wait('Appointment')
            self.VistA.write(mult)
        for vitem in vlist:
            self.VistA.wait(vitem)
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def checkout(self, clinic, vlist1, vlist2, icd,  strDate=None, endDate=None, mult=None):
        '''Checks a Patient out'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        if strDate is not None and endDate is not None:
            self.VistA.write(strDate)
            self.VistA.wait('Date:')
            self.VistA.write(endDate)
        else:
            self.VistA.write('t')
            self.VistA.wait('Date:')
            self.VistA.write('t')  
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        self.VistA.wait('Select Action:')
        self.VistA.write('CO')
        if mult is not None:
            self.VistA.wait('Appointment')
            self.VistA.write(mult)
        for vitem in vlist1:
            self.VistA.wait(vitem)
        self.VistA.wait('appointment')
        self.VistA.write('No')
        self.VistA.wait('date and time:')
        self.VistA.write('Now')
        self.VistA.wait('PROVIDER:')
        self.VistA.write('Alexander')
        self.VistA.wait('ENCOUNTER')
        self.VistA.write('Yes')
        self.VistA.wait('PROVIDER')
        self.VistA.write('')
        self.VistA.wait('Diagnosis')
        self.VistA.write(icd)
        self.VistA.wait('Ok')
        self.VistA.write('Yes')
        self.VistA.wait('ENCOUNTER')
        self.VistA.write('Yes')
        self.VistA.wait('Resulting:')
        self.VistA.write('R')
        for vitem in vlist2:
            self.VistA.wait(vitem)
        self.VistA.wait('Diagnosis')
        self.VistA.write('')
        self.VistA.wait('Problem List')
        self.VistA.write('No')
        self.VistA.wait('PROCEDURE')
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('screen')
        self.VistA.write('No')
        self.VistA.wait('Clinic:')
        self.VistA.write('')

    def unschvisit(self, clinic, patient, patientname):
        '''Makes a walk-in appointment. Automatically checks in'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('UN')
        self.VistA.wait('Select Patient:')
        self.VistA.write(patient)
        self.VistA.wait('TIME:')
        self.VistA.write('')
        self.VistA.wait('TYPE:')
        self.VistA.write('Regular')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('Check Out:')
        self.VistA.write('CI')
        self.VistA.wait('CHECKED-IN:')
        self.VistA.write('')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('SLIP NOW')
        self.VistA.write('No')
        self.VistA.wait(patientname)
        self.VistA.wait('Checked In')
        self.VistA.wait('Select Action')
        self.VistA.write('')

    def chgpatient(self, clinic, patient1, patient2, patientname1, patientname2):
        '''Changes the patient between patient 1 and patient 2'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('PT')
        self.VistA.wait('Patient:')
        self.VistA.write(patient1)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait(patientname1.upper())
        self.VistA.wait('Select Action:')
        self.VistA.write('PT')
        self.VistA.wait('Patient:')
        self.VistA.write(patient2)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait(patientname2.upper())
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')

    def chgclinic(self):
        '''Changes the clinic from clinic1 to clinic2'''
        self.VistA.wait('Clinic name:')
        self.VistA.write('Clinic1')
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Clinic1')
        self.VistA.wait('Select Action:')
        self.VistA.write('CL')
        self.VistA.wait('Select Clinic:')
        self.VistA.write('Clinic2')
        self.VistA.wait('Clinic2')
        self.VistA.wait('Select Action:')
        self.VistA.write('Quit')

    def chgdaterange(self, clinic):
        '''Changes the date range of the clinic'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait(clinic)
        self.VistA.wait('Select Action:')
        self.VistA.write('CD')
        self.VistA.wait('Date:')
        self.VistA.write('t+7')
        self.VistA.wait('Date:')
        self.VistA.write('t+7')
        self.VistA.wait('Select Action:')
        self.VistA.write('CD')
        self.VistA.wait('Date:')
        self.VistA.write('t-4')
        self.VistA.wait('Date:')
        self.VistA.write('t+4')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def expandentry(self, clinic, vlist1, vlist2, vlist3, vlist4, vlist5, mult=None):
        '''Expands an appointment entry for more detail'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait(clinic)
        self.VistA.wait('Select Action:')
        self.VistA.write('AL')
        self.VistA.wait('Select List:')
        self.VistA.write('TA')
        self.VistA.wait('Select Action:')
        self.VistA.write('EP')
        if mult is not None:
            self.VistA.wait('Appointment')
            self.VistA.write(mult)
        for vitem in vlist1:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Action:')
        self.VistA.write('')
        for vitem in vlist2:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Action:')
        self.VistA.write('')
        for vitem in vlist3:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Action:')
        self.VistA.write('')
        for vitem in vlist4:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Action:')
        self.VistA.write('')
        for vitem in vlist5:
            self.VistA.wait(vitem)
        self.VistA.wait('Select Action:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def addedit(self, clinic, name, icd):
        '''Functional but not complete. Exercises the Add/Edit menu but doesn't make any changes
        Same problem as checkout with the CPT codes and the MPI'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait(clinic)
        self.VistA.wait('Select Action:')
        self.VistA.write('AE')
        self.VistA.wait('Name:')
        self.VistA.write(name)
        self.VistA.wait('exit:')
        self.VistA.write('A')
        self.VistA.wait('Clinic:')
        self.VistA.write(clinic)
        self.VistA.wait('Time:')
        time = self.schtime()
        self.VistA.write(time)
        self.VistA.wait('APPOINTMENT TYPE:')
        self.VistA.write('')
        self.VistA.wait('PROVIDER:')
        self.VistA.write('Alexander')
        self.VistA.wait('ENCOUNTER')
        self.VistA.write('Yes')
        self.VistA.wait('Enter PROVIDER:')
        self.VistA.write('')
        self.VistA.wait('Diagnosis')
        self.VistA.write(icd)
        self.VistA.wait('Ok')
        self.VistA.write('Yes')
        self.VistA.wait('ENCOUNTER')
        self.VistA.write('Yes')
        self.VistA.wait('Resulting')
        self.VistA.write('R')
        self.VistA.wait('Diagnosis')
        self.VistA.write('')
        self.VistA.wait('Problem List')
        self.VistA.write('')
        self.VistA.wait('CPT CODE')
        self.VistA.write('')
        self.VistA.wait('encounter')
        self.VistA.write('Yes')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def patdem(self, clinic, name, mult=None):
        '''This edits the patients demographic information'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait(clinic)
        self.VistA.wait('Select Action:')
        self.VistA.write('PD')
        if mult is not None:
            self.VistA.wait('Appointment')
            self.VistA.write(mult)
        self.VistA.wait(name)
        self.VistA.wait('COUNTRY:')
        self.VistA.write('')
        self.VistA.wait('ADDRESS')
        self.VistA.write('')
        self.VistA.wait(':')
        self.VistA.write('')
        self.VistA.wait('PHONE NUMBER')
        self.VistA.write('')
        self.VistA.wait('PHONE NUMBER')
        self.VistA.write('')
        self.VistA.wait('INDICATOR:')
        self.VistA.write('')
        self.VistA.wait('changes')
        self.VistA.write('No')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('SEX:')
        self.VistA.write('')
        self.VistA.wait('INFORMATION')
        self.VistA.write('N')
        self.VistA.wait('INFORMATION:')
        self.VistA.write('W')
        self.VistA.wait('RACE INFORMATION')
        self.VistA.write('Yes')
        self.VistA.wait('INFORMATION:')
        self.VistA.write('')
        self.VistA.wait('STATUS:')
        self.VistA.write('Married')
        self.VistA.wait('PREFERENCE:')
        self.VistA.write('')
        self.VistA.wait('ACTIVE')
        self.VistA.write('No')
        self.VistA.wait('NUMBER')
        self.VistA.write('')
        self.VistA.wait('NUMBER')
        self.VistA.write('')
        self.VistA.wait('ADDRESS:')
        self.VistA.write('')
        self.VistA.wait('Select Action')
        self.VistA.write('')

    def teaminfo(self, clinic, patient=None):
        '''This checks the display team info feature'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('TI')
        if patient is not None:
            self.VistA.wait('Select Patient')
            self.VistA.write(patient)
        self.VistA.wait('Team Information')
        self.VistA.wait('Select Action:')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('')

    def enroll(self, clinic, patient):
        '''This enrolls a patient as an inpatient in a clinic'''
        self.VistA.wait('OPTION NAME')
        self.VistA.write('Appointment Menu')
        self.VistA.wait('Menu Option')
        self.VistA.write('Edit Clinic Enrollment Data')
        self.VistA.wait('PATIENT NAME')
        self.VistA.write(patient)
        self.VistA.wait('CLINIC:')
        self.VistA.write(clinic)
        self.VistA.wait('ENROLLMENT CLINIC')
        self.VistA.write('Yes')
        self.VistA.wait('ENROLLMENT:')
        self.VistA.write('t')
        self.VistA.wait('DATE OF ENROLLMENT')
        self.VistA.write('Yes')
        self.VistA.wait('AC:')
        self.VistA.write('OPT')
        self.VistA.wait('DATE:')
        self.VistA.write('')
        self.VistA.wait('DISCHARGE:')
        self.VistA.write('')
        self.VistA.wait('DISCHARGE')
        self.VistA.write('')
        self.VistA.wait('CLINIC:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('ENROLLMENT')
        self.VistA.write('')
        self.VistA.wait('ENROLLMENT')
        self.VistA.write('')
        self.VistA.wait('AC:')
        self.VistA.write('')
        self.VistA.wait('DATE:')
        self.VistA.write('')
        self.VistA.wait('DISCHARGE')
        self.VistA.write('')
        self.VistA.wait('DISCHARGE')
        self.VistA.write('')
        self.VistA.wait('CLINIC')
        self.VistA.write('')
        self.VistA.wait('NAME:')
        self.VistA.write('')
        self.VistA.wait('Menu Option:')
        self.VistA.write('')
        self.VistA.wait('halt')
        self.VistA.write('')

    def discharge(self, clinic, patient, appnum=None):
        '''Discharges a patient from the clinic'''
        self.VistA.wait('Clinic name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Select Action:')
        self.VistA.write('DC')
        if appnum is not None:
            self.VistA.wait('Select Appointment')
            self.VistA.write(appnum)
        self.VistA.wait('Discharging patient from')
        self.VistA.wait('DATE OF DISCHARGE:')
        self.VistA.write('t')
        self.VistA.wait('REASON FOR DISCHARGE')
        self.VistA.write('testing')
        self.VistA.wait('Action:')
        self.VistA.write('')

    def deletecheckout(self, clinic, appnum=None):
        '''Deletes checkout from the menu
        Must be signed in as fakedoc1 (1Doc!@#$)
        Must have the SD SUPERVISOR Key assigned to Dr. Alexander'''
        self.VistA.wait('Menu Option:')
        self.VistA.write('Appointment Menu')
        self.VistA.wait('Menu Option:')
        self.VistA.write('Appointment Management')
        self.VistA.wait('Clinic name')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Action:')
        self.VistA.write('DE')
        if appnum is not None:
            self.VistA.wait('Select Appointment')
            self.VistA.write(appnum)
        self.VistA.wait('check out')
        self.VistA.write('Yes')
        self.VistA.wait('deleting')
        self.VistA.wait('continue:')
        self.VistA.write('')
        self.VistA.wait('deleting check out')
        self.VistA.wait('exit:')
        self.VistA.write('')
        self.VistA.wait('Action:')
        self.VistA.write('')

    def waitlistentry(self, clinic, patient):
        '''Enters a patient into the wait list
        This assumes that SDWL PARAMETER and SDWL MENU
        keys are given to fakedoc1'''
        self.VistA.wait('Option:')
        self.VistA.write('Appointment Menu')
        self.VistA.wait('Option:')
        self.VistA.write('Appointment Management')
        self.VistA.wait('name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Action:')
        self.VistA.write('WE')
        self.VistA.wait('NAME:')
        self.VistA.write(patient)
        self.VistA.wait('Patient')
        self.VistA.write('Yes')
        self.VistA.wait('response:')
        # TODO: Explore all three options (PCMM TEAM ASSIGNMENT, SERVICE/SPECIALTY, SPECIFIC CLINIC
        self.VistA.write('1')
        self.VistA.wait('Institution:')
        self.VistA.write('1327')
        self.VistA.wait('OK')
        self.VistA.write('Yes')
        self.VistA.wait('Team:')
        self.VistA.write('1')
        self.VistA.wait('OK')
        self.VistA.write('yes')
        self.VistA.wait('Comments:')
        self.VistA.write('test')
        self.VistA.wait('Action:')
        self.VistA.write('')

    def waitlistdisposition(self, clinic, patient):
        '''This verifies that the wait list disposition option is working'''
        self.VistA.wait('Option:')
        self.VistA.write('Appointment Management')
        self.VistA.wait('name:')
        self.VistA.write(clinic)
        self.VistA.wait('OK')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('')
        self.VistA.wait('Date:')
        self.VistA.write('t+1')
        self.VistA.wait('Action:')
        self.VistA.write('WD')
        self.VistA.wait('PATIENT:')
        self.VistA.write(patient)
        self.VistA.wait('Quit')
        self.VistA.write('Yes')
        # TODO: For deeper coverage, execute all 6 disposition reasons
        self.VistA.wait('response:')
        self.VistA.write('D')
        self.VistA.wait('removed from Wait List')
        self.VistA.wait('exit:')
        self.VistA.write('')
        self.VistA.wait('no Wait List')
        self.VistA.write('')
        self.VistA.wait('Select Action:')
        self.VistA.write('')
