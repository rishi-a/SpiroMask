// This code records audio using the Adafruit I2S microphone (SPH0645LM4H) and stores raw audio data in an SD card
// Currently, the data is stored at 100 Hz, but the microphone is samples at 8kHZ.
// The code below is heavily insipired from the discussion in the GitHub repo as noted below.
// I2S code Source: https://github.com/adafruit/Adafruit_ZeroDMA/issues/12
// Author: Rishiraj Adhikary | https://rishi-a.github.io  

#include <SPI.h>
#include <SD.h>
//#include <I2S.h>
#include <Adafruit_ZeroI2S.h>

//audio intake settings.
#define SAMPLERATE_HZ 8000
int32_t audiosamples = 512;
const int sample_delay = 1000;

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


  //check SD card status
  /*
  if(!SD.begin(chipSelect)){
    Serial.println("Card failed, or not present");  
    //don't do anything more
    while(1);
  }
  Serial.println("Card Initialised");
  */
}

void loop() {

  String dataString = ""; //this variable will be used to convert audio amplitude to string

  // This is a stereo Mic. But we'll only read from LEFT channel
  digitalWrite(11, LOW);  

  float sound;
  int32_t left,right;
  int i;
  int sample=0;

  // Read a bunch of samples!!!
  int32_t samples[audiosamples];
  char charSamples[audiosamples];
  
  for (int i = 0; i < audiosamples; i++) {
    i2s.read(&left, &right);
    delay(1);  // Workaround delay to prevent oversizing the buffer
    sample = left;
    //Serial.println(sample);
    // convert to 18 bit signed
    sample >>= 14;
    samples[i] = abs(sample);
  }

  for (int i = 0; i < audiosamples; i++) {
    Serial.println(samples[i]);
    //samples[i] -= meanval;
  }

  // Calculate mean (avg) over samples
  
  float meanval = 0;
  for (int i = 0; i < audiosamples; i++) {
    meanval += samples[i];
  }
  meanval /= audiosamples;

  // subtract it from all samples to get a 'normalized' output
  for (int i = 0; i < audiosamples; i++) {
    samples[i] -= meanval;
  }

  /*
  // find the 'peak to peak' max
  float maxsample, minsample;
  minsample = 100000;
  maxsample = -100000;
    
  for (int i = 0; i < audiosamples; i++) {
    minsample = min(minsample, samples[i]);
    maxsample = max(maxsample, samples[i]);
  }

  sound = 10 * log(maxsample - minsample);
  Serial.println(sound);
 
  //convert audio amplitude to String
  dataString += String(sound);
  

  //store data in SD card;
  File dataFile = SD.open("datalog.txt",FILE_WRITE);

  //if file is available, write to it
  if(dataFile){
    dataFile.println(dataString);
    dataFile.close();
    digitalWrite(writeIndicator, HIGH);  
  }
  delay(10); // Let's just process a measurement each 10 micro second.
  */

}
