# SmartView – SPS Web-HMI mit OPC UA

## 📌 Projektbeschreibung

Dieses Projekt realisiert eine Web-HMI (Human Machine Interface) zur Überwachung und Steuerung einer SPS (Speicherprogrammierbare Steuerung) über OPC UA.

Ein Raspberry Pi liest Prozessdaten aus der SPS und stellt diese in einer Weboberfläche dar. Zusätzlich können Steuerbefehle (Start, Stopp, Reset) über den Browser gesendet werden.

### Industrie 4.0 Bezug

Das Projekt zeigt zentrale Konzepte von Industrie 4.0:

* Vernetzung von Maschinen (SPS ↔ Raspberry Pi)
* Nutzung von OPC UA als Industriestandard
* Webbasierte Visualisierung (Remote Monitoring)
* Fernsteuerung von Anlagen

---

## 🚀 Kurzanleitung (Quick Start)

```bash
PC Terminalsteuerung:
ssh andiarbeit@192.168.137.XXX
cd smartview
python3 backend/app.py

XXX: Die IP die der Laptop für den Raspberry PI vergibt

Visual Code:
zuerst das Remote Paket installieren
wenn installiert:
STRG + SHIFT + P
andiarbeit@192.168.137.XXX oben einfügen
Passwort: streik26
Open Folder: smartview und dann backend
(gegebenenfalls noch Linux als Betriebssystem auswählen)
```

Dann im Browser öffnen:

```
http://192.168.137.XXX:5000
```

---

## ⚙️ Setup

### Hardware

* Raspberry Pi
* SPS mit OPC UA Server

### Software

* Raspberry Pi OS (auf SD-Karte installiert)
* Python 3

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors asyncua
```

---

## 🔧 Konfiguration

### OPC UA Verbindung

```python
SPS_IP = "192.168.1.1"
SPS_URL = f"opc.tcp://{SPS_IP}:4840"
```

### Verwendete NodeIDs

```text
Analogwert:
ns=3;s="RPI_verknuepfung"."SFEProjekt.Analogwert"

Magazin:
ns=3;s="RPI_verknuepfung"."SFEProjekt.Magazin_voll"

Zylinder:
ns=3;s="RPI_verknuepfung"."SFEProjekt.Zylinder_ausfahren"
```

Steuerbefehle:

* Start
* Stopp
* Reset

---

## 🏗️ Architektur

```
+-------------------+
|       SPS         |
|  (OPC UA Server)  |
+--------+----------+
         |
         | OPC UA
         |
+--------v----------+
|   Raspberry Pi    |
|  Python Backend   |
|  Flask + asyncua  |
+--------+----------+
         |
         | HTTP / API
         |
+--------v----------+
|     Browser       |
|   Web Interface   |
+-------------------+
```

---

## 🖥️ Weboberfläche

Die Weboberfläche zeigt:

* Analogwert
* Zustand des Zylinders
* Magazinstatus
* Steuerbuttons (Start, Stopp, Reset)
* 
* Betriebsart (Automatikbetrieb/Tippbetrieb)
* Wertkstück am Ende des Förderbands






(Screenshot von Website hier einfügen)
<img width="1157" height="840" alt="image" src="https://github.com/user-attachments/assets/e24fd2c7-7f98-47f0-8f82-bfa9a02fc0a1" />

<img width="2398" height="1271" alt="image" src="https://github.com/user-attachments/assets/a1df76d9-da60-4d35-ba00-01a6a05d8ba4" />
<img width="2398" height="1265" alt="image" src="https://github.com/user-attachments/assets/99d20361-5ec8-4ca1-8447-d3c9cdc4a87e" 
         <img width="2381" height="1266" alt="image" src="https://github.com/user-attachments/assets/14077d6b-a16e-48fe-b2e6-1e3e9db19e75" />
         <img width="2398" height="1264" alt="image" src="https://github.com/user-attachments/assets/e2e7353e-7d19-48bd-b707-18c2e05e8566" />


## 👥 Team

* Marius Steinbrecht
* Andreas Wühr

---

## 📄 Lizenz

Copyright (c) 2026 Marius Steinbrecht & Andreas Wühr
Die Nutzung, Kopie, Veränderung und Weitergabe der Software ist erlaubt, sowohl privat als auch kommerziell.

Bedingungen:
Der Urheberrechtshinweis muss enthalten bleiben

Haftungsausschluss:
Die Software wird ohne jegliche Garantie bereitgestellt. Die Autoren übernehmen keine Haftung für Schäden, die durch die Nutzung entstehen.
