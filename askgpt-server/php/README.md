# BookGPT Server - PHP Version

PHP-basierte Backend-Implementierung für den Modern Book Generator mit OpenAI GPT und DALL-E Integration.

## 🚀 Features

- **Textgenerierung**: Vorwort, Kapitel und Nachwort via ChatGPT
- **Bildgenerierung**: Buchcover via DALL-E
- **RESTful API**: Einfache HTTP-Endpoints
- **Fehlerbehandlung**: Robuste Error-Handling
- **CORS-Support**: Cross-Origin Resource Sharing
- **Health Check**: Systemüberwachung

## 📋 Voraussetzungen

- PHP 8.0+
- cURL Extension
- OpenAI API Key
- Web Server (Apache/Nginx)

## 🛠️ Installation

### 1. Dateien hochladen

```bash
# Alle PHP-Dateien in das Web-Verzeichnis kopieren
cp *.php /var/www/html/bookgpt/
```

### 2. Umgebungsvariablen setzen

```bash
# .env Datei erstellen
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

### 3. Berechtigungen setzen

```bash
chmod 644 *.php
chmod 755 uploads/
```

## 🔧 Konfiguration

### Umgebungsvariablen

| Variable | Beschreibung | Beispiel |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API Schlüssel | `sk-...` |

### API-Endpoints

| Endpoint | Methode | Parameter | Beschreibung |
|----------|---------|-----------|--------------|
| `/ask.php` | GET | `ask` | Textgenerierung |
| `/topic.php` | GET | `ask` | Kapitelgenerierung |
| `/image_1.php` | GET | `ask` | Bildgenerierung |
| `/health.php` | GET | - | Systemstatus |

## 📖 Verwendung

### Text generieren

```bash
curl "https://bookgpt.bilke-projects.com/ask.php?ask=Schreibe ein Vorwort über künstliche Intelligenz"
```

### Kapitel generieren

```bash
curl "https://bookgpt.bilke-projects.com/topic.php?ask=Maschinelles Lernen"
```

### Bild generieren

```bash
curl "https://bookgpt.bilke-projects.com/image_1.php?ask=Künstliche Intelligenz" -o cover.png
```

### Health Check

```bash
curl "https://bookgpt.bilke-projects.com/health.php"
```

## 🔒 Sicherheit

### Empfohlene Maßnahmen

1. **HTTPS verwenden**:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTPS} off
   RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
   ```

2. **Rate Limiting**:
   ```apache
   # In .htaccess
   <IfModule mod_ratelimit.c>
       SetOutputFilter RATE_LIMIT
       SetEnv rate-limit 10
   </IfModule>
   ```

3. **Input Validation**:
   ```php
   // In jeder PHP-Datei
   $ask = filter_input(INPUT_GET, 'ask', FILTER_SANITIZE_STRING);
   if (empty($ask)) {
       http_response_code(400);
       die('Parameter "ask" ist erforderlich');
   }
   ```

## 🐛 Troubleshooting

### Häufige Probleme

1. **API Key Fehler**:
   ```bash
   # Prüfen Sie die Umgebungsvariable
   echo $OPENAI_API_KEY
   
   # Oder in PHP
   var_dump(getenv('OPENAI_API_KEY'));
   ```

2. **cURL Fehler**:
   ```bash
   # cURL Extension prüfen
   php -m | grep curl
   
   # Oder in PHP
   var_dump(extension_loaded('curl'));
   ```

3. **Berechtigungsfehler**:
   ```bash
   # Schreibrechte prüfen
   ls -la uploads/
   
   # Berechtigungen setzen
   chmod 755 uploads/
   ```

### Debug-Modus

```php
// Am Anfang jeder PHP-Datei
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('log_errors', 1);
ini_set('error_log', '/var/log/php_errors.log');
```

## 📊 Monitoring

### Logs überwachen

```bash
# PHP-Fehlerprotokoll
tail -f /var/log/php_errors.log

# Apache/Nginx Logs
tail -f /var/log/apache2/access.log
tail -f /var/log/nginx/access.log
```

### Health Check Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "openai_key_configured": true,
  "domain": "bookgpt.bilke-projects.com",
  "php_version": "8.1.0",
  "curl_available": true
}
```

## 🚀 Deployment

### Production Setup

1. **Webserver konfigurieren**:
   ```apache
   <VirtualHost *:80>
       ServerName bookgpt.bilke-projects.com
       DocumentRoot /var/www/bookgpt
       
       <Directory /var/www/bookgpt>
           AllowOverride All
           Require all granted
       </Directory>
   </VirtualHost>
   ```

2. **SSL-Zertifikat**:
   ```bash
   certbot --apache -d bookgpt.bilke-projects.com
   ```

3. **Monitoring einrichten**:
   ```bash
   # Cron-Job für Health Checks
   */5 * * * * curl -f https://bookgpt.bilke-projects.com/health.php || echo "Service down"
   ```

## 📝 API-Dokumentation

### Request-Format

Alle Endpoints erwarten GET-Requests mit Query-Parametern:

```
https://bookgpt.bilke-projects.com/endpoint.php?parameter=value
```

### Response-Format

- **Text-Endpoints**: Plain Text
- **Image-Endpoints**: Binary Image Data
- **Health-Endpoint**: JSON

### Error-Responses

```php
// 400 Bad Request
http_response_code(400);
echo "Parameter 'ask' ist erforderlich";

// 500 Internal Server Error
http_response_code(500);
echo "Fehler bei der API-Anfrage: " . $error_message;
```

## 🔄 Migration von Python

### Unterschiede

| Feature | Python (FastAPI) | PHP |
|---------|------------------|-----|
| Framework | FastAPI | Vanilla PHP |
| Performance | Höher | Geringer |
| Deployment | Docker | Traditional |
| Monitoring | Built-in | Manual |

### Migration Guide

1. **Endpoints identisch**: Gleiche URL-Struktur
2. **Parameter identisch**: Gleiche Query-Parameter
3. **Response identisch**: Gleiche Ausgabeformate

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
- Dokumentation: https://bookgpt.bilke-projects.com/docs

---

**BookGPT Server - PHP Version** - Powered by OpenAI GPT & DALL-E APIs 