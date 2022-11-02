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



#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <avr/dtostrf.h>.

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_DC     6
#define OLED_CS     5
#define OLED_RESET  9
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT,
  &SPI, OLED_DC, OLED_RESET, OLED_CS);


#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ 0b00000000, 0b11000000,
  0b00000001, 0b11000000,
  0b00000001, 0b11000000,
  0b00000011, 0b11100000,
  0b11110011, 0b11100000,
  0b11111110, 0b11111000,
  0b01111110, 0b11111111,
  0b00110011, 0b10011111,
  0b00011111, 0b11111100,
  0b00001101, 0b01110000,
  0b00011011, 0b10100000,
  0b00111111, 0b11100000,
  0b00111111, 0b11110000,
  0b01111100, 0b11110000,
  0b01110000, 0b01110000,
  0b00000000, 0b00110000 };


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

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
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
  greettext();
}

void loop() {
  int i;
  digitalWrite(writeIndicator, LOW);
  float eCO2; 
  // make a string for assembling the data to log:
  String dataString = "";
  if(ccs.available()){
    for (i = 0; i < SAMPLES; i++) {
      if(!ccs.readData()){
        eCO2 = ccs.geteCO2();
        Serial.println(eCO2);
        if(eCO2 < 800.0) //set this from outside co2 sensor
          break; 
        vReal[i] = eCO2;
        vImag[i] = 0;
        if(i>=50)
          displayCO2(eCO2); //displays on OLED
        delay(1000);
      }
    }
    if(i == SAMPLES){  //only perform FFT if we have collected enough samples i.e 64 samples
      FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
      FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
      FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
      double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
      Serial.print("RR = ");
      Serial.println(peak*60.0);
      if(peak*60.0 < 5.00){ 
        displayRespirationRate(0.0); 
      }
      else{
        displayRespirationRate(peak*60.0); 
      } 
    } //if(i == SAMPLES-1) 
    else{
      noRR();
    }
  }
}




void greettext(void) {
  display.clearDisplay();

  display.setTextSize(2); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println(F("SpiroMask"));
  display.display();      // Show initial text
  delay(100);

  // Scroll in various directions, pausing in-between:
  display.startscrollright(0x00, 0x0F);
  delay(1000);
  display.stopscroll();
  delay(1000);
  display.startscrollleft(0x00, 0x0F);
  delay(1000);
  display.stopscroll();
}


void displayCO2(double val) {
  char stringOutput[10];
  String myOLEDdata = "";
  dtostrf(val,2,2,stringOutput);
 
  display.clearDisplay();

  display.setTextSize(3); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println(F("eCO2"));
  display.println(F(stringOutput));
  //display.println(F("BrPM\n 20"));
  display.display();      // Show initial text
  //delay(100);
}


void displayRespirationRate(double val) {
  char stringOutput[10];
  String myOLEDdata = "";
  dtostrf(val,2,2,stringOutput);
 
  display.clearDisplay();

  display.setTextSize(3); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println(F("BrPM"));
  display.println(F(stringOutput));
  //display.println(F("BrPM\n 20"));
  display.display();      // Show initial text
  //delay(100);
}

void noRR(void) {
  display.clearDisplay();

  display.setTextSize(2); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 0);
  display.println(F("Mask\nLoose"));
  display.display();      // Show initial text
  delay(100);

  // Scroll in various directions, pausing in-between:
  display.startscrollright(0x00, 0x0F);
  delay(1000);
  display.stopscroll();
  delay(1000);
  display.startscrollleft(0x00, 0x0F);
  delay(1000);
  display.stopscroll();
}
