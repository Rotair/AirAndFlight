import unittest
import serial
import unittest.mock as mock
from unittest.mock import patch

from aerosmith.communication import Communication
from aerosmith.commands import RateTableCommandFactory, ACLCommands, Command, InvalidArugment

PORT = 'loop://'

timeout = 1
# Response of valid command when no data is requested
response_terminator = b'/r/n/>/r/n'


class TestSetJog(unittest.TestCase):
    def setUp(self):
        self.s = serial.serial_for_url(PORT, timeout=timeout)
        self.rate_table = RateTableCommandFactory(self.s)

    def test_valid_response(self):
            jog_acl = self.rate_table.command(ACLCommands.JOG)

            # Removes the need to wait for the response terminator
            with mock.patch.object(self.s, 'read_until', return_value=0):
                jog_acl.data = 60

            response = self.s.read(5)
          
            expected_response = b'JOG60'
    
            self.assertEqual(expected_response, response)

    def test_set_jog_high(self):
        jog_acl = self.rate_table.command(ACLCommands.JOG)

        with self.assertRaises(InvalidArugment) as context:
            jog_acl.data = 361
