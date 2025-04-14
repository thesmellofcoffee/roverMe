# 🚀 RoverMe - Autonomous Rover Project

RoverMe is an autonomous rover designed to navigate to a user's location upon request via an iOS (Swift) application. The project supports multiple hardware configurations, including Raspberry Pi Pico WH, Arduino, and NodeMCU microcontrollers, all communicating via Firebase for real-time location tracking and command delivery.

## 🎯 Project Features

- Autonomous navigation with GPS guidance
- Firebase real-time data integration
- Multi-platform support (Raspberry Pi Pico WH, Arduino, NodeMCU)
- User-friendly iOS application (Swift)
- Remote command via Firebase and IR remote control
- "Tank turn" (in-place rotation) capability

## 🛠 Hardware Components

- Raspberry Pi Pico WH
- Arduino Duemilanove (alternative implementation)
- NodeMCU ESP8266 (alternative implementation)
- Neo-6M GPS Module
- HW-95 Motor Drivers (x2, controlling 4 DC motors)
- Ultrasonic Sensor (HC-SR04)
- IR Receiver and Remote Module
- Power management (battery and voltage regulator)

## 💻 Software Components

- **Raspberry Pi Pico WH**: MicroPython / C implementation for high-performance motor control and GPS handling.
- **Arduino**: C/C++ implementation for basic navigation and GPS handling (alternative solution).
- **NodeMCU**: ESP8266 Arduino IDE implementation for Firebase communication and motor control (alternative solution).
- **Swift App**: User interface to send commands, visualize rover location on a map, and interact with Firebase.

## 🚦 Setup and Installation Guide

### 🔧 Hardware Installation
- Detailed schematics for motor and sensor connections can be found in the [Hardware Schematics folder](link-to-schematics).

### 🥧 Raspberry Pi Pico WH
1. Install MicroPython or compile the C firmware provided.
2. Upload main scripts via Thonny or command-line.

### 📟 Arduino (Optional)
1. Use Arduino IDE to compile and upload code from `arduino/` folder.

### 📶 NodeMCU (Optional)
1. Upload NodeMCU firmware via Arduino IDE from `nodemcu/` folder.

### 📱 Swift Application
1. Open project with Xcode from `ios_app/` folder.
2. Configure Firebase credentials in the app’s config file.
3. Run on simulator or physical device.

## 🔥 Firebase Integration
The project utilizes Firebase Realtime Database for remote commands and location tracking:










🚀 RoverMe – Autonomes Rover-Projekt

RoverMe ist ein autonomer Rover, der auf Anfrage über eine iOS-App (Swift) zum Standort des Nutzers navigiert. Das Projekt unterstützt mehrere Hardware-Konfigurationen, darunter Raspberry Pi Pico WH, Arduino und NodeMCU. Die Kommunikation erfolgt über Firebase, wodurch Standortdaten und Befehle in Echtzeit übermittelt werden können.

🎯 Projektmerkmale

-Autonome Navigation mit GPS-Unterstützung

-Firebase-Echtzeitintegration für Daten

-Multi-Plattform-Support (Raspberry Pi Pico WH, Arduino, NodeMCU)

-Benutzerfreundliche iOS-Anwendung (Swift)

-Fernsteuerung per Firebase und IR-Fernbedienung

-„Tank Turn“ (Drehung auf der Stelle)



----🛠 Hardwarekomponenten----
-Raspberry Pi Pico WH
-Arduino Duemilanove (alternative Implementierung)
-NodeMCU ESP8266 (alternative Implementierung)
-Neo-6M GPS-Modul
-HW-95 Motortreiber (2 Stück, steuern 4 DC-Motoren)
-Ultraschallsensor (HC-SR04)
-IR-Empfänger und Fernbedienungsmodul
-Stromversorgung (Batterie und Spannungsregler)


💻 Softwarekomponenten

-Raspberry Pi Pico WH: Implementierung in MicroPython / C für leistungsstarke Motorsteuerung und GPS-Verwaltung.

-Arduino: C/C++-Implementierung für grundlegende Navigation und GPS-Verarbeitung (alternative Lösung).

-NodeMCU: ESP8266 Arduino IDE-Implementierung für Firebase-Kommunikation und Motorsteuerung (alternative Lösung).

-Swift-App: Benutzeroberfläche zum Senden von Befehlen, zur Anzeige des Rover-Standorts auf einer Karte und zur Interaktion mit Firebase.

🚦 Einrichtungs- und Installationsanleitung


🔧 Hardwareinstallation

-Ausführliche Schaltpläne für Motor- und Sensoranschlüsse befinden sich im Ordner Hardware Schematics.

🥧 Raspberry Pi Pico WH

-Installieren Sie MicroPython oder kompilieren Sie die bereitgestellte C-Firmware.
-Laden Sie die Hauptskripte über Thonny oder eine Kommandozeile hoch.

📟 Arduino (Optional)

Verwenden Sie die Arduino IDE, um den Code aus dem Ordner arduino/ zu kompilieren und hochzuladen.

📶 NodeMCU (Optional)

Laden Sie die NodeMCU-Firmware über die Arduino IDE aus dem Ordner nodemcu/ hoch.

📱 Swift-Anwendung

Öffnen Sie das Projekt in Xcode aus dem Ordner ios_app/.
Konfigurieren Sie die Firebase-Zugangsdaten in der Konfigurationsdatei der App.
Führen Sie die App im Simulator oder auf einem physischen Gerät aus.
🔥 Firebase-Integration
Das Projekt verwendet die Firebase Realtime Database, um Befehle in Echtzeit zu empfangen und den Standort des Rovers zu verfolgen.
