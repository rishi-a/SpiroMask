#include "LowPower.h"
#include <arm_math.h>

#include <PDM.h>

#include <ArduinoBLE.h>

const int VERSION = 0x00000001;
const float TEMPERATURE_CALIBRATION = -5.0;
unsigned long currentTime;

#define SCIENCE_KIT_UUID(val) ("555a0002-" val "-467a-9538-01f0652c74e8")
#define RESISTANCE_PIN A0
#define VOLTAGE_BUFFER_SIZE 16

//#define DEBUG 0

BLEService                     service                    (SCIENCE_KIT_UUID("0000"));
BLEUnsignedIntCharacteristic   versionCharacteristic      (SCIENCE_KIT_UUID("0001"), BLERead);
BLEUnsignedShortCharacteristic soundPressureCharacteristic(SCIENCE_KIT_UUID("0019"), BLENotify);

byte voltageBufferIndex = 0;
bool voltageBufferFilled = false;
short soundSampleBuffer[256];
short voltageSampleBuffer[VOLTAGE_BUFFER_SIZE];

void onPDMdata() {
  // query the number of bytes available
  int bytesAvailable = PDM.available();

  // read into the sample buffer
  PDM.read(soundSampleBuffer, bytesAvailable);
}

uint16_t getSoundAverage() {
  uint32_t avg = 0;
  for (int i = 0; i < sizeof(soundSampleBuffer)/sizeof(soundSampleBuffer[0]); i++) {
    avg += soundSampleBuffer[i]*soundSampleBuffer[i];
  }
  return sqrt(avg);
}


// String to calculate the local and device name
String name;
unsigned long lastNotify = 0;

void printSerialMsg(const char * msg) {
  #ifdef DEBUG
  if (Serial) {
    Serial.println(msg);
  }
  #endif
}

void blinkLoop() {
  while (1) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
  }
}

void setup() {
  #ifdef DEBUG
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");
  #endif

  delay(2000);

 
  PDM.onReceive(onPDMdata);
  if (!PDM.begin(1, 16000)) {
    printSerialMsg("Failed to start PDM!");
    blinkLoop();
  }

  if (!BLE.begin()) {
    printSerialMsg("Failed to initialized BLE!");
    blinkLoop();
  }

  String address = BLE.address();
  #ifdef DEBUG
  if (Serial) {
    Serial.print("address = ");
    Serial.println(address);
  }
  #endif
  address.toUpperCase();

  name = "BLE Sense - ";
  name += address[address.length() - 5];
  name += address[address.length() - 4];
  name += address[address.length() - 2];
  name += address[address.length() - 1];

  #ifdef DEBUG
  if (Serial) {
    Serial.print("name = ");
    Serial.println(name);
  }
  #endif

  //BLE.setLocalName(name.c_str());
  BLE.setLocalName("BLE Sense - 45CF");
  BLE.setDeviceName(name.c_str());
  BLE.setAdvertisedService(service);

  service.addCharacteristic(versionCharacteristic);
  service.addCharacteristic(soundPressureCharacteristic);
  
  versionCharacteristic.setValue(VERSION);

  BLE.addService(service);
  BLE.advertise();

  lowPower();
}

void loop() {
  currentTime = millis(); 
  BLE.poll(10000);
  while (BLE.connected()) {
    lowPowerBleWait(100); //does this mean that in one second we have 10 data point?
    updateSubscribedCharacteristics();

    if((millis()-currentTime)>60000){
      //NRF_POWER->SYSTEMOFF = 1;
      delay(60*1000); //sleep for a minute 
      //BLE.end();      //does not make any difference, so its better to keep the connection on
      //lowPowerWait(60*1000);
      currentTime = millis(); //get the current time
    }
  }
}

void updateSubscribedCharacteristics() {
  if (soundPressureCharacteristic.subscribed()) {
    uint16_t sound = getSoundAverage();
    soundPressureCharacteristic.writeValue(sound);
  }
}
