// This code records audio using the Adafruit I2S microphone (SPH0645LM4H) and stores raw audio data in an SD card
// Currently, the data is stored at 100 Hz, but the microphone is samples at 8kHZ.
// The code below is heavily insipired from the discussion in the GitHub repo as noted below.
// I2S code Source: https://github.com/adafruit/Adafruit_ZeroDMA/issues/12
// Author: Rishiraj Adhikary | https://rishi-a.github.io  

#include <SPI.h>
#include <SD.h>
#include <Adafruit_ZeroI2S.h>

//enable/disable the part of code that is involved with SD card actions
bool SDENABLE = 0;

//audio intake settings.
#define SAMPLERATE_HZ 8000
int32_t audiosamples = 128; //128 because 512B/4B = 32B. 512B is what we can write in one block of the SD card. 4B is the size of the variable 

// The I2S interface with the Mic using Adafruit Library.
Adafruit_ZeroI2S i2s; 


//for sd card
const int chipSelect = 4;
const int writeIndicator = 8;


void setup() {
  // Open serial communications and wait for port to open:
  // Configure serial port.
  Serial.begin(115200);
  Serial.println("Zero I2S Audio Tone Generator");

  // Initialize the I2S transmitter.
  if (!i2s.begin(I2S_32_BIT, SAMPLERATE_HZ)) {
    Serial.println("Failed to initialize I2S transmitter!");
    while (1);
  }

   // Enable receive PIN 11 for Digital Output.
  i2s.enableRx(); 
  pinMode(11, OUTPUT);

  //LED to indicate correct writing
  pinMode(writeIndicator,OUTPUT);


  if(SDENABLE){

  //check SD card status
  if(!SD.begin(chipSelect)){
    Serial.println("Card failed, or not present");  
    //don't do anything more
    while(1);
  }
  Serial.println("Card Initialised");

  }
  
  
}

void loop() {


  // This is a stereo Mic. But we'll only read from LEFT channel
  //digitalWrite(11, LOW);  

  float sound;
  int32_t left,right;
  int i;
  int sample=0;

  // Read a bunch of samples!!!
  int32_t samples[audiosamples];
  //char charSamples[audiosamples];
  
  for (int i = 0; i < audiosamples; i++) {
    i2s.read(&left, &right);
    //delay(1);  // Workaround delay to prevent oversizing the buffer
    sample = left;
    //Serial.println(sample);
    // convert to 18 bit signed
    //sample >>= 14;
    //samples[i] = abs(sample);
    Serial.println(sample);
    samples[i] = sample;
    
  }

   




  if(SDENABLE){

    //store data in SD card;
    File dataFile = SD.open("datalog.dat",FILE_WRITE);
  
    //if file is available, write to it
    if(dataFile){
      dataFile.write((const uint8_t *)&samples, sizeof(samples));
      dataFile.close();
      digitalWrite(writeIndicator, HIGH);  
    }

  }

  
 
  

}
