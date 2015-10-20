int rel = 4;

int m0 = 11;
int m1 = 10;
int m2 = 9;
int m3 = 12;
int m4 = 3;
int m5 = 5;

int ser = A5;

char command;

void setup() {
  pinMode(ser,OUTPUT);
  pinMode(rel,OUTPUT);
  pinMode(m0,OUTPUT);
  pinMode(m1,OUTPUT);
  pinMode(m2,OUTPUT);
  pinMode(m3,OUTPUT);
  pinMode(m4,OUTPUT);
  pinMode(m5,OUTPUT);
  Serial.begin(9600);
  Serial.println("READY");
}

void loop() {
  while (Serial.available() > 0) {
    command = Serial.read();
    Serial.println(command);
    if (command == B110000) {
      digitalWrite(rel,HIGH);
    } else if (command == B110001) {
      digitalWrite(rel,LOW);
    } else if (command == B110010) {
      digitalWrite(m0,HIGH);
    } else if (command == B110011 ) {
      digitalWrite(m0,LOW);
    } else if (command == B110100 ) {
      digitalWrite(m1,HIGH);
    } else if (command == B110101 ) {
      digitalWrite(m1,LOW);
    } else if (command == B110110 ) {
      digitalWrite(m2,HIGH);
    } else if (command == B110111 ) {
      digitalWrite(m2,LOW);
    } else if (command == B111000 ) {
      digitalWrite(m3,HIGH);
    } else if (command == B111001 ) {
      digitalWrite(m3,LOW);
    } else if (command == B1100001 ) {
      digitalWrite(m4,HIGH);
    } else if (command == B1100010 ) {
      digitalWrite(m4,LOW);
    } else if (command == B1100011 ) {
      digitalWrite(m5,HIGH);
    } else if (command == B1100100 ) {
      digitalWrite(m5,LOW);
    } else if (command == B1100101) {
      digitalWrite(ser,HIGH);
    } else if (command == B1100111 ) {
      digitalWrite(ser,LOW);
    }   
  }
}
