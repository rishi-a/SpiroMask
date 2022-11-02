#include <Arduino_LSM9DS1.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);
  //Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  //Serial.print("Accelerometer sample rate = ");
  //Serial.print(IMU.accelerationSampleRate());
  //Serial.println(" Hz");
  //Serial.print("Gyroscope sample rate = ");
  //Serial.print(IMU.gyroscopeSampleRate());
  //Serial.println(" Hz");
  //Serial.println();
  //Serial.println("Acceleration  in G's and Gyroscope in degree/sec");
  Serial.println("X\tY\tZ\tXG\tYG\tZG");
}

void loop() {
  // put your main code here, to run repeatedly:
  float x, y, z, xg, yg,zg;

  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(x, y, z);
    IMU.readGyroscope(xg, yg, zg);


    Serial.printf("%f %f %f %f %f %f\n", x,y,z,xg,yg,zg);
    /*
    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
    Serial.print('\t');
    Serial.print(xg);
    Serial.print('\t');
    Serial.print(yg);
    Serial.print('\t');
    Serial.print(zg);
    //Serial.print('\n');
    */
  }

}
