#include <SoftwareSerial.h>

SoftwareSerial bt(2, 3);  // RX, TX
char data;
void setup() {
  Serial.begin(9600);
  bt.begin(9600);
}

void loop() {

  if (Serial.available()){
    data = Serial.read();
    bt.write(data);   
  }
}