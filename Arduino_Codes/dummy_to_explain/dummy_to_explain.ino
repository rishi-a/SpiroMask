bool set=1;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 
    int32_t val = 9;
    //char inchar = val+'0';
    char inchar;
    //Serial.println(val);
    //Serial.println("\n");
    Serial.println("---");
    inchar = char(val);
    Serial.println(inchar);
    
  
 

}
