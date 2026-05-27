#include <SPI.h>
#include <LoRa.h>

#define SS 10
#define RST 9
#define DIO0 2

String incomingData = "";

void setup() {
  Serial.begin(9600);

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }

  Serial.println("LoRa Transmitter Ready");
}

void loop() {

  while (Serial.available()) {
    char c = Serial.read();
    
    if (c == '\n') {
      
      incomingData.trim();

      if (incomingData == "ALERT") {

        LoRa.beginPacket();
        LoRa.print("VEHICLE_ALERT");
        LoRa.endPacket();

        Serial.println("Alert Sent via LoRa");
      }

      incomingData = "";
    }
    else {
      incomingData += c;
    }
  }
}