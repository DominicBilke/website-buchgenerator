# Modern Book Generator

Ein moderner Buchgenerator, der mit Hilfe von ChatGPT und TCPDF professionelle E-Books erstellt.

## 🚀 Features

- **Moderne UI**: Sauberes, responsives Design
- **KI-gestützte Inhaltsgenerierung**: Verwendet ChatGPT für Vorwort, Kapitel und Nachwort
- **Automatische Bildgenerierung**: Erstellt Buchcover mit DALL-E
- **Professionelle PDF-Erstellung**: Verwendet TCPDF für hochwertige E-Books
- **Mehrsprachige Unterstützung**: Deutsch und Englisch
- **Echtzeit-Fortschritt**: Live-Updates während der Generierung

## 🛠️ Technologie-Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: PHP 8.0+
- **PDF-Generierung**: TCPDF
- **ChatGPT API**: Inhaltsgenerierung via `bookgpt.bilke-projects.com`
- **DALL-E API**: Bildgenerierung für Buchcover

## 📋 Voraussetzungen

- PHP 8.0 oder höher
- TCPDF Bibliothek
- cURL Extension
- Schreibrechte für den `uploads/` Ordner
- Internetverbindung für API-Calls

## 🚀 Installation

1. **Repository klonen**:
   ```bash
   git clone <repository-url>
   cd buchgenerator.dominic-bilke.de
   ```

2. **Dependencies installieren**:
   ```bash
   composer require tecnickcom/tcpdf
   ```

3. **Ordnerberechtigungen setzen**:
   ```bash
   chmod 755 uploads/
   chmod 644 *.php *.html *.css *.js
   ```

4. **Webserver konfigurieren**:
   - Apache/Nginx auf das Verzeichnis zeigen
   - PHP 8.0+ aktivieren
   - cURL Extension aktivieren

## 🎯 Verwendung

### 1. Buchdetails eingeben

Öffnen Sie `index.html` und füllen Sie das Formular aus:

- **Autor**: Name des Buchautors
- **Themen**: Komma-getrennte Liste der Buchthemen
- **Sprache**: Deutsch oder Englisch

### 2. Buch generieren

Klicken Sie auf "Buch generieren" und verfolgen Sie den Fortschritt:

1. **Vorwort generieren** (via ChatGPT)
2. **Kapitel generieren** (für jedes Thema)
3. **Nachwort generieren** (via ChatGPT)
4. **Buchcover erstellen** (via DALL-E)
5. **PDF zusammenstellen** (via TCPDF)

### 3. Download

Das fertige E-Book wird automatisch zum Download bereitgestellt.

## 📁 Projektstruktur

```
buchgenerator.dominic-bilke.de/
├── index.html              # Hauptseite mit Buchgenerator
├── modern-style.css        # Moderne CSS-Styles
├── script.js               # JavaScript für UI-Interaktionen
├── generate_book.php       # PDF-Generierung mit TCPDF
├── fetch_book_data.php     # API-Calls zu ChatGPT
├── uploads/                # Temporäre Dateien
├── 1-ueber_uns.html        # Über uns Seite
├── 2-contact.html          # Kontaktseite
└── README.md               # Diese Datei
```

## 🔧 Konfiguration

### API-Endpoints

Die Anwendung verwendet folgende Endpoints von `bookgpt.bilke-projects.com`:

- `ask.php` - Textgenerierung (Vorwort/Nachwort)
- `topic.php` - Kapitelgenerierung
- `image_1.php` - Bildgenerierung

### Anpassungen

#### PDF-Layout anpassen

Bearbeiten Sie `generate_book.php`:

```php
// PDF-Einstellungen
$pdf = new TCPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);

// Schriftart und Größe
$pdf->SetFont('helvetica', '', 12);

// Seitenränder
$pdf->SetMargins(20, 20, 20);
```

#### UI anpassen

Bearbeiten Sie `modern-style.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --accent-color: #3b82f6;
}
```

## 🐛 Troubleshooting

### Häufige Probleme

1. **PDF wird nicht generiert**:
   - Prüfen Sie TCPDF Installation
   - Schreibrechte für `uploads/` Ordner
   - PHP-Fehlerprotokoll prüfen

2. **API-Calls schlagen fehl**:
   - Internetverbindung prüfen
   - Domain `bookgpt.bilke-projects.com` erreichbar?
   - cURL Extension aktiviert?

3. **Bilder werden nicht geladen**:
   - DALL-E API verfügbar?
   - Temporäre Dateien löschen

### Debug-Modus

Aktivieren Sie PHP-Fehlerprotokollierung:

```php
error_reporting(E_ALL);
ini_set('display_errors', 1);
```

## 🔒 Sicherheit

### Empfohlene Maßnahmen

1. **HTTPS verwenden**:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTPS} off
   RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
   ```

2. **Datei-Uploads einschränken**:
   ```php
   // Nur bestimmte Dateitypen erlauben
   $allowed_types = ['html', 'png', 'jpg', 'jpeg'];
   ```

3. **Rate Limiting**:
   ```php
   // Einfaches Rate Limiting
   session_start();
   if (isset($_SESSION['last_request']) && 
       time() - $_SESSION['last_request'] < 5) {
       die('Zu viele Anfragen');
   }
   $_SESSION['last_request'] = time();
   ```

## 📊 Performance

### Optimierungen

1. **Caching**:
   ```php
   // API-Responses cachen
   $cache_file = 'cache/' . md5($request) . '.json';
   if (file_exists($cache_file) && time() - filemtime($cache_file) < 3600) {
       return json_decode(file_get_contents($cache_file), true);
   }
   ```

2. **Asynchrone Verarbeitung**:
   ```javascript
   // AJAX für bessere UX
   fetch('/generate_book.php', {
       method: 'POST',
       body: formData
   }).then(response => response.json())
   ```

3. **Bildkomprimierung**:
   ```php
   // Bilder komprimieren
   $image = imagecreatefromstring($image_data);
   imagejpeg($image, $output_path, 85);
   ```

## 🚀 Deployment

### Production Setup

1. **Webserver konfigurieren**:
   ```apache
   <VirtualHost *:80>
       ServerName yourdomain.com
       DocumentRoot /var/www/buchgenerator
       
       <Directory /var/www/buchgenerator>
           AllowOverride All
           Require all granted
       </Directory>
   </VirtualHost>
   ```

2. **SSL-Zertifikat**:
   ```bash
   certbot --apache -d yourdomain.com
   ```

3. **Monitoring**:
   ```bash
   # Logs überwachen
   tail -f /var/log/apache2/error.log
   ```

## 🤝 Contributing

1. Fork das Repository
2. Feature Branch erstellen
3. Änderungen committen
4. Pull Request erstellen

## 📄 Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert.

## 🆘 Support

Bei Fragen und Problemen:
- Issue im Repository erstellen
- Kontakt: info@web-software-entwicklung.de
- Dokumentation: https://yourdomain.com/docs

---

**Modern Book Generator** - Powered by ChatGPT & TCPDF 