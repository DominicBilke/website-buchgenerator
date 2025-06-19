# AskGPT Server - PHP Version

PHP implementation of the AskGPT server for the Modern Book Generator backend service.

## 📋 Requirements

- PHP 7.4 or higher
- cURL extension
- JSON extension
- OpenAI API key
- Web server (Apache/Nginx)

## 🛠️ Installation

### 1. Upload Files

Upload the PHP files to your web server directory:
```
/var/www/html/askgpt/
├── ask.php
├── topic.php
├── image_1.php
├── health.php
└── uploads/          # Create this directory
```

### 2. Set Environment Variables

Set your OpenAI API key as an environment variable:

**Apache (.htaccess):**
```apache
SetEnv OPENAI_API_KEY "your_openai_api_key_here"
```

**Nginx:**
```nginx
fastcgi_param OPENAI_API_KEY "your_openai_api_key_here";
```

**PHP (php.ini or .user.ini):**
```ini
env[OPENAI_API_KEY] = "your_openai_api_key_here"
```

### 3. Set Permissions

```bash
chmod 755 uploads/
chown www-data:www-data uploads/
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask.php` | GET | Generate text content |
| `/topic.php` | GET | Generate chapter content |
| `/image_1.php` | GET | Generate book cover image |
| `/health.php` | GET | Health check |

### Example Usage

```bash
# Generate text content
curl "https://askgpt.bilke-projects.com/ask.php?ask=Schreibe ein Vorwort über künstliche Intelligenz"

# Generate chapter content
curl "https://askgpt.bilke-projects.com/topic.php?ask=Maschinelles Lernen"

# Generate book cover image
curl "https://askgpt.bilke-projects.com/image_1.php?ask=Künstliche Intelligenz" -o cover.png

# Health check
curl "https://askgpt.bilke-projects.com/health.php"
```

## 🔒 Security

### Input Validation

- All inputs are validated for length (max 1000 characters)
- CORS headers are set for cross-origin requests
- Error messages are logged but don't expose sensitive information

### Rate Limiting

Consider implementing rate limiting at the web server level:

**Apache (.htaccess):**
```apache
<IfModule mod_ratelimit.c>
    <Location "/ask.php">
        SetOutputFilter RATE_LIMIT
        SetEnv rate-limit 10
    </Location>
</IfModule>
```

**Nginx:**
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location ~ \.php$ {
    limit_req zone=api burst=20 nodelay;
    # ... other configuration
}
```

## 📊 Monitoring

### Health Check Response

```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00+00:00",
    "openai_key_configured": true,
    "extensions": {
        "curl": true,
        "json": true
    },
    "uploads_writable": true,
    "server_info": {
        "php_version": "8.1.0",
        "server_software": "Apache/2.4.41",
        "memory_limit": "128M",
        "max_execution_time": "30"
    }
}
```

### Logging

All errors are logged to the PHP error log. Check your server's error log for debugging:

```bash
# Apache
tail -f /var/log/apache2/error.log

# Nginx
tail -f /var/log/nginx/error.log
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Not Set**
   ```bash
   # Check if environment variable is set
   php -r "echo getenv('OPENAI_API_KEY') ? 'Set' : 'Not set';"
   ```

2. **cURL Extension Missing**
   ```bash
   # Check if cURL is installed
   php -m | grep curl
   ```

3. **Uploads Directory Not Writable**
   ```bash
   # Check permissions
   ls -la uploads/
   chmod 755 uploads/
   ```

4. **Memory Limit Exceeded**
   ```ini
   # Increase memory limit in php.ini
   memory_limit = 256M
   ```

### Debug Mode

Enable error reporting for debugging:

```php
// Add to the top of any PHP file
error_reporting(E_ALL);
ini_set('display_errors', 1);
```

## 🚀 Performance

### Optimization Tips

1. **Enable OPcache**
   ```ini
   opcache.enable=1
   opcache.memory_consumption=128
   opcache.interned_strings_buffer=8
   opcache.max_accelerated_files=4000
   ```

2. **Use FastCGI**
   ```nginx
   location ~ \.php$ {
       fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
       fastcgi_index index.php;
       include fastcgi_params;
   }
   ```

3. **Enable Compression**
   ```apache
   <IfModule mod_deflate.c>
       AddOutputFilterByType DEFLATE text/plain
       AddOutputFilterByType DEFLATE application/json
   </IfModule>
   ```

## 🔄 Migration from Python

If you're migrating from the Python FastAPI version:

1. **Update URLs**: The endpoints remain the same
2. **Environment Variables**: Set `OPENAI_API_KEY` in your web server configuration
3. **File Structure**: Ensure the `uploads/` directory exists and is writable
4. **Testing**: Use the health check endpoint to verify everything is working

## 📝 API Documentation

### Request Parameters

All endpoints accept a GET parameter `ask` containing the prompt or topic.

### Response Formats

- **Text endpoints** (`ask.php`, `topic.php`): Return plain text
- **Image endpoint** (`image_1.php`): Returns PNG image data
- **Health endpoint** (`health.php`): Returns JSON

### Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing or invalid parameters)
- `500`: Server error (API issues, configuration problems)

## 🤝 Support

For support and questions:
- Check the health endpoint for system status
- Review server error logs
- Contact: info@web-software-entwicklung.de

---

**AskGPT Server PHP** - Simple, reliable PHP implementation for AI-powered content generation 