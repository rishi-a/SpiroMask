/*
This code interfaces CCS811 with Adafruit Feather MO Adalogger.
Logs both TVOC ad eCO2 data to an SD card.

Compiled by Rishiraj Adhikary at https://rishi-a.github.io

*/
#include <SPI.h>
#include <SD.h>
#include "Adafruit_CCS811.h"
#include <arduinoFFT.h> //for the Fourier transform
#define SAMPLES 64 //Must be a power of 2
#define SAMPLING_FREQUENCY 1
Adafruit_CCS811 ccs;




arduinoFFT FFT = arduinoFFT();
volatile int samplesRead;
double vReal[SAMPLES];
double vImag[SAMPLES];

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
}

void loop() {
  digitalWrite(writeIndicator, LOW);
  float eCO2; 
  // make a string for assembling the data to log:
  String dataString = "";
  if(ccs.available()){
    for (int i = 0; i < SAMPLES; i++) {
      if(!ccs.readData()){
        eCO2 = ccs.geteCO2();
        vReal[i] = eCO2;
        vImag[i] = 0;
        delay(1000);
      }
    }
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
    double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
    Serial.println(peak);    
  }
}
