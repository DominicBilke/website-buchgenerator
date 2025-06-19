# AskGPT Server

Backend service for the Modern Book Generator, providing AI-powered content generation using OpenAI's GPT and DALL-E APIs.

## 🚀 Features

- **Text Generation**: Generate preface, chapters, and afterword content using GPT-3.5-turbo
- **Image Generation**: Create book cover images using DALL-E
- **RESTful API**: Clean, documented API endpoints
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Nginx Integration**: Production-ready reverse proxy with SSL support
- **Health Monitoring**: Built-in health checks and monitoring

## 📋 Prerequisites

- Python 3.11+ (for local development)
- Docker & Docker Compose (for containerized deployment)
- OpenAI API Key
- Domain name (for production deployment)

## 🛠️ Installation

### Option 1: Docker Deployment (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd askgpt-server
   ```

2. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env and set your OPENAI_API_KEY
   ```

3. **Start with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Verify deployment**:
   ```bash
   curl http://localhost/health
   ```

### Option 2: Local Development

1. **Setup Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env and set your OPENAI_API_KEY
   ```

3. **Start server**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information |
| `/health` | GET | Health check |
| `/ask.php` | GET | Generate text content |
| `/topic.php` | GET | Generate chapter content |
| `/image_1.php` | GET | Generate book cover image |
| `/docs` | GET | API documentation |

### Example Usage

```bash
# Generate text content
curl "https://askgpt.bilke-projects.com/ask.php?ask=Schreibe ein Vorwort über künstliche Intelligenz"

# Generate chapter content
curl "https://askgpt.bilke-projects.com/topic.php?ask=Maschinelles Lernen"

# Generate book cover image
curl "https://askgpt.bilke-projects.com/image_1.php?ask=Künstliche Intelligenz" -o cover.png
```

## 🐳 Docker Deployment

### Production Deployment

1. **Build and start**:
   ```bash
   docker-compose up -d --build
   ```

2. **View logs**:
   ```bash
   docker-compose logs -f askgpt-server
   ```

3. **Stop services**:
   ```bash
   docker-compose down
   ```

### SSL Configuration

1. **Generate SSL certificates**:
   ```bash
   mkdir ssl
   # Add your SSL certificates to ssl/cert.pem and ssl/key.pem
   ```

2. **Update domain in nginx.conf**:
   ```bash
   # Edit nginx.conf and replace askgpt.bilke-projects.com with your domain
   ```

3. **Restart with SSL**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## 📊 Monitoring

### Health Check

```bash
curl https://askgpt.bilke-projects.com/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "openai_key_configured": true
}
```

### Logs

```bash
# Docker logs
docker-compose logs -f askgpt-server

# Nginx logs
docker-compose logs -f nginx
```

## 🔒 Security

### Rate Limiting

- API endpoints are rate-limited to 10 requests per second
- Burst allowance of 20 requests
- Configured in nginx.conf

### Security Headers

- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000

### CORS Configuration

Update CORS settings in `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Replace with actual domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🚀 Scaling

### Horizontal Scaling

1. **Multiple instances**:
   ```bash
   docker-compose up -d --scale askgpt-server=3
   ```

2. **Load balancer configuration**:
   Update nginx.conf to include multiple upstream servers

### Performance Optimization

- Enable Redis caching for API responses
- Implement request queuing for high load
- Use CDN for static file delivery

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   ```bash
   # Check environment variable
   echo $OPENAI_API_KEY
   
   # Verify in .env file
   cat .env
   ```

2. **Port Already in Use**:
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill process or change port
   ```

3. **SSL Certificate Issues**:
   ```bash
   # Check certificate validity
   openssl x509 -in ssl/cert.pem -text -noout
   ```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up
```

## 📝 API Documentation

Visit `https://askgpt.bilke-projects.com/docs` for interactive API documentation.

### Request Examples

```python
import requests

# Generate text
response = requests.get(
    "https://askgpt.bilke-projects.com/ask.php",
    params={"ask": "Schreibe ein Vorwort über KI"}
)
print(response.text)

# Generate image
response = requests.get(
    "https://askgpt.bilke-projects.com/image_1.php",
    params={"ask": "Künstliche Intelligenz"}
)
with open("cover.png", "wb") as f:
    f.write(response.content)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact: info@web-software-entwicklung.de
- Documentation: https://askgpt.bilke-projects.com/docs

---

**AskGPT Server** - Powered by OpenAI GPT and DALL-E APIs 