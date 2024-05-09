//--------------
// Tested ESP8266 OLED Display 128 x 64 MQTT publish and subscriber.
// code written on : 2/05/2024

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

// Wi-Fi credentials
const char* ssid = "Swapnonil"; // Swapnonil // Chakra_nssv
const char* password = "$ubho&$hreya"; //$ubho&$hreya // Coron@Virus$19 

// MQTT broker details
const char* mqtt_server = "192.168.0.119"; // Raspberry Pi IP Address
const int mqtt_port = 1883;
const char* mqtt_topic = "sensor/temperature";
const char* mqtt_username = "subha";
const char* mqtt_password = "123456789";

// OneWire setup
const int oneWireBus = 14; // D5 : GPIO 14 pin connected to DS18B20
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

// OLED setup
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// MQTT setup
WiFiClient espClient;
PubSubClient client(espClient);

void setupWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected.");
}

void setupMQTT() {
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback); // Set callback function for incoming MQTT messages
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect("ESP8266", mqtt_username, mqtt_password)) {
      Serial.println("MQTT connected.");
      client.subscribe(mqtt_topic); // Subscribe to the topic upon successful connection
    } else {
      Serial.print("MQTT connection failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Handle incoming MQTT messages here
}

void setup() {
  Serial.begin(115200);
  setupWiFi();
  setupMQTT();
  sensors.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 initialization failed.");
    while (true);
  }
  display.clearDisplay();
}

void updateDisplay(float temperature) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  //  display.setCursor(0, 0);
  display.setCursor(10, 0);
  display.print("Temperature:");
  display.setTextSize(2);
  //  display.setCursor(0, 16);
  display.setCursor(10, 26);

  display.print(temperature, 2);
  display.print(" C");
  display.display();
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);

  Serial.println("Temperature: " + String(temperature) + " C");
  client.publish(mqtt_topic, String(temperature).c_str());

  updateDisplay(temperature);

  delay(5000); // Wait for 5 seconds before the next reading
}
