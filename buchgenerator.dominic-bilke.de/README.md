# Modern Book Generator

Ein fortschrittlicher, KI-gestützter Buchgenerator, der professionelle E-Books mit modernem Design und strukturiertem Inhalt erstellt.

## 🚀 Features

### ✨ Moderne Benutzeroberfläche
- **Responsive Design**: Optimiert für Desktop, Tablet und Mobile
- **Moderne UI/UX**: Clean Design mit Inter Font und Font Awesome Icons
- **Gradient Backgrounds**: Attraktive Farbverläufe und moderne Schatten
- **Real-time Progress**: Live-Fortschrittsanzeige während der Inhaltsgenerierung

### 🤖 KI-gestützte Inhaltsgenerierung
- **ChatGPT Integration**: Automatische Generierung von Vorwort, Kapiteln und Nachwort
- **Intelligente Strukturierung**: Automatische Erstellung von Inhaltsverzeichnissen
- **Bildgenerierung**: KI-gestützte Cover-Bilder basierend auf dem Hauptthema
- **Mehrsprachige Unterstützung**: Optimiert für deutsche Inhalte

### 📚 Professionelle E-Book-Erstellung
- **Modernes PDF-Layout**: Zeitgemäßes Design mit professioneller Typografie
- **Strukturierte Inhalte**: Kapitel, Überschriften, Listen und Zitate
- **Responsive Typography**: Optimierte Lesbarkeit auf allen Geräten
- **Automatische Formatierung**: Professionelle Seitenumbrüche und Layout

## 🛠️ Technologie-Stack

### Frontend
- **HTML5**: Semantische Struktur
- **CSS3**: Moderne Styling mit CSS Grid und Flexbox
- **JavaScript/jQuery**: Interaktive Funktionalität
- **Font Awesome**: Moderne Icons
- **Google Fonts (Inter)**: Moderne Typografie

### Backend
- **PHP**: Server-seitige Verarbeitung
- **TCPDF**: Professionelle PDF-Generierung
- **FPDI**: PDF-Manipulation und -Konkatenation
- **cURL**: Externe API-Kommunikation

### Externe Services
- **ChatGPT API**: Inhaltsgenerierung via `askgpt.bilke-projects.com`
- **Bildgenerierung**: Cover-Images via KI-Service

## 📁 Projektstruktur

```
buchgenerator.dominic-bilke.de/
├── index.html                 # Hauptseite mit modernem Interface
├── generate_book.php          # PDF-Generierung mit modernem Layout
├── fetch_book_data.php        # KI-API Integration
├── css/
│   ├── modern-style.css       # Moderne CSS-Styles
│   └── style.css             # Legacy Styles (Backup)
├── tcpdf/                    # TCPDF Library
├── uploads/                  # Temporäre Dateien
├── img/                      # Bilder und Icons
├── 1-ueber_uns.html         # Über uns Seite
├── 2-contact.html           # Kontaktseite
└── README.md                # Diese Dokumentation
```

## 🎯 Verwendung

### 1. Buch erstellen
1. **Daten eingeben**: Titel, Autor, Verlag und Hauptthema
2. **Kapitel definieren**: Themen zeilenweise eingeben
3. **Inhalte generieren**: KI erstellt automatisch alle Inhalte
4. **E-Book erstellen**: PDF wird mit modernem Design generiert

### 2. Workflow
```
Benutzereingabe → KI-Inhaltsgenerierung → PDF-Erstellung → Download
```

### 3. Generierte Inhalte
- **Vorwort**: Einführung zum Hauptthema
- **Kapitel**: Strukturierte Inhalte für jedes Thema
- **Nachwort**: Abschließende Betrachtungen
- **Inhaltsverzeichnis**: Automatische Navigation
- **Cover-Bild**: KI-generiertes Titelbild

## 🎨 Design-Features

### Moderne UI-Elemente
- **Gradient Backgrounds**: Attraktive Farbverläufe
- **Glassmorphism**: Moderne Transparenz-Effekte
- **Smooth Animations**: Flüssige Übergänge und Hover-Effekte
- **Responsive Grid**: Flexible Layouts für alle Bildschirmgrößen

### PDF-Design
- **Moderne Typografie**: Inter Font für optimale Lesbarkeit
- **Strukturierte Layouts**: Klare Hierarchie und Abstände
- **Professionelle Formatierung**: Seitenumbrüche und Margins
- **Farbkodierung**: Konsistente Farbpalette

## 🔧 Installation & Setup

### Voraussetzungen
- PHP 7.4+
- Web Server (Apache/Nginx)
- cURL Extension
- Schreibrechte für `/uploads/` Verzeichnis

### Installation
1. **Dateien hochladen**: Alle Projektdateien auf den Server kopieren
2. **Berechtigungen setzen**: Schreibrechte für Uploads-Verzeichnis
3. **TCPDF konfigurieren**: Library ist bereits enthalten
4. **API-Keys konfigurieren**: ChatGPT-Integration einrichten

### Konfiguration
```php
// generate_book.php - Timeout-Einstellungen
ini_set('default_socket_timeout', 1200);
set_time_limit(0);
```

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1200px - Vollständige Funktionalität
- **Tablet**: 768px - 1200px - Angepasstes Layout
- **Mobile**: < 768px - Optimierte Mobile-Ansicht

### Mobile-Features
- **Touch-optimiert**: Große Buttons und Touch-Targets
- **Gestapeltes Layout**: Vertikale Anordnung für kleine Bildschirme
- **Optimierte Typografie**: Angepasste Schriftgrößen

## 🔒 Sicherheit & Performance

### Sicherheitsmaßnahmen
- **Input Validation**: Validierung aller Benutzereingaben
- **File Cleanup**: Automatische Bereinigung alter Dateien
- **Timeout Handling**: Robuste Fehlerbehandlung
- **Secure Headers**: Moderne Security-Headers

### Performance-Optimierungen
- **Lazy Loading**: Progressive Inhaltsladung
- **Caching**: Temporäre Dateispeicherung
- **Compression**: Optimierte Bildkompression
- **Minification**: Komprimierte CSS/JS-Dateien

## 🚀 Zukünftige Erweiterungen

### Geplante Features
- **Mehrsprachige Unterstützung**: Internationale Sprachen
- **Template-System**: Verschiedene E-Book-Designs
- **Cloud-Integration**: Speicherung in der Cloud
- **Analytics**: Nutzungsstatistiken und Insights
- **API-Interface**: RESTful API für externe Integration

### Technische Verbesserungen
- **Progressive Web App**: PWA-Funktionalität
- **Offline-Support**: Lokale Verarbeitung
- **Real-time Collaboration**: Gemeinsame Bearbeitung
- **Advanced AI**: Erweiterte KI-Features

## 📞 Support & Kontakt

### Entwickler
- **Dipl.-Ing. (FH) Dominic Bilke**
- **Web- und Softwareentwicklung**
- **Website**: [www.web-software-entwicklung.de](https://www.web-software-entwicklung.de)
- **E-Mail**: info@web-software-entwicklung.de

### Technologien
- PHP, SQL, HTML, CSS, JavaScript
- WordPress, Typo3, C++, Python
- Moderne Web-Technologien

## 📄 Lizenz

© 2024 Modern Book Generator. Erstellt mit ❤️ und KI.

---

**Modern Book Generator** - Die Zukunft der E-Book-Erstellung mit künstlicher Intelligenz. 