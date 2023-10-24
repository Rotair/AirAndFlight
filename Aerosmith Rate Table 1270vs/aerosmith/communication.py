

response_terminator = b'/r/n/>/r/n'

query_prefix = b'?'

import serial

class Communication:

    def __init__(self, serial : serial.Serial):
       
        self.s = serial

    def send(self, command, value):

        data = str(command) + str(value)
        
        b = self.s.write(data.encode())

        if b > 0 :
            try:
                response = self.s.read_until(expected=response_terminator)
            except serial.SerialTimeoutException:
                print("Timeout Occured")
                exit(1)
            
            if response == response_terminator:
                return True

        return False
    
    # Requests and returns a response in bytes
    def request(self, command):
        
        self.s.write(command + query_prefix)
        
        try:
            response = self.s.read_until(expected=response_terminator)
        except serial.SerialTimeoutException:
            print("Timeout Occured")
            exit(1)
            
        if len(response_terminator) > len(response):
             
            data_length = response - response_terminator

            data = response[:data_length]
            # Data will always be in the form data + response_terminator.
            # Data is always encoded into UTF8. 
            return data.decode()
        
            
        return False