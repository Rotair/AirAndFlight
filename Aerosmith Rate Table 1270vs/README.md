

## Rate Table Overview
The rate table operates with 1 axis of rotation in order to test rate gyros on aircraft. 

The 1270VS is equipped with RS-232 in order to serially command the table to rotate in units of degrees/second.

### Install and Run
Create the Virtual environment in the directory 

    python -m venv /path/to/new/virtual/environment

Activate your environment; One windows runs 

    ./scripts/activate

Install dependencies by running the following

    pip install -r requirements.txt

### Testing

For testing we need a virtual COM port. For windows we use 

python -m unittest test

python -m unittest discover

### Hardware Requirements
You will need an RS 232 to USB converter. There are plenty of brands to choose from however it important to consider the chip that will be doing the conversion. FTDI makes all an all-in-one package and has readily available drivers.

#### Installing the Drivers
If you have a cable with an FTDI chip you can readily plug the cable in and have windows Auto-Configure your drivers. If you drivers do not auto install , then download and install [here](https://ftdichip.com/drivers/vcp-drivers/)

### Configuration 

Host communication is established with the controller through the RS-232 port. It is a three-wire asynchronous serial interface with hard wired Clear To Send (CTS) and Data Terminal Ready (DTR). The controller is configured as DCE. Listed below are the communication parameters. 

 * Baud Rate 9600 
 * Stop Bits 1 
 * Parity None 
 * Data Bits 8



### Details
Serial Communication relies on PySerial 

pip install pip-tools

