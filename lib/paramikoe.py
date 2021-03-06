#
# Paramiko Expect
#
# Written by Fotis Gimian
# http://github.com/fgimian
#
# This library works with a Paramiko SSH channel to provide native SSH
# expect-like handling for servers.  The library may be used to interact
# with commands like 'configure' or Cisco IOS devices or with interactive
# Unix scripts or commands.
#
# You must have Paramiko installed in order to use this library.
#
import sys
import re
import types

class SSHClientInteraction:
    """This class allows an expect-like interface to Paramiko which allows coders
    to interact with applications and the shell of the connected device."""

    def __init__(self, client, timeout=60, newline='\r', buffer_size=1024, display=False):
        """The constructor for our SSHClientInteraction class.

        Arguments:
        client -- A Paramiko SSHClient object

        Keyword arguments:
        timeout -- THe connection timeout in seconds
        newline -- The newline character to send after each command
        buffer_size -- The amount of data (in bytes) that will be read at a time
                       after a command is run
        display -- Whether or not the output should be displayed in real-time as
                   it is being performed (especially useful when debugging)

        """
        self.channel = client.invoke_shell()
        self.newline = newline
        self.buffer_size = buffer_size
        self.display = display
        self.timeout = timeout
        self.current_output = ''
        self.current_output_clean = ''
        self.current_send_string = ''
        self.last_match = ''
        self.logfile_read = None
        self.buf = ''

    def __del__(self):
        """The destructor for our SSHClientInteraction class."""
        self.close()  # --jspivey, commenting this out to fix bug on our side #10/5.. adding it back in

    def close(self):
        """Attempts to close the channel for clean completion"""
        try:
            self.channel.close()
        except:
            pass

    def log(self, lines):

        if self.display is False:
            return

        sys.stdout.write('#####\n')
        for line in lines:
            sys.stdout.write(__name__ + '.' + sys._getframe(1).f_code.co_name + '-- ' + line + '\n')
        sys.stdout.write('#####\n')
        sys.stdout.flush()

    # jspivey- TODO: implement timeout
    def expect(self, re_strings='', timeout=None):
        """This function takes in a regular expression (or regular expressions)
        that represent the last line of output from the server.  The function
        waits for one or more of the terms to be matched.  The regexes are matched
        using expression \n<regex>$ so you'll need to provide an easygoing regex
        such as '.*server.*' if you wish to have a fuzzy match.

        Keyword arguments:
        re_strings -- Either a regex string or list of regex strings that
                      we should expect.  If this is not specified, then
                      EOF is expected (i.e. the shell is completely closed
                      after the exit command is issued)

        Returns:
        - EOF: Returns -1
        - Regex String: When matched, returns 0
        - List of Regex Strings: Returns the index of the matched string as
                                 an integer

        """

        # Set the channel timeout
        self.channel.settimeout(self.timeout)  # jspivey-- not sure this is appropriate


        # debugging...
        self.log([])
        self.log(['Displaying previous buffer...',
                  self.current_output_clean,
                  'Current expect regex(s): ' + str(re_strings)])

        # Create an empty output buffer
        # self.current_output = '' #jspivey-- want to preserve the original buffer, but remove from it when a match is found


        # This function needs all regular expressions to be in the form of a list, so
        # if the user provided a string, let's convert it to a 1 item list.
        if len(re_strings) != 0 and type(re_strings) == types.StringType:
            re_strings = [re_strings]

        # Loop until one of the expressions is matched or loop forever if nothing is expected (usually used for exit)
        while len(re_strings) == 0 or \
              not [re_string for re_string in re_strings if re.match('.*' + re_string + '.*' , self.current_output, re.DOTALL)]:
              # not [re_string for re_string in re_strings if re.match('.*\n' + re_string + '$' , self.current_output, re.DOTALL)]:

            # Read some of the output
            buf = self.channel.recv(self.buffer_size)

            # If we have an empty buffer, then the SSH session has been closed
            if len(buf) == 0:
                break

            # Strip all ugly \r (Ctrl-M making) characters from the current read
            buf = buf.replace('\r', '')

            # Display the current buffer in realtime if requested to do so (good for
            # debugging purposes) #jspivey-- rather see the preserved buffer instead of the temp buffer
            if self.display:
                sys.stdout.write('live buffer recv: ')
                sys.stdout.write(buf)
                sys.stdout.flush()

            if self.logfile_read is not None:
                self.logfile_read.write (buf)
                self.logfile_read.flush()

            # Add the currently read buffer to the output
            self.current_output += buf

        # Grab the first pattern that was matched
        if len(re_strings) != 0:
            found_pattern = [(re_index, re_string) for re_index, re_string in enumerate(re_strings) if re.match('.*' + re_string + '.*', self.current_output, re.DOTALL)]
            # found_pattern = [(re_index, re_string) for re_index, re_string in enumerate(re_strings) if re.match('.*\n' + re_string + '$', self.current_output, re.DOTALL)]

        self.current_output_clean = self.current_output

        # Clean the output up by removing the sent command
        if len(self.current_send_string) != 0:
            self.current_output_clean = self.current_output_clean.replace(self.current_send_string + '\n', '')


        self.log(['Buffer after match found...',
                  self.current_output_clean
                ])

        # Reset the current send string to ensure that multiple expect calls don't result in bad output cleaning
        self.current_send_string = ''

        # Clean the output up by removing the expect output from the end if requested and
        # save the details of the matched pattern
        if len(re_strings) != 0:
            # jspivey-- this would be a bug because of greedy matching
            # jspivey-- is found_pattern[0][1] even correct?
            self.current_output_clean = re.sub('.*' + found_pattern[0][1], '', self.current_output_clean, 0, re.DOTALL)
            # self.current_output_clean = re.sub(found_pattern[0][1] + '$', '', self.current_output_clean)

            '''--jspivey the clean_output_buffer is old code, not even referenced...
            The real persistent output buffer is 'current_output'
            '''
            self.current_output = self.current_output_clean

            self.log(['matched pattern: ' + found_pattern[0][1],
                     'regex list index: ' + str(found_pattern[0][0]),
                     'buffer after cropping...',
                     self.current_output_clean])
            # print 'removing pattern: ' +found_pattern[0][1]
            # print 'Cropped buffer result:'
            # print self.current_output_clean
            # print '\n'
            self.last_match = found_pattern[0][1]
            return found_pattern[0][0]  # jspivey-- why return [0][0]?
        else:
            # We would socket timeout before getting here, but for good measure, let's send back a -1
            return -1

    def send(self, send_string):
        """Saves and sends the send string provided"""

        self.log(['sending command: ' + send_string])

        self.current_send_string = send_string
        self.channel.send(send_string)

    def tail(self, line_prefix=None):
        """This function takes control of an SSH channel and displays line
        by line of output as \n is recieved.  This function is specifically
        made for tail-like commands.

        Keyword arguments:
        line_prefix -- Text to append to the left of each line of output.
                       This is especially useful if you are using my
                       MultiSSH class to run tail commands over multiple
                       servers.

        """

        # Set the channel timeout to the maximum integer the server allows, setting this to None
        # Breaks the KeyboardInterrupt exception and won't allow us to Ctrl+C out of teh script
        self.channel.settimeout(sys.maxint)

        # Create an empty line buffer and a line counter
        current_line = ''
        line_counter = 0

        # Loop forever, Ctrl+C (KeyboardInterrupt) is used to break the tail
        while True:

            # Read the output one byte at a time so we can detect \n correctly
            buffer = self.channel.recv(1)

            # If we have an empty buffer, then the SSH session has been closed
            if len(buffer) == 0:
                break

            # Strip all ugly \r (Ctrl-M making) characters from the current read
            buffer = buffer.replace('\r', '')

            # Add the currently read buffer to the current line output
            current_line += buffer

            # Display the last read line in realtime when we reach a \n character
            if current_line.endswith('\n'):
                if line_counter and line_prefix:
                    sys.stdout.write(line_prefix)
                if line_counter:
                    sys.stdout.write(current_line)
                    sys.stdout.flush()
                line_counter += 1
                current_line = ''
'''
    def take_control(self):
        """This function is a better documented and touched up version of the posix_shell function
        found in the interactive.py demo script that ships with Paramiko"""

        # Get attributes of the shell you were in before going to the new one
        original_tty = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            # We must set the timeout to 0 so that we can bypass times when
            # there is no available text to receive
            self.channel.settimeout(0)

            # Loop forever until the user exits (i.e. read buffer is empty)
            while True:
                select_read, select_write, select_exception = select.select([self.channel, sys.stdin], [], [])
                # Read any output from the terminal and print it to the screen.
                # With timeout set to 0, we just can ignore times when there's nothing to receive.
                if self.channel in select_read:
                    try:
                        buffer = self.channel.recv(self.buffer_size)
                        if len(buffer) == 0:
                            break
                        sys.stdout.write(buffer)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                # Send any keyboard input to the terminal one byte at a time
                if sys.stdin in select_read:
                    buffer = sys.stdin.read(1)
                    if len(buffer) == 0:
                        break
                    self.channel.send(buffer)
        finally:
            # Restore the attributes of the shell you were in
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_tty)
'''
