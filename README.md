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
ssh andiarbeit@192.168.137.43
cd smartview
python3 backend/app.py
```

Dann im Browser öffnen:

```
http://192.168.137.43:5000
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






(Screenshot hier einfügen)

---











## 👥 Team

* Marius Steinbrecht
* Andreas Wühr

---

## 📄 Lizenz

MIT Lizenz

Copyright (c) 2026 Marius Steinbrecht & Andreas Wühr
Die Nutzung, Kopie, Veränderung und Weitergabe der Software ist erlaubt, sowohl privat als auch kommerziell.

Bedingungen:
Der Urheberrechtshinweis muss enthalten bleiben

Haftungsausschluss:
Die Software wird ohne jegliche Garantie bereitgestellt. Die Autoren übernehmen keine Haftung für Schäden, die durch die Nutzung entstehen.
