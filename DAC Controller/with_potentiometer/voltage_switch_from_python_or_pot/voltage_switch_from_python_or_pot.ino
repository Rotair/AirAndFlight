#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac;
const int potPin = A0;
bool potMode = true;
const int POT_MIN_VALUE = 0;
const int POT_MAX_VALUE = 1500;
const char* DAC_ERROR_MSG = "Error: DAC Cannot be reached"

void setup() {
  Serial.begin(9600);
  dac.begin(0x60);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "POT") {
      potMode = true;
    } else {
      potMode = false;
      float voltage = command.toFloat();
      if(setDACVoltage(voltage)) {
        Serial.println(voltage, 2);
      } else {
        Serial.println(DAC_ERROR_MSG);
      }
    }
  }

  if (potMode) {
    usePotentiometer();
  }
}

bool setDACVoltage(float voltage) {
  uint16_t dacValue = (voltage * 4095.0) / 5.0;

  if (dacValue > 4095) {
    dacValue = 4095;
  }

  return dac.setVoltage(dacValue, false);
}

void usePotentiometer() {
  int potValue = analogRead(potPin);
  int linearPotValue = map(potValue, POT_MIN_VALUE, POT_MAX_VALUE, POT_MIN_VALUE, POT_MAX_VALUE);
  float voltage = (linearPotValue * 5.0) / 1023.0;

  if(!setDACVoltage(voltage)) {
    Serial.println(DAC_ERROR_MSG);
    potMode = false;
  }
}
