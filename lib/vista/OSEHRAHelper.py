r"""Class to Connect to a VistA EHR automatically."""
#---------------------------------------------------------------------------
# Copyright 2012 The Open Source Electronic Health Record Agent
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------
import sys
import os
import telnetlib
import TestHelper
import time
import re
import logging
import paramiko

filedir = os.path.dirname(os.path.abspath(__file__))
pexpectdir = os.path.normpath(os.path.join(filedir, "../pexpect/"))
paramikoedir = os.path.normpath(os.path.join(filedir, "../"))
sys.path.append(pexpectdir)
sys.path.append(paramikoedir)
try:
  import pexpect
  no_pexpect = None
except ImportError, no_pexpect:
  pass

#---------------------------------------------------------------------------
# Initial Global Variables to use over the course of connecting

# connection=False
# log =False

#---------------------------------------------------------------------------
class PROMPT(object):
  """Wait for a VISTA> prompt in current namespace."""

class ConnectMUMPS(object):

  def ZN(self, namespace):
    self.wait('>')
    self.write('ZN "' + namespace + '"')
    self.namespace = namespace
    self.prompt = self.namespace + '>'

  def login(self, username, password):
    self.wait('Username:')
    self.write(username)
    self.wait('Password')
    self.write(password)

  def getenv(self, volume):
    self.write('D GETENV^%ZOSV W Y')
    if sys.platform == 'win32':
      match = self.wait_re([volume + ':[0-9A-Za-z-]+'], None)
      test = match[1].span()
      VistAboxvol = ''
      for i in range(test[0], test[1]):
        VistAboxvol = VistAboxvol + match[2][i]
      self.boxvol = VistAboxvol
    else:
      self.wait_re(volume + ':[0-9A-Za-z-]+', None)
      self.boxvol = self.connection.after

  def IEN(self, file, objectname):
    self.write('S DUZ=1 D Q^DI')
    self.wait('OPTION')
    self.write('5')
    self.wait('FILE:')
    self.write(file)
    self.wait(file + ' NAME')
    self.write(objectname + '\r')
    self.wait('CAPTIONED OUTPUT?')
    self.write('N')
    self.wait('PRINT FIELD')
    self.write('NUMBER\r')
    self.wait('Heading')
    self.write('')
    self.wait('DEVICE')
    if sys.platform == 'win32':
      self.write('\r')
      match = self.wait_re(['\r\n[0-9]+'], None)
      test = match[1].span()
      number = ''
      for i in range(test[0], test[1]):
        number = number + match[2][i]
      number = number.lstrip('\r\n')
      self.IENumber = number
    else:
      self.write('')
      self.wait_re(['\n[0-9]+'], None)
      number = self.connection.after
      number = number.lstrip('\r\n')
      self.IENumber = number
    self.write('')

