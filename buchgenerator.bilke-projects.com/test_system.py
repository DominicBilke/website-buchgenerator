#!/usr/bin/env python3
"""
System Test Script for Book Generator v2.0
Tests all components to ensure they work correctly
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path

def print_test_header(test_name):
    """Print test header"""
    print(f"\n{'='*50}")
    print(f"🧪 Testing: {test_name}")
    print(f"{'='*50}")

def test_python_installation():
    """Test Python installation"""
    print_test_header("Python Installation")
    
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
        if version < (3, 7):
            print("❌ Python 3.7+ required")
            return False
        else:
            print("✅ Python version is compatible")
            return True
    except Exception as e:
        print(f"❌ Error checking Python: {e}")
        return False

def test_dependencies():
    """Test required Python packages"""
    print_test_header("Python Dependencies")
    
    required_packages = ['requests', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_openai_api():
    """Test OpenAI API connection"""
    print_test_header("OpenAI API")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        return False
    
    print("✅ OpenAI API key found")
    
    # Test API connection
    try:
        result = subprocess.run([
            sys.executable, "simple_generator.py", "test"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('success'):
                print("✅ OpenAI API connection successful")
                return True
            else:
                print("❌ OpenAI API test failed")
                return False
        else:
            print(f"❌ OpenAI API test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API test error: {e}")
        return False

def test_text_generation():
    """Test text generation"""
    print_test_header("Text Generation")
    
    try:
        result = subprocess.run([
            sys.executable, "simple_generator.py", "text", "Write a short paragraph about AI."
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'text' in data and len(data['text']) > 50:
                print("✅ Text generation successful")
                print(f"   Generated {len(data['text'])} characters")
                return True
            else:
                print("❌ Text generation failed - insufficient content")
                return False
        else:
            print(f"❌ Text generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Text generation error: {e}")
        return False

def test_image_generation():
    """Test image generation"""
    print_test_header("Image Generation")
    
    try:
        result = subprocess.run([
            sys.executable, "simple_generator.py", "image", "A simple robot"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'image_url' in data and data['image_url']:
                print("✅ Image generation successful")
                print(f"   Image URL: {data['image_url'][:50]}...")
                return True
            else:
                print("❌ Image generation failed - no URL returned")
                return False
        else:
            print(f"❌ Image generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return False

def test_book_generation():
    """Test complete book generation"""
    print_test_header("Book Generation")
    
    try:
        result = subprocess.run([
            sys.executable, "simple_generator.py", "book", "Test Author", "Technology", "English"
        ], capture_output=True, text=True, timeout=300)  # 5 minutes timeout
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'title' in data and 'chapters' in data and len(data['chapters']) > 0:
                print("✅ Book generation successful")
                print(f"   Title: {data['title']}")
                print(f"   Chapters: {len(data['chapters'])}")
                return True
            else:
                print("❌ Book generation failed - incomplete data")
                return False
        else:
            print(f"❌ Book generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Book generation error: {e}")
        return False

def test_directories():
    """Test directory structure"""
    print_test_header("Directory Structure")
    
    required_dirs = ['uploads', 'logs']
    missing_dirs = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"\n📁 Creating missing directories...")
        for directory in missing_dirs:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}")
    
    return True

def test_php_environment():
    """Test PHP environment"""
    print_test_header("PHP Environment")
    
    try:
        result = subprocess.run(['php', '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
            
            # Check if version is 7.4+
            if 'PHP 7.' in version_line or 'PHP 8.' in version_line:
                print("✅ PHP version is compatible")
                return True
            else:
                print("❌ PHP 7.4+ required")
                return False
        else:
            print("❌ PHP not found or not working")
            return False
            
    except Exception as e:
        print(f"❌ PHP test error: {e}")
        return False

def test_web_interface():
    """Test web interface files"""
    print_test_header("Web Interface")
    
    required_files = ['simple_interface.html', 'simple_generator.php']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ File exists: {file}")
        else:
            print(f"❌ File missing: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n📄 Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Book Generator v2.0 - System Test")
    print("=" * 60)
    
    tests = [
        ("Python Installation", test_python_installation),
        ("Dependencies", test_dependencies),
        ("Directory Structure", test_directories),
        ("OpenAI API", test_openai_api),
        ("Text Generation", test_text_generation),
        ("Image Generation", test_image_generation),
        ("Book Generation", test_book_generation),
        ("PHP Environment", test_php_environment),
        ("Web Interface", test_web_interface),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready to use.")
        print("\n📖 Next steps:")
        print("   1. Open simple_interface.html in your browser")
        print("   2. Generate your first book!")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("   1. Install missing Python packages: pip install requests openai")
        print("   2. Set OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("   3. Create missing directories: mkdir uploads logs")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 