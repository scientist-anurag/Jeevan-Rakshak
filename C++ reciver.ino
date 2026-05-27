#include <SPI.h>
#include <LoRa.h>

#define SS 10
#define RST 9
#define DIO0 2

#define BUZZER 7
#define LED 6

unsigned long alertTimer = 0;
bool alertActive = false;

void setup() {

  Serial.begin(9600);

  pinMode(BUZZER, OUTPUT);
  pinMode(LED, OUTPUT);

  digitalWrite(BUZZER, LOW);
  digitalWrite(LED, LOW);

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }

  Serial.println("LoRa Receiver Ready");
}

void loop() {

  int packetSize = LoRa.parsePacket();

  if (packetSize) {

    String received = "";

    while (LoRa.available()) {
      received += (char)LoRa.read();
    }

    Serial.print("Received: ");
    Serial.println(received);

    if (received == "VEHICLE_ALERT") {

      digitalWrite(LED, HIGH);
      tone(BUZZER, 1000);

      alertTimer = millis();
      alertActive = true;
    }
  }

  // Auto stop alert after 3 seconds
  if (alertActive && millis() - alertTimer > 3000) {

    digitalWrite(LED, LOW);
    noTone(BUZZER);

    alertActive = false;
  }
}