class ConnectWinCache(ConnectMUMPS):
  def __init__(self, logfile, instance, namespace, location='127.0.0.1'):
    super(ConnectMUMPS, self).__init__()
    self.connection = telnetlib.Telnet(location, 23)
    if len(namespace) == 0:
      namespace = 'VISTA'
    self.namespace = namespace
    self.prompt = self.namespace + '>'
    self.log = file(logfile, 'w')
    self.type = 'cache'

  def write(self, command):
    self.connection.write(command + '\r')
    logging.debug('connection.write:' + command)

  def wait(self, command, tout=15):
    if command is PROMPT:
      command = self.namespace + '>'
    rbuf = self.connection.read_until(command, tout)
    if rbuf.find(command) == -1:
        self.log.write('ERROR: expected: ' + command + 'actual: ' + rbuf)
        logging.debug('ERROR: expected: ' + command + 'actual: ' + rbuf)
        raise TestHelper.TestError('ERROR: expected: ' + command + 'actual: ' + rbuf)
    else:
        self.log.write(rbuf)
        logging.debug(rbuf)
        return 1

  def wait_re(self, command, timeout=30):
    if command is PROMPT:
      command = self.prompt
    output = self.connection.expect(command, None)
    self.match = output[1]
    self.before = output[2]
    if output[0] == -1 and output[1] == None:
      raise Exception("Timed out")
    if output[2]:
      self.log.write(output[2])
      self.log.flush()
      return output

  def multiwait(self, options, tout=15):
    if isinstance(options, list):
      index = self.connection.expect(options)
      if index == -1:
        logging.debug('ERROR: expected: ' + str(options))
        raise TestHelper.TestError('ERROR: expected: ' + options)
      self.log.write(index[2])
      return index[0]
    else:
      raise IndexError('Input to multiwait function is not a list')

  def startCoverage(self, routines=['*']):
    self.write('D ^%SYS.MONLBL')
    rval = self.multiwait(['Stop Monitor', 'Start Monitor'])
    if rval == 0:
        self.write('1')
        self.wait('Start Monitor')
        self.write('1')
    elif rval == 1:
        self.write('1')
    else:
        raise TestHelper.TestError('ERROR starting monitor, rbuf: ' + rval)
    for routine in routines:
        self.wait('Routine Name')
        self.write(routine)
    self.wait('Routine Name', tout=60)
    self.write('')
    self.wait('choice')
    self.write('2')
    self.wait('choice')
    self.write('1')
    self.wait('continue')
    self.write('\r')

  def stopCoverage(self, path):
    newpath, filename = os.path.split(path)
    self.write('D ^%SYS.MONLBL')
    self.wait('choice')
    self.write('6')
    self.wait('Routine number')
    self.write('*')
    self.wait('FileName')
    self.write(newpath + '/Coverage/' + filename.replace('.log', '.cmcov').replace('.txt', '.cmcov'))
    self.wait('continue')
    self.write('')
    self.wait('choice')
    self.write('1\r')

class ConnectLinuxCache(ConnectMUMPS):
  def __init__(self, logfile, instance, namespace, location='127.0.0.1'):
    super(ConnectMUMPS, self).__init__()
    self.connection = pexpect.spawn('ccontrol session ' + instance + ' -U ' + namespace, timeout=None)
    if len(namespace) == 0:
      namespace = 'VISTA'
    self.namespace = namespace
    self.prompt = self.namespace + '>'
    self.connection.logfile_read = file(logfile, 'w')
    self.type = 'cache'

  def write(self, command):
    self.connection.send(command + '\r')

  def wait(self, command, tout=15):
    if command is PROMPT:
      command = self.namespace + '>'
    rbuf = self.connection.expect_exact(command, tout)
    if rbuf == -1:
        logging.debug('ERROR: expected: ' + command)
        raise TestHelper.TestError('ERROR: expected: ' + command)
    else:
        return 1

  def wait_re(self, command, timeout=15):
    if not timeout: timeout = -1
    self.connection.expect(command, timeout)

  def multiwait(self, options, tout=15):
    if isinstance(options, list):
      index = self.connection.expect(options)
      if index == -1:
        logging.debug('ERROR: expected: ' + str(options))
        raise TestHelper.TestError('ERROR: expected: ' + options)
      self.connection.logfile_read.write(options[index])
      return index
    else:
      raise IndexError('Input to multiwait function is not a list')

  def startCoverage(self, routines=['*']):
    self.write('D ^%SYS.MONLBL')
    rval = self.multiwait(['Stop Monitor', 'Start Monitor'])
    if rval == 0:
        self.write('1')
        self.wait('Start Monitor')
        self.write('1')
    elif rval == 1:
        self.write('1')
    else:
        raise TestHelper.TestError('ERROR starting monitor, rbuf: ' + rval)
    for routine in routines:
        self.wait('Routine Name')
        self.write(routine)
    self.wait('Routine Name', tout=60)
    self.write('')
    self.wait('choice')
    self.write('2')
    self.wait('choice')
    self.write('1')
    self.wait('continue')
    self.write('\r')

  def stopCoverage(self, path):
    newpath, filename = os.path.split(path)
    self.write('D ^%SYS.MONLBL')
    self.wait('choice')
    self.write('6')
    self.wait('Routine number')
    self.write('*')
    self.wait('FileName')
    self.write(newpath + '/Coverage/' + filename.replace('.log', '.cmcov').replace('.txt', '.cmcov'))
    self.wait('continue')
    self.write('')
    self.wait('choice')
    self.write('1\r')

