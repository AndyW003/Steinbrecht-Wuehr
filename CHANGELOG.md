[0.1] – Projektstart
Projektidee festgelegt: SCADA-System mit OPC UA
Architektur definiert:

Raspberry Pi als Edge Device
SPS als Datenquelle
Webserver zur Visualisierung
Entwicklungsumgebung vorbereitet
[0.2] – Raspberry Pi Einrichtung
Raspberry Pi erfolgreich installiert und gestartet
Verbindung über SSH eingerichtet
Netzwerk über Hotspot konfiguriert
Erste Verbindung vom Laptop zum Raspberry hergestellt
[0.3] – Python Umgebung
Virtuelle Umgebung (venv) erstellt
Python-Pakete installiert:

flask
flask-cors
opcua / asyncua
Projektstruktur erstellt:

/backend
[0.4] – Flask Webserver
Erste Flask-App erstellt
REST API Endpoint implementiert:

GET /api/tags
Testdaten (random Werte) erfolgreich im Browser angezeigt
Raspberry als Webserver im Netzwerk erreichbar gemacht
[0.4.1] – Zwischen Probleme
Probleme mit zweit PC auf Raspberry → aufgrund von Krankheit
[0.4.2] – Netzwerkproblem behoben
Problem: Raspberry Webserver war im Browser nicht erreichbar
Ursache: Flask lief nur auf 127.0.0.1
Lösung: Server auf 0.0.0.0 umgestellt → Zugriff aus dem Netzwerk möglich
[0.5] – SPS Vorbereitung
OPC UA Server auf der SPS aktiviert
Benutzer für OPC UA Zugriff erstellt
Globaler Datenbaustein (DB_HMI) angelegt:

Analogwert (REAL)
Start (BOOL)
Stopp (BOOL)
Reset (BOOL)
Optimierten Bausteinzugriff deaktiviert
OPC UA Zugriff für Variablen konfiguriert (Lesen/Schreiben)
[0.5.1] – OPC UA Zugriff korrigiert
Problem: Zugriff auf SPS Variablen nicht möglich
Ursache: Optimierter Bausteinzugriff im DB aktiv
Lösung: Optimierung deaktiviert → NodeIds funktionieren

TIA Portal update nötig

[0.6] – SPS Logik Integration
DB_HMI Variablen in SPS-Programm eingebunden:

Start → startet Prozess
Stopp → stoppt Prozess
Reset → setzt Prozess zurück
Analogwert wird aus SPS in DB_HMI geschrieben
[0.7] – OPC UA Verbindung
OPC UA Client in Python implementiert
Verbindung zur SPS hergestellt
Erste Werte erfolgreich aus SPS gelesen
Fehlerbehandlung für Verbindungsprobleme eingebaut
[0.7.1] – Verbindungsfehler OPC UA
Problem: Verbindung zur SPS wurde abgelehnt
Ursache: Benutzerrechte / Authentifizierung fehlten
Lösung: Benutzer im OPC UA Server eingerichtet
[0.8] – API mit echten SPS-Daten
Flask API liefert jetzt echte SPS-Daten statt Dummy-Werten
JSON-Struktur angepasst:

Analogwert
Status
Verbindung über Browser getestet
[0.9] – Steuerbefehle (Write)
OPC UA Schreibfunktion implementiert
Start/Stopp/Reset Befehle vom Raspberry zur SPS gesendet
SPS reagiert korrekt auf externe Befehle
[1.0] – Frontend
Responsive Weboberfläche mit HTML/CSS/JS
Anzeige von:

Analogwerten
Status (Ein/Aus)
Steuerbuttons:
Start / Stopp / Reset
[1.1] – Benutzer-Login System
Einfaches Login-System implementiert
Zugriffsschutz für:
Weboberfläche
API-Endpunkte
Session-basierte Authentifizierung
Login/Logout Funktion hinzugefügt
[1.2] – Historisierung (SQLite)
Lokale Datenbank (SQLite) integriert
Automatisches Speichern von Prozessdaten:
Analogwert
Magazinstatus
Zylinderstatus
Zeitstempel
Tabelle history erstellt
Speicherung bei jeder SPS-Abfrage
[1.3] – Verbesserte API
API um Authentifizierung erweitert
Fehlerbehandlung verbessert
Strukturierte JSON-Antworten
Zugriffsschutz für nicht eingeloggte Benutzer
[1.4] – Frontend Visualisierung
Vollständige Weboberfläche implementiert
Darstellung eines Förderbands mit Animation:
Zylinderbewegung
Materialfluss (Puck)
Statusanzeigen:
Magazin (voll/leer)
Zylinder (ein/ausgefahren)
Analogwert mit Einheit
[1.6] – Live-Daten & Performance
Datenaktualisierung alle 200 ms
Asynchrone Kommunikation (asyncio)
Schnelle Reaktion auf Zustandsänderungen
[1.7] – Warnsystem
Visuelles Warnsystem implementiert:
Anzeige bei negativem Analogwert
Overlay mit Bestätigungsbutton
Zustandsverwaltung im Frontend
[1.8] – Sicherheits- und Stabilitätsverbesserungen
Fehlerbehandlung für:
OPC UA Verbindungsprobleme
Datenbankfehler
Schutz vor unautorisierten Zugriffen
Session-Handling verbessert
[1.9] – Dokumentation
README.md erstellt
Architekturdiagramm hinzugefügt
Setup-Anleitung dokumentiert
Screenshots eingefügt
[2.0] – Finalisierung
Code bereinigt und kommentiert
GitHub Repository strukturiert
Projekt abgeschlossen und getestet
