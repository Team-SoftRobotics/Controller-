#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ESP32_Control";
const char* password = "12345678";

WebServer server(80);

// --- Hardware Pins ---
const int DIR_PIN  = 25;
const int STEP_PIN = 26;
const int ENA_PIN  = 27;

// --- Motor Settings ---
const int stepsPerCommand = 400; // Number of steps per key press
const int stepDelay = 1000;       // Microseconds between pulses (lower is faster)

void stepMotor(int steps) {
    for (int i = 0; i < steps; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(stepDelay);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(stepDelay);
    }
}

void handleCommand() {
    String cmd = server.arg("cmd");
    Serial.print("\n[WIFI] Command received: ");
    Serial.println(cmd);

    // 1. Acknowledge the laptop immediately so Python doesn't throw a timeout error
    server.send(200, "text/plain", "OK: " + cmd);

    // 2. Move the hardware
    if (cmd == "cw") {
        Serial.println("[MOTOR] Executing Clockwise turn...");
        digitalWrite(DIR_PIN, HIGH);
        stepMotor(stepsPerCommand);
    } 
    else if (cmd == "ccw") {
        Serial.println("[MOTOR] Executing Anti-Clockwise turn...");
        digitalWrite(DIR_PIN, LOW);
        stepMotor(stepsPerCommand);
    }

    Serial.println("[MOTOR] Movement complete.");
    Serial.println("--------------------------------");
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    // Initialize Motor Pins
    pinMode(DIR_PIN, OUTPUT);
    pinMode(STEP_PIN, OUTPUT);
    pinMode(ENA_PIN, OUTPUT);
    digitalWrite(ENA_PIN, LOW); // TB6600 Enable

    // Start SoftAP Wi-Fi
    Serial.println("\n[INIT] Starting Wi-Fi Access Point...");
    WiFi.softAP(ssid, password);
    
    Serial.print("[INIT] Connect laptop to Wi-Fi SSID: ");
    Serial.println(ssid);
    Serial.print("[INIT] ESP32 IP Address: ");
    Serial.println(WiFi.softAPIP());

    // Define web server routes
    server.on("/command", HTTP_GET, handleCommand);
    server.begin();
    
    Serial.println("[INIT] Server running. Waiting for commands...");
    Serial.println("--------------------------------");
}

void loop() {
    server.handleClient();
}
