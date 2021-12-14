/*
This code interfaces CCS811 with Adafruit Feather MO Adalogger.
Logs both TVOC ad eCO2 data to an SD card.

Compiled by Rishiraj Adhikary at https://rishi-a.github.io

*/
#include <SPI.h>
#include <SD.h>
#include "Adafruit_CCS811.h"
Adafruit_CCS811 ccs;

//for sd card
const int chipSelect = 4;
const int writeIndicator = 8;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  //while (!Serial) {
   // ; // wait for serial port to connect. Needed for native USB port only
  //}
  Serial.println("CCS811 test");
  Serial.print("Initializing SD card...");
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(writeIndicator, OUTPUT);

  if(!ccs.begin()){
    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(writeIndicator, LOW); 
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }
  // Wait for the sensor to be ready
  while(!ccs.available());

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
}

void loop() {
  digitalWrite(writeIndicator, LOW); 
  // make a string for assembling the data to log:
  String dataString = "";
  if(ccs.available()){
    if(!ccs.readData()){
        float eCO2 = ccs.geteCO2();
        dataString += String(eCO2);
        float TVOC = ccs.getTVOC();
        dataString += ",";
        dataString += String(TVOC);
      }
  }
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Serial.println(dataString); 
    digitalWrite(writeIndicator, HIGH); 
    
  }
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
    digitalWrite(writeIndicator, LOW);
  }
  delay(1000);
}