class ConnectLinuxGTM(ConnectMUMPS):
  def __init__(self, logfile, instance, namespace, location='127.0.0.1'):
    super(ConnectMUMPS, self).__init__()
    self.connection = pexpect.spawn('gtm', timeout=None)
    if len(namespace) == 0:
        self.prompt = os.getenv("gtm_prompt")
        if self.prompt == None:
          self.prompt = "GTM>"
    self.connection.logfile_read = file(logfile, 'w')
    self.type = 'GTM'

  def write(self, command):
    self.connection.send(command + '\r')
    logging.debug('WRITE: ' + command)

  def wait(self, command, tout=15):
    if command is PROMPT:
      command = self.prompt
    rbuf = self.connection.expect_exact(command, tout)
    logging.debug('RECEIVED: ' + command)
    if rbuf == -1:
        logging.debug('ERROR: expected: ' + command)
        raise TestHelper.TestError('ERROR: expected: ' + command)
    else:
        return 1

  def wait_re(self, command, timeout=None):
    if not timeout: timeout = -1
    self.connection.expect(command, timeout)

  def multiwait(self, options, tout=15):
    if isinstance(options, list):
      index = self.connection.expect(options)
      if index == -1:
        logging.debug('ERROR: expected: ' + str(options))
        raise TestHelper.TestError('ERROR: expected: ' + options)
      self.connection.logfile_read.write(options[index])
      return index
    else:
      raise IndexError('Input to multiwait function is not a list')

  def startCoverage(self, routines=['*']):
    self.write('K ^ZZCOVERAGE VIEW "TRACE":1:"^ZZCOVERAGE"')

  def stopCoverage(self, path):
    path, filename = os.path.split(path)
    self.write('VIEW "TRACE":0:"^ZZCOVERAGE"')
    self.wait(PROMPT)
    self.write('D ^%GO')
    self.wait('Global')
    self.write('ZZCOVERAGE')
    self.wait('Global')
    self.write('')
    self.wait('Label:')
    self.write('')
    self.wait('Format')
    self.write('ZWR')
    self.wait('device')
    self.write(path + '/Coverage/' + filename.replace('.log', '.mcov').replace('.txt', '.mcov'))

