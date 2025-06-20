# AI Book Generator v2.0 - Complete Revamp

A modern, AI-powered book generation system that creates professional e-books with ChatGPT-generated content and DALL-E images. This is a complete revamp of the original system with improved architecture, better error handling, and cross-platform compatibility.

## 🚀 New Features in v2.0

### ✨ Enhanced User Experience
- **Modern UI**: Clean, responsive design with intuitive interface
- **Real-time Progress**: Visual progress tracking during book generation
- **Error Handling**: Comprehensive error messages and recovery
- **Cross-platform**: Works on Windows, macOS, and Linux

### 🔧 Improved Architecture
- **Centralized Configuration**: All settings in `config.php`
- **Better Error Handling**: Robust error catching and reporting
- **Modular Design**: Separated concerns for easier maintenance
- **Logging System**: Detailed logs for debugging and monitoring

### 🤖 Enhanced AI Integration
- **Retry Logic**: Automatic retry for failed API calls
- **Better Prompts**: Optimized prompts for higher quality content
- **Image Optimization**: Improved image generation and handling
- **Content Validation**: Better content structure and formatting

## 🏗️ System Architecture

```
buchgenerator.bilke-projects.com/
├── config.php                 # Centralized configuration
├── index_v2.html             # Modern web interface
├── generate_book_v2.php      # Enhanced book generation
├── ai_generator_v2.py        # Improved AI engine
├── requirements.txt          # Python dependencies
├── setup_v2.py              # Enhanced setup script
├── css/                     # Stylesheets
│   ├── style.css           # Main styles
│   └── document-style.css  # PDF styles
├── tcpdf/                  # PDF generation library
├── uploads/                # Generated files
└── logs/                   # Application logs
```

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.7+** with pip
- **PHP 7.4+** with extensions: curl, json, mbstring
- **OpenAI API Key** (required for AI features)
- **Web Server** (Apache/Nginx) or PHP built-in server

### 1. Clone/Download the Project

```bash
# Navigate to your web directory
cd /path/to/your/web/root
```

### 2. Set Up Python Environment

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use the enhanced setup script
python setup_v2.py
```

### 3. Configure OpenAI API

Set your OpenAI API key as an environment variable:

```bash
# Linux/macOS
export OPENAI_API_KEY="your-openai-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-openai-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=your-openai-api-key-here
```

Or create a `.env` file:

```bash
# Create .env file
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### 4. Set Permissions

```bash
# Make Python scripts executable
chmod +x ai_generator_v2.py setup_v2.py

# Ensure directories are writable
chmod 755 uploads/
chmod 755 logs/
```

### 5. Test Installation

```bash
# Test the AI generator
python ai_generator_v2.py test

# Test with a sample book
python ai_generator_v2.py book "Test Author" "Artificial Intelligence" "English"
```

## 🎯 Usage

### Web Interface

1. Open `index_v2.html` in your browser
2. Fill in the book details:
   - **Author**: Your name or pen name
   - **Topics**: Main topics for the book (comma-separated)
   - **Language**: Preferred language
   - **Publisher**: Optional publisher name
3. Click "Generate Book" to create your e-book
4. Monitor progress in real-time
5. Download the generated PDF when complete

### Command Line

```bash
# Generate text
python ai_generator_v2.py text "Write about machine learning"

# Generate image
python ai_generator_v2.py image "A futuristic robot"

# Generate complete book
python ai_generator_v2.py book "John Doe" "AI, Machine Learning" "English"

# Test API connection
python ai_generator_v2.py test
```

## 🔧 Configuration

### AI Settings (config.php)

```php
// OpenAI settings
define('OPENAI_MODEL', 'gpt-4');
define('OPENAI_MAX_TOKENS', 2000);
define('OPENAI_TEMPERATURE', 0.7);
define('DALL_E_SIZE', '1024x1024');
```

### PDF Settings (config.php)

```php
// PDF settings
define('PDF_MARGIN_LEFT', 20);
define('PDF_MARGIN_TOP', 20);
define('PDF_MARGIN_RIGHT', 20);
define('PDF_MARGIN_BOTTOM', 20);
define('PDF_FONT_SIZE', 11);
define('PDF_FONT_NAME', 'freesans');
```

## 📊 Generated Content Structure

Each generated book includes:

1. **Cover Page**: Professional title page with author information
2. **Table of Contents**: Detailed chapter listing
3. **Chapters**: 8 comprehensive chapters with:
   - Engaging titles
   - Rich content (800-1200 words each)
   - Relevant AI-generated images
   - Professional formatting
4. **Afterword**: Author's final thoughts and acknowledgments

## 🔒 Security Features

- **Input Validation**: All user inputs are sanitized
- **File Upload Restrictions**: Secure file handling
- **Error Logging**: Comprehensive error tracking
- **Automatic Cleanup**: Old files are automatically removed
- **CORS Headers**: Proper web security headers

## 🐛 Troubleshooting

### Common Issues

1. **Python not found**
   ```bash
   # Check Python installation
   python --version
   python3 --version
   ```

2. **OpenAI API errors**
   ```bash
   # Test API connection
   python ai_generator_v2.py test
   ```

3. **Permission errors**
   ```bash
   # Fix directory permissions
   chmod 755 uploads/
   chmod 755 logs/
   ```

4. **PDF generation fails**
   - Check TCPDF installation
   - Verify file paths in config.php
   - Check PHP error logs

### Logs

Check the application logs:
```bash
# AI generator logs
tail -f logs/ai_generator.log

# PHP error logs
tail -f /var/log/apache2/error.log  # Apache
tail -f /var/log/nginx/error.log    # Nginx
```

## 📈 Performance

- **Content Generation**: 30-60 seconds per book
- **Image Generation**: 10-20 seconds per image
- **PDF Creation**: 5-10 seconds
- **Total Time**: 2-3 minutes for a complete book

## 🔄 Migration from v1.0

If you're upgrading from the original version:

1. **Backup your data**
   ```bash
   cp -r buchgenerator.bilke-projects.com buchgenerator_backup
   ```

2. **Update files**
   - Replace old files with new v2.0 versions
   - Keep your existing uploads directory

3. **Update configuration**
   - Review and update config.php settings
   - Set your OpenAI API key

4. **Test the system**
   ```bash
   python ai_generator_v2.py test
   ```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the logs in the `logs/` directory
3. Test individual components using the command line tools
4. Verify your OpenAI API key and quota

## 🎉 What's New in v2.0

### Major Improvements
- ✅ Modern, responsive web interface
- ✅ Real-time progress tracking
- ✅ Better error handling and user feedback
- ✅ Cross-platform compatibility
- ✅ Centralized configuration
- ✅ Enhanced AI prompts for better content
- ✅ Improved image generation
- ✅ Comprehensive logging system
- ✅ Automatic file cleanup
- ✅ Better PDF formatting

### Technical Enhancements
- ✅ Modular code architecture
- ✅ Retry logic for API calls
- ✅ Input validation and sanitization
- ✅ Better file handling
- ✅ Enhanced security features
- ✅ Performance optimizations

---

**Version**: 2.0.0  
**Last Updated**: December 2024  
**Compatibility**: Python 3.7+, PHP 7.4+, All major operating systems 