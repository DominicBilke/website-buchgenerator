# Book Generator - AI-Powered E-Book Creation

A modern, AI-powered book generator that creates professional e-books with ChatGPT-generated content and DALL-E images. The system runs entirely on `buchgenerator.bilke-projects.com` with local Python AI integration.

## 🚀 Features

- **AI-Powered Content Generation**: Uses OpenAI GPT-4 for intelligent book content creation
- **Professional PDF Generation**: Creates beautifully formatted PDFs with TCPDF
- **Image Generation**: Automatically generates relevant images using DALL-E
- **Multi-language Support**: Supports German and other languages
- **Modern UI**: Clean, responsive web interface
- **Complete Book Structure**: Generates title, table of contents, chapters, and afterword
- **Local Processing**: All AI processing happens locally on the server

## 🏗️ Architecture

The system consists of:

- **Frontend**: Modern HTML/CSS/JavaScript interface
- **Backend**: PHP scripts for web handling and PDF generation
- **AI Engine**: Python scripts using OpenAI APIs for content generation
- **PDF Engine**: TCPDF for professional PDF creation

## 📁 Project Structure

```
buchgenerator.bilke-projects.com/
├── ai_generator.py          # Main AI content generator
├── setup.py                 # Setup and configuration script
├── requirements.txt         # Python dependencies
├── ask.php                  # Text generation endpoint
├── topic.php                # Topic-based content endpoint
├── image_1.php              # Image generation endpoint
├── fetch_book_data.php      # Book data fetching
├── generate_book.php        # PDF generation
├── index.html               # Main interface
├── css/                     # Stylesheets
├── tcpdf/                   # PDF generation library
├── uploads/                 # Generated files
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- PHP 7.4 or higher
- OpenAI API key
- Web server (Apache/Nginx)

### 1. Clone/Download the Project

```bash
# Navigate to your web directory
cd /path/to/your/web/root
```

### 2. Set Up Python Environment

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use the setup script
python3 setup.py
```

### 3. Configure OpenAI API

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or create a `.env` file:

```bash
# Create .env file
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### 4. Set Permissions

```bash
# Make Python scripts executable
chmod +x ai_generator.py setup.py

# Ensure uploads directory is writable
chmod 755 uploads/
```

### 5. Test Installation

```bash
# Test the AI generator
python3 ai_generator.py text "Hello, this is a test."
```

## 🎯 Usage

### Web Interface

1. Open `index.html` in your browser
2. Fill in the book details:
   - **Author**: Your name or pen name
   - **Topics**: Main topics for the book (comma-separated)
   - **Language**: Preferred language (default: German)
3. Click "Generate Book" to create your e-book
4. The system will:
   - Generate a compelling book title
   - Create a detailed table of contents
   - Write 8 comprehensive chapters
   - Generate relevant images for each chapter
   - Create an afterword
   - Compile everything into a professional PDF

### API Endpoints

The system provides several API endpoints for integration:

#### Text Generation
```bash
POST /ask.php
{
    "prompt": "Write about artificial intelligence"
}
```

#### Image Generation
```bash
POST /image_1.php
{
    "prompt": "A futuristic robot",
    "size": "1024x1024"
}
```

#### Complete Book Generation
```bash
POST /topic.php
{
    "author": "John Doe",
    "topic": "Machine Learning, AI, Data Science",
    "language": "German"
}
```

## 🔧 Configuration

### AI Settings

Edit the AI behavior in `ai_generator.py`:

```python
# Model settings
model = "gpt-4"              # or "gpt-3.5-turbo"
max_tokens = 2000            # Maximum response length
temperature = 0.7            # Creativity level (0.0-1.0)

# Image settings
image_size = "1024x1024"     # Image resolution
```

### PDF Settings

Customize PDF generation in `generate_book.php`:

```php
// Page settings
$pdf->SetMargins(20, 20, 20);
$pdf->SetAutoPageBreak(TRUE, 20);

// Font settings
$pdf->SetFont('freesans', 'B', 11);
```

## 📊 Generated Content Structure

Each generated book includes:

1. **Cover Page**: Professional title page with author information
2. **Table of Contents**: Detailed chapter listing
3. **Chapters**: 8 comprehensive chapters with:
   - Engaging titles
   - Rich content (800-1200 words each)
   - Relevant images
   - Professional formatting
4. **Afterword**: Author's final thoughts and acknowledgments

## 🔒 Security Considerations

- API keys are stored as environment variables
- Input validation on all endpoints
- File upload restrictions
- Automatic cleanup of old files
- CORS headers for web security

## 🐛 Troubleshooting

### Common Issues

1. **Python not found**
   ```bash
   # Ensure Python 3 is installed
   python3 --version
   ```

2. **OpenAI API errors**
   ```bash
   # Check API key
   echo $OPENAI_API_KEY
   ```

3. **Permission errors**
   ```bash
   # Fix uploads directory permissions
   chmod 755 uploads/
   ```

4. **PDF generation fails**
   - Check TCPDF installation
   - Verify file paths in `generate_book.php`

### Logs

Check the AI generator logs:
```bash
tail -f ai_generator.log
```

## 📈 Performance

- **Content Generation**: 30-60 seconds per book
- **Image Generation**: 10-20 seconds per image
- **PDF Creation**: 5-10 seconds
- **Total Time**: 2-3 minutes for a complete book

## 🔄 Updates

To update the system:

1. Backup your configuration
2. Update the Python scripts
3. Run the setup script again
4. Test with a sample book

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review the logs in `ai_generator.log`
3. Test individual components
4. Verify API key and permissions

## 📄 License

This project is proprietary software. All rights reserved.

---

**Version**: 2.0  
**Last Updated**: 2024  
**Server**: buchgenerator.bilke-projects.com 