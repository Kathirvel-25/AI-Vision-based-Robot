#include <SoftwareSerial.h>

SoftwareSerial bt(2, 3);  // RX, TX
char data;

#define ENA 5
#define IN1 9
#define IN2 10

#define ENB 6
#define IN3 11
#define IN4 12

void setup() {

  Serial.begin(9600);
  bt.begin(9600);
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void MotorMove(){
  
  analogWrite(ENA, 70);
  analogWrite(ENB, 70);

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void left() {
  analogWrite(ENA, 70);
  analogWrite(ENB, 70);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);  

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);   
}

void Right(){
  analogWrite(ENA,70);
  analogWrite(ENB,70);

  digitalWrite(IN1,HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void loop() {

  if (bt.available()) {

    data = bt.read(); 

    Serial.print("Received: ");
    Serial.println(data);

    if(data == 'F'){
      MotorMove();
    }
    if(data == 'S'){
      stopMotors();
    }
    if(data == 'L'){
      left();
    }
    if (data == 'R'){
      Right();
    }      
  }
}
