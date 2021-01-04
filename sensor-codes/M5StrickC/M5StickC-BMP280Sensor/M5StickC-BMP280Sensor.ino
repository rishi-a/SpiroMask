#include "bmp280.h"
//#include <M5Stack.h>
#include <M5StickC.h>

#define P0 1013.25

BMP280 bmp;


void setup()
{
  M5.begin();
  if(!bmp.begin()){
    Serial.println("BMP init failed!");
    while(1);
  }
  else Serial.println("BMP init success!");
  
  bmp.setOversampling(4);
  //M5.Lcd.drawString("BPS Example", 90, 0, 4);
  
}
void loop()
{
  double T,P;
  char result = bmp.startMeasurment();
 
  if(result!=0){
    delay(result);
    result = bmp.getTemperatureAndPressure(T,P);
    
      if(result!=0)
      {
        double A = bmp.altitude(P,P0);
        
        Serial.print("T = \t");Serial.print(T,2); Serial.print(" degC\t");
        Serial.print("P = \t");Serial.print(P,2); Serial.print(" mBar\t");
        Serial.print("A = \t");Serial.print(A,2); Serial.println(" m");
        //display_result(T, P, A);
      }
      else {
        Serial.println("Error.");
      }
  }
  else {
    Serial.println("Error.");
  }
  
  delay(2000);
  //M5.Lcd.fillRect(160, 40, 100, 80, BLACK);
}
