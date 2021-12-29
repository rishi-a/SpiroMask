//This code should consume 0.8mA to 0.93mA on the Arduino Nano 33 BLE Sense after cutting the jumper.

void setup() {
  pinMode(LED_PWR, OUTPUT);
  digitalWrite(LED_PWR, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(60 * 1000);
}
