# Book Generator - AI-Powered E-Book Creation

A modern, AI-powered book generator that creates professional e-books with ChatGPT-generated content and Unsplash images. The system runs entirely on `buchgenerator.bilke-projects.com` with local Python AI integration.

## 🚀 Features

- **AI-Powered Content Generation**: Uses OpenAI GPT-4 for intelligent book content creation
- **Professional PDF Generation**: Creates beautifully formatted PDFs with TCPDF
- **Image Integration**: Automatically finds relevant images using Unsplash API
- **Multi-language Support**: Supports German and other languages
- **Modern UI**: Clean, responsive web interface
- **Complete Book Structure**: Generates title, table of contents, chapters, and afterword
- **Local Processing**: All AI processing happens locally on the server

## 🏗️ Architecture

The system consists of:

- **Frontend**: Modern HTML/CSS/JavaScript interface
- **Backend**: PHP scripts for web handling and PDF generation
- **AI Engine**: Python scripts using OpenAI APIs for content generation
- **Image Service**: Unsplash API for high-quality stock photos
- **PDF Engine**: TCPDF for professional PDF creation

## 📁 Project Structure

```
buchgenerator.bilke-projects.com/
├── ai_generator.py          # Main AI content generator
├── ai_generator_v2.py       # Enhanced AI generator with Unsplash
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

- Python 3.7+
- PHP 7.4+
- OpenAI API key
- Unsplash API key (optional, uses fallback images if not provided)

### Setup Steps

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   python setup.py
   ```
   This creates a `.env` file. Edit it and add your API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   UNSPLASH_API_KEY=your-unsplash-api-key-here
   ```

4. **Get API Keys**:
   - **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Unsplash API Key**: Get from [Unsplash Developers](https://unsplash.com/developers) (optional)

5. **Test the system**:
   ```bash
   python test_system.py
   ```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `UNSPLASH_API_KEY`: Your Unsplash API key (optional)
- `OPENAI_MODEL`: GPT model to use (default: gpt-4)
- `OPENAI_MAX_TOKENS`: Maximum tokens per request (default: 2000)
- `OPENAI_TEMPERATURE`: Creativity level (default: 0.7)

### Image Generation

The system now uses Unsplash API instead of DALL-E for image generation:

- **With Unsplash API Key**: Searches for relevant high-quality stock photos
- **Without Unsplash API Key**: Uses Picsum Photos as fallback for placeholder images
- **Smart Query Conversion**: Automatically converts DALL-E prompts to Unsplash search terms

## 📖 Usage

### Web Interface

1. Open `index.html` in your browser
2. Enter author name and topics
3. Select language
4. Click "Generate Book"
5. Download the generated PDF

### Command Line

```bash
# Generate text
python ai_generator.py text "Write about artificial intelligence"

# Generate image (now uses Unsplash)
python ai_generator.py image "professional business meeting"

# Generate complete book
python ai_generator.py book "John Doe" "AI, Machine Learning, Data Science" "English"
```

## 🔄 API Endpoints

- `ask.php` - Text generation
- `topic.php` - Topic-based content generation
- `image_1.php` - Image generation (now uses Unsplash)
- `fetch_book_data.php` - Book data retrieval
- `generate_book.php` - PDF generation

## 📝 Features

### Content Generation
- **Smart Prompts**: Automatically generates appropriate prompts based on topics
- **Multi-language**: Supports German, English, and other languages
- **Structured Content**: Creates well-organized chapters with proper formatting
- **Professional Tone**: Maintains consistent, professional writing style

### Image Integration
- **Unsplash Integration**: Uses high-quality stock photos from Unsplash
- **Smart Search**: Converts content prompts to relevant image searches
- **Fallback System**: Uses placeholder images if Unsplash is unavailable
- **Orientation Detection**: Automatically selects landscape for covers, portrait for chapters

### PDF Generation
- **Professional Layout**: Clean, book-like formatting
- **Image Integration**: Properly sized and positioned images
- **Table of Contents**: Auto-generated with page numbers
- **Multiple Formats**: Supports different page sizes and orientations

## 🚀 Deployment

The system is designed to run on any web server with PHP and Python support:

1. Upload all files to your web server
2. Ensure Python 3.7+ is installed
3. Install Python dependencies
4. Configure environment variables
5. Set proper permissions for uploads directory

## 🔒 Security

- API keys are stored in environment variables
- Input validation on all endpoints
- Error handling prevents information leakage
- Secure file handling for uploads

## 📊 Performance

- **Caching**: Implemented for repeated requests
- **Async Processing**: Non-blocking image and content generation
- **Optimized Images**: Automatic image optimization for web
- **Efficient PDF Generation**: Streamlined PDF creation process

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation
- Review the test files
- Check the logs in `ai_generator.log`

## 🔄 Changelog

### Version 2.0.0
- **Major Update**: Replaced DALL-E with Unsplash API for image generation
- **Improved**: Better image quality and relevance
- **Added**: Fallback image system using Picsum Photos
- **Enhanced**: Smart prompt-to-search query conversion
- **Updated**: All documentation and setup files

### Version 1.0.0
- Initial release with DALL-E integration
- Basic book generation functionality
- PDF generation with TCPDF 