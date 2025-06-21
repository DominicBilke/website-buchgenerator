#!/usr/bin/env python3
"""
Setup script for the Book Generator AI components
"""

import os
import sys
import subprocess
import json

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required Python packages"""
    try:
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
        print("   Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    print("✅ OpenAI API key found")
    return True

def test_ai_generator():
    """Test the AI generator with a simple prompt"""
    try:
        result = subprocess.run([
            sys.executable, "ai_generator.py", "text", "Hello, this is a test."
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                json.loads(result.stdout)
                print("✅ AI generator test successful")
                return True
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

def main():
    """Main setup function"""
    print("🚀 Setting up Book Generator AI Components")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Check OpenAI key
    if not check_openai_key():
        print("\n📝 Setup incomplete - please set your OpenAI API key")
        print("   You can either:")
        print("   1. Set environment variable: export OPENAI_API_KEY='your-key'")
        print("   2. Edit the .env file and add your key")
        return
    
    # Test AI generator
    if test_ai_generator():
        print("\n🎉 Setup completed successfully!")
        print("   The AI generator is ready to use.")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("   Please check the configuration and try again.")

if __name__ == "__main__":
    main() 