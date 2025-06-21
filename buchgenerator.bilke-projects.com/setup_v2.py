#!/usr/bin/env python3
"""
Enhanced Setup Script for Book Generator v2.0
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🚀 AI Book Generator v2.0 - Setup")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def detect_python_command():
    """Detect the correct Python command for the system"""
    system = platform.system().lower()
    
    if system == "windows":
        # Try different Python commands on Windows
        commands = ["python", "python3", "py"]
        for cmd in commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Python command detected: {cmd}")
                    return cmd
            except:
                continue
    else:
        # Unix-like systems
        commands = ["python3", "python"]
        for cmd in commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Python command detected: {cmd}")
                    return cmd
            except:
                continue
    
    print("❌ Python command not found")
    return None

def install_requirements():
    """Install required Python packages"""
    try:
        print("📦 Installing Python requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_openai_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY environment variable not set")
        print("   Please set it with one of the following methods:")
        print()
        print("   Windows (PowerShell):")
        print("   $env:OPENAI_API_KEY='your-api-key-here'")
        print()
        print("   Windows (Command Prompt):")
        print("   set OPENAI_API_KEY=your-api-key-here")
        print()
        print("   Linux/macOS:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
        print("   Or create a .env file with:")
        print("   OPENAI_API_KEY=your-api-key-here")
        return False
    print("✅ OpenAI API key found")
    return True

def create_env_file():
    """Create .env file template"""
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Unsplash API Configuration (for images)
UNSPLASH_API_KEY=your-unsplash-api-key-here

# Optional: Customize AI behavior
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Image generation settings
DALL_E_SIZE=1024x1024
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("   Please edit .env and add your OpenAI API key and Unsplash API key")
        print("   Get your Unsplash API key from: https://unsplash.com/developers")
    else:
        print("ℹ️  .env file already exists")

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"ℹ️  Directory exists: {directory}")

def test_ai_generator():
    """Test the AI generator with a simple prompt"""
    try:
        print("🧪 Testing AI generator...")
        result = subprocess.run([
            sys.executable, "simple_generator.py", "test"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                if data.get('success'):
                    print("✅ AI generator test successful")
                    return True
                else:
                    print("❌ AI generator test failed")
                    return False
            except json.JSONDecodeError:
                print("❌ AI generator returned invalid JSON")
                return False
        else:
            print(f"❌ AI generator test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ AI generator test timed out")
        return False
    except Exception as e:
        print(f"❌ AI generator test error: {e}")
        return False

def create_config_file():
    """Create configuration file for PHP"""
    config_content = """<?php
/**
 * Configuration file for Book Generator v2.0
 */

// Application settings
define('APP_NAME', 'AI Book Generator');
define('APP_VERSION', '2.0.0');
define('APP_DEBUG', true);

// File paths
define('ROOT_PATH', __DIR__);
define('UPLOADS_PATH', ROOT_PATH . '/uploads');
define('TCPDF_PATH', ROOT_PATH . '/tcpdf');

// Python settings
define('PYTHON_SCRIPT', ROOT_PATH . '/simple_generator.py');
define('PYTHON_COMMAND', 'python'); // Change to 'python3' on Linux/Mac

// OpenAI settings
define('OPENAI_MODEL', 'gpt-4');
define('OPENAI_MAX_TOKENS', 2000);
define('OPENAI_TEMPERATURE', 0.7);
define('DALL_E_SIZE', '1024x1024');

// Error reporting
if (APP_DEBUG) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Time limits
ini_set('max_execution_time', 1200);
ini_set('default_socket_timeout', 1200);
ini_set('post_max_size', '64M');
ini_set('upload_max_filesize', '64M');

// Create uploads directory if it doesn't exist
if (!is_dir(UPLOADS_PATH)) {
    mkdir(UPLOADS_PATH, 0755, true);
}
?>
"""
    
    if not os.path.exists('config.php'):
        with open('config.php', 'w') as f:
            f.write(config_content)
        print("✅ Created config.php")
    else:
        print("ℹ️  config.php already exists")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect Python command
    python_cmd = detect_python_command()
    if not python_cmd:
        print("❌ Please install Python and try again")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create configuration files
    create_env_file()
    create_config_file()
    
    # Check OpenAI key
    if not check_openai_key():
        print("\n📝 Setup incomplete - please set your OpenAI API key")
        print("   You can either:")
        print("   1. Set environment variable")
        print("   2. Edit the .env file and add your key")
        print("\n   After setting the API key, run this setup again to test.")
        return
    
    # Test AI generator
    if test_ai_generator():
        print("\n🎉 Setup completed successfully!")
        print("   The AI generator is ready to use.")
        print("\n📖 Next steps:")
        print("   1. Open simple_interface.html in your browser")
        print("   2. Fill in the form and generate your first book")
        print("   3. Check the uploads/ directory for generated files")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("   Please check the configuration and try again.")

if __name__ == "__main__":
    main() 