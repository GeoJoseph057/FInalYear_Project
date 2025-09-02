#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "mobile";
const char* password = "11112222";

// MQTT Broker settings
const char* mqtt_server = "broker.emqx.io";  // Public MQTT broker
const int mqtt_port = 1883;
const char* mqtt_topic = "esp8266/fsr_sensor";
const char* client_id = "ESP8266_FSR_Client";

// FSR pin definition - ESP8266 uses different pin naming
#define FSR_PIN A0  // Analog pin on ESP8266

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(client_id)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);  // Allow time for serial monitor to open
  
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int fsrReading = analogRead(FSR_PIN);  // Read analog value (0-1023 on ESP8266)
  
  // Convert to voltage (ESP8266 ADC range is 0-3.3V but with 10-bit resolution)
  float voltage = fsrReading * (3.3 / 1023.0);

  Serial.print("FSR Reading: ");
  Serial.print(fsrReading);
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 3);
  Serial.println(" V");

  // Determine message to publish based on threshold
  String message = (fsrReading > 250) ? "1" : "0";
  
  // Publish to MQTT
  client.publish(mqtt_topic, message.c_str());
  Serial.print("Published to MQTT: ");
  Serial.println(message);


  delay(200);  // Adjust delay as needed
}