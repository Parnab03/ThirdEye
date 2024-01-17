#include <LiquidCrystal.h>

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);
const int buzzer_Pin = 13;
const int led_Pin = 11;
char sleep_status = 0;
const int Relay_Pin = 12;
unsigned long previousMillis = 0;
const long interval = 2000;

void setup() {
  Serial.begin(9600);
  pinMode(buzzer_Pin, OUTPUT);
  pinMode(led_Pin, OUTPUT);
  pinMode(Relay_Pin, OUTPUT);
  lcd.begin(16, 2);
  lcd.print("Drowsiness Driver ");
  lcd.setCursor(0, 2);
  lcd.print("Detection System");
  digitalWrite(buzzer_Pin, LOW);
  digitalWrite(led_Pin, LOW);
  digitalWrite(Relay_Pin, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    sleep_status = Serial.read();
    handleSleepStatus(sleep_status);
  }

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    handleSleepStatus('b'); // Assuming default status when no commands received
    previousMillis = currentMillis;
  }
}

void handleSleepStatus(char status) {
  switch (status) {
    case 'a':
      lcd.clear();
      lcd.print("Please wake up");
      digitalWrite(buzzer_Pin, HIGH);
      digitalWrite(led_Pin, HIGH);
      digitalWrite(Relay_Pin, LOW);
      delay(2000);
      digitalWrite(buzzer_Pin, LOW);
      digitalWrite(led_Pin,  LOW);
      digitalWrite(Relay_Pin, HIGH);
      break;

    case 'b':
      lcd.clear();
      lcd.print("All Ok");
      lcd.setCursor(0, 2);
      lcd.print("Drive Safe");
      digitalWrite(buzzer_Pin, LOW);
      digitalWrite(led_Pin, LOW);
      digitalWrite(Relay_Pin, HIGH);
      break;

    default:
      /* Do Nothing */
      break;
  }
}