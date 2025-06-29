# Quick Start Guide - AI Book Generator v2.0

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites
- Python 3.7 or higher
- PHP 7.4 or higher
- OpenAI API key (get one at https://platform.openai.com/)

### 2. Setup

#### Step 1: Install Python Dependencies
```bash
pip install requests openai python-dotenv
```

#### Step 2: Set OpenAI API Key
**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/macOS:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### Step 3: Test the System
```bash
python simple_generator.py test
```

### 3. Generate Your First Book

#### Option A: Web Interface
1. Open `simple_interface.html` in your browser
2. Fill in the form:
   - Author: Your name
   - Topics: "Artificial Intelligence, Machine Learning"
   - Language: English
3. Click "Generate Book"
4. Download the generated book

#### Option B: Command Line
```bash
python simple_generator.py book "Your Name" "AI, Machine Learning" "English"
```

### 4. Files Generated
- **HTML Book**: `uploads/book_[id].html` - View in browser
- **Images**: `uploads/image_[id].png` - Chapter illustrations
- **Logs**: `logs/ai_generator.log` - Debug information

## 🔧 Troubleshooting

### Common Issues

**1. "Python not found"**
```bash
# Check Python installation
python --version
python3 --version
```

**2. "OpenAI API key not found"**
- Make sure you set the environment variable correctly
- Check if the API key is valid at https://platform.openai.com/

**3. "Failed to execute Python script"**
- Make sure Python is in your PATH
- Try using `python3` instead of `python` on Linux/Mac

**4. "Permission denied"**
```bash
# Create directories with proper permissions
mkdir uploads logs
chmod 755 uploads logs
```

### Testing Individual Components

**Test text generation:**
```bash
python simple_generator.py text "Write about artificial intelligence"
```

**Test image generation:**
```bash
python simple_generator.py image "A futuristic robot"
```

**Test complete book:**
```bash
python simple_generator.py book "Test Author" "Technology" "English"
```

## 📁 File Structure

```
buchgenerator.bilke-projects.com/
├── simple_generator.py      # AI content generator
├── simple_generator.php     # Web API endpoint
├── simple_interface.html    # Web interface
├── config.php              # Configuration (auto-generated)
├── requirements.txt        # Python dependencies
├── uploads/                # Generated files
├── logs/                   # Application logs
└── README_v2.md           # Full documentation
```

## 🎯 What's New in v2.0

### ✅ Improvements
- **Simplified Setup**: No complex configuration needed
- **Better Error Handling**: Clear error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modern UI**: Clean, responsive web interface
- **Faster Generation**: Optimized prompts and processing
- **Better Logging**: Detailed logs for debugging

### 🔄 Migration from v1.0
1. **Backup your data**: Copy your existing uploads
2. **Use new files**: Replace old files with v2.0 versions
3. **Test the system**: Run the test commands above
4. **Update configuration**: Set your OpenAI API key

## 📞 Support

If you encounter issues:

1. **Check the logs**: Look at `logs/ai_generator.log`
2. **Test components**: Use the individual test commands
3. **Verify API key**: Make sure your OpenAI API key is valid
4. **Check permissions**: Ensure directories are writable

## 🎉 Success!

Once everything is working, you can:

- Generate books with AI-powered content
- Create custom images for each chapter
- Download professional-looking HTML books
- Scale up for production use

---

**Need help?** Check the full documentation in `README_v2.md` 