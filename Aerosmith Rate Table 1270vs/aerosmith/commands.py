
#  Ideal Aerosmith Table Language
#  Action Commands have a Parameter Type and Limit, they will always return AeroSmith's Response terminator
#  
#  Query Commands are denoted by the use of a ? after the command and have a return Type 


# Each Command has a following Tuple
# (Command Name,  Request Type , Query Return Type, Lower, Upper)
import enum

import serial

from aerosmith.communication import Communication

class InvalidArugment(Exception):
    pass

class SendFailed(Exception):
    pass

class Command:
    upper : None | float | int
    lower : None | float | int
    _data : None
    command_id : str
    communication : Communication = None

    def validate(self, value):

        # Wrong data type is given
        if self.datatype is not None and not isinstance(value, self.datatype):
            raise InvalidArugment("Invalid data type for command")
        
        #  No Limits, no need to validate
        if self.upper is None or self.lower is None:
            return True
        
        # Check if value is within limits
        if value <= self.upper and value >= self.lower:
            return True
        
        return False
        

        
    
    def __init__(self, id, datatype=None, lower=None, upper=None, units : str = None):
        self.command_id = id
        self.lower = lower
        self.upper = upper
        self.units = units
        self.datatype = datatype
    
    @property
    def data(self):
        return self.request(self.command_id)
    
    @data.setter
    def data(self, value):
        if not self.validate(value):
            raise InvalidArugment("Command not within device limits")

        if not self.communication.send(self.command_id, value):
            raise SendFailed('Command failed to send')
    
    def send(self, data):
        return self.communication.send(self.command_id, data)

    def request(self):
        return self.communication.request(self.command_id)


class ACLCommands(str, enum.Enum):
    HOME = 'HOM'
    ACCELERATION = 'ACL'
    CALIBRATION = 'CAL'
    CLUTCH = 'CLU'
    JOG = 'JOG'
    REX = 'REX'
    MOTOR = 'SRV'
    STOP = 'STO'

    def __str__(self) -> str:
            return self.value


commands =  {
    ACLCommands.ACCELERATION : Command(ACLCommands.ACCELERATION, float),
    ACLCommands.HOME : Command(ACLCommands.HOME),
    ACLCommands.CALIBRATION : Command(ACLCommands.CALIBRATION),
    ACLCommands.CLUTCH : Command(ACLCommands.CLUTCH, int, 1, 5),
    # 1-21600 Deg/Min, bi-directional 360 degrees per second Negative units represent Counter Clockwise
    ACLCommands.JOG : Command(ACLCommands.JOG, int, -360, 360),
    ACLCommands.MOTOR: Command(ACLCommands.MOTOR, 0, 1, int),
    ACLCommands.STOP : Command(ACLCommands.STOP)
}


class RateTableCommandFactory():

    def __init__(self, serial):
        Command.communication = Communication(serial)

    def command(self, command_id):
        return commands[command_id]