class ConnectRemoteSSH(ConnectMUMPS):
  """
  This will provide a connection to VistA via SSH. This class handles any
  remote system (ie: currently there are not multiple versions of it for each
  remote OS).
  """

  def __init__(self, logfile, instance, namespace, location, remote_conn_details):
    super(ConnectMUMPS, self).__init__()

    self.type = str.lower(instance)
    self.namespace = str.upper(namespace)
    self.prompt = self.namespace + '>'

    # Create a new SSH client object
    client = paramiko.SSHClient()

    # Set SSH key parameters to auto accept unknown hosts
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the host
    client.connect(hostname=remote_conn_details.remote_address, username=remote_conn_details.username, password=remote_conn_details.password)

    # Create a client interaction class which will interact with the host
    from paramikoe import SSHClientInteraction
    interact = SSHClientInteraction(client, timeout=10, display=False)
    self.connection = interact
    self.connection.logfile_read = file(logfile, 'w')
    self.client = client  # apparently there is a deconstructor which disconnects (probably sends a FYN packet) when client is gone

  def write(self, command):
    time.sleep(.01)
    logging.debug('connection.send:' + command)
    self.connection.send(command + '\r')

  def wait(self, command, tout=15):
    time.sleep(.01)
    logging.debug('connection.expect: ' + str(command))

    if command is PROMPT:
      command = self.namespace + '>'
    else:
      command = self.escapeSpecialChars(command)
      if command == '':
        command = '.*'  # fix for paramiko expect, it does not work with wait('')

    rbuf = self.connection.expect(command, tout)
    if rbuf == -1:
        logging.debug('ERROR: expected: ' + command)
        print 'ERROR: expected: ' + command
        raise TestHelper.TestError('ERROR: expected: ' + command)
    else:
        return 1

  def multiwait(self, options, tout=15):
    logging.debug('connection.expect: ' + str(options))

    temp_options = []
    for command in options:
        temp_options.append(self.escapeSpecialChars(command))
    options = temp_options

    time.sleep(.01)
    if isinstance(options, list):
      index = self.connection.expect(options, timeout=tout)
      if index == -1:
        logging.debug('ERROR: expected: ' + str(options))
        raise TestHelper.TestError('ERROR: expected: ' + str(options))
      return index
    else:
      raise IndexError('Input to multiwait function is not a list')

  def startCoverage(self, routines=['*']):
    if self.type == 'cache':
        self.write('D ^%SYS.MONLBL')
    	rval = self.multiwait(['Stop Monitor', 'Start Monitor'])
    	if rval == 0:
        	self.write('1')
        	self.wait('Start Monitor')
        	self.write('1')
    	elif rval == 1:
        	self.write('1')
    	else:
        	raise TestHelper.TestError('ERROR starting monitor, rbuf: ' + rval)
        for routine in routines:
            self.wait('Routine Name')
            self.write(routine)
        self.wait('Routine Name', tout=60)
        self.write('')
        self.wait('choice')
        self.write('2')
        self.wait('choice')
        self.write('1')
        self.wait('continue')
        self.write('\r')
    else:
        self.write('K ^ZZCOVERAGE VIEW "TRACE":1:"^ZZCOVERAGE"')

  def stopCoverage(self, path):
    if self.type == 'cache':
        newpath, filename = os.path.split(path)
        self.write('D ^%SYS.MONLBL')
        self.wait('choice')
        self.write('5')
        self.wait('summary')
        self.write('Y')
        self.wait('FileName')
        self.write(newpath + '/' + filename.replace('.log', '.cmcov'))
        self.wait('continue')
        self.write('')
        self.wait('choice')
        self.write('1\r')
    else:
        path, filename = os.path.split(path)
        self.write('VIEW "TRACE":0:"^ZZCOVERAGE"')
        self.wait(PROMPT)
        self.write('D ^%GO')
        self.wait('Global')
        self.write('ZZCOVERAGE')
        self.wait('Global')
        self.write('')
        self.wait('Label:')
        self.write('')
        self.wait('Format')
        self.write('ZWR')
        self.wait('device')
        self.write(path + '/' + filename.replace('.log', '.mcov'))

  """
  Added to convert regex's into regular string matching. It replaces special
  characters such as '?' into '\?'
  """
  def escapeSpecialChars(self, string):
    re_chars = '?*.+-|^$\()[]{}'
    escaped_str = ''
    for c in string:
        if c in re_chars:
            escaped_str = escaped_str + '\\'
        escaped_str += c
    return escaped_str
def ConnectToMUMPS(logfile, instance='CACHE', namespace='VISTA', location='127.0.0.1', remote_conn_details=None):

    # self.namespace = namespace
    # self.location = location
    # print "You are using " + sys.platform
    # remote connections
    if remote_conn_details is not None:
        return ConnectRemoteSSH(logfile, instance, namespace, location, remote_conn_details)

    # local connections
    if sys.platform == 'win32':
      return ConnectWinCache(logfile, instance, namespace, location)
    elif sys.platform == 'linux2':
      if no_pexpect:
        raise no_pexpect
      try:
        return ConnectLinuxCache(logfile, instance, namespace, location)
      except pexpect.ExceptionPexpect, no_cache:
        pass
      try:
        return ConnectLinuxGTM(logfile, instance, namespace, location)
      except pexpect.ExceptionPexpect, no_gtm:
         if (no_cache and no_gtm):
           raise "Cannot find a MUMPS instance"
