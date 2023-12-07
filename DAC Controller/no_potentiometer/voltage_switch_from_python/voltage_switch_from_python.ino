#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac;

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  dac.begin(0x60); // The I2C address of the MCP4725 is 0x60 (default)
}

void loop() {
  if (Serial.available() > 0) {
    float voltage = Serial.parseFloat();
    setDACVoltage(voltage);
  }
}

void setDACVoltage(float voltage) {
  // Update the voltage reference to 5V
  uint16_t dacValue = (voltage * 4095.0) / 5.0;

  if (dacValue > 4095) {
    dacValue = 4095;
  }

  dac.setVoltage(dacValue, false);
  Serial.print("Voltage updated to ");
  Serial.print((voltage / 1.085));
  Serial.println(" V.");
}
