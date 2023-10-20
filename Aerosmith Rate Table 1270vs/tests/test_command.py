import unittest
import serial

PORT = 'loop://'

timeout = 1
# Response of valid command when no data is requested
response_terminator = b'/r/n/>/r/n'

class TestRecieve(unittest.TestCase):
    def setUp(self):
        self.s = serial.serial_for_url(PORT, timeout=timeout)
        

    def test_valid_response(self):
        self.s.write(response_terminator + b'sssss')
        response = self.s.read_until(expected=response_terminator)
        self.assertEqual(response_terminator, response)
