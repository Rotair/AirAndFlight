import unittest
import serial
import unittest.mock as mock

from aerosmith.commands import RateTableCommandFactory, ACLCommands

PORT = 'loop://'

timeout = 1
# Response of valid command when no data is requested
response_terminator = b'/r/n/>/r/n'



class TestSetJog(unittest.TestCase):
    def setUp(self):
        self.s = serial.serial_for_url(PORT, timeout=timeout)
        self.rate_table = RateTableCommandFactory(self.s)

    def test_valid_response(self):
        print(ACLCommands.JOG)
        jog_acl = self.rate_table.command(ACLCommands.JOG)

    with mock.patch.object(Base, 'assignment', {'bucket': 'head'})
        jog_acl.data = 60

        # Write a successfuly response
        # self.s.write(response_terminator)

        expected_response = b'JOG60'

        response = self.s.read(5)
 
        self.assertEqual(response, expected_response)