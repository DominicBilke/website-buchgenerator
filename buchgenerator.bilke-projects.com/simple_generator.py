#!/usr/bin/env python3
"""
Simple AI Content Generator for Book Generator
A working version that can be easily tested and improved
"""

import os
import sys
import json
import requests
import logging
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleAIGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt):
        """Generate text using OpenAI API"""
        try:
            url = f"{self.base_url}/chat/completions"
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a professional book writer."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            logging.info(f"Generated text: {len(content)} characters")
            return content
            
        except Exception as e:
            logging.error(f"Error generating text: {e}")
            raise
    
    def generate_image(self, prompt):
        """Generate image using DALL-E API"""
        try:
            url = f"{self.base_url}/images/generations"
            data = {
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
                "response_format": "url"
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            image_url = result['data'][0]['url']
            logging.info(f"Generated image: {image_url}")
            return image_url
            
        except Exception as e:
            logging.error(f"Error generating image: {e}")
            return ""
    
    def generate_book(self, author, topics, language="English"):
        """Generate a complete book"""
        try:
            logging.info(f"Starting book generation for {author} about {topics}")
            
            # Generate title
            title_prompt = f"Create a book title about {topics} by {author}. Return only the title."
            title = self.generate_text(title_prompt)
            
            # Generate chapters
            chapters = []
            for i in range(1, 6):  # Generate 5 chapters
                chapter_prompt = f"""Write a chapter {i} for a book titled "{title}" about {topics}.
                Language: {language}
                Make it engaging and informative. 500-800 words."""
                
                content = self.generate_text(chapter_prompt)
                
                # Generate image for chapter
                image_prompt = f"Create an illustration for a book chapter about {topics}"
                image_url = self.generate_image(image_prompt)
                
                chapters.append({
                    "title": f"Chapter {i}",
                    "content": content,
                    "image": image_url
                })
            
            # Generate afterword
            afterword_prompt = f"Write a short afterword for the book '{title}' by {author}."
            afterword = self.generate_text(afterword_prompt)
            
            book_data = {
                "title": title,
                "author": author,
                "topics": topics,
                "language": language,
                "chapters": chapters,
                "afterword": afterword,
                "generated_at": datetime.now().isoformat()
            }
            
            logging.info(f"Book generated successfully: {title}")
            return book_data
            
        except Exception as e:
            logging.error(f"Error generating book: {e}")
            raise
    
    def test_connection(self):
        """Test API connection"""
        try:
            result = self.generate_text("Hello, this is a test.")
            return True
        except:
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_generator.py <command> [args]")
        print("Commands: text <prompt>, image <prompt>, book <author> <topics>, test")
        return
    
    try:
        generator = SimpleAIGenerator()
        command = sys.argv[1]
        
        if command == "text" and len(sys.argv) >= 3:
            prompt = sys.argv[2]
            result = generator.generate_text(prompt)
            print(json.dumps({"text": result}, ensure_ascii=False, indent=2))
            
        elif command == "image" and len(sys.argv) >= 3:
            prompt = sys.argv[2]
            result = generator.generate_image(prompt)
            print(json.dumps({"image_url": result}, ensure_ascii=False, indent=2))
            
        elif command == "book" and len(sys.argv) >= 4:
            author = sys.argv[2]
            topics = sys.argv[3]
            language = sys.argv[4] if len(sys.argv) > 4 else "English"
            
            result = generator.generate_book(author, topics, language)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif command == "test":
            success = generator.test_connection()
            print(json.dumps({"success": success}, ensure_ascii=False, indent=2))
            
        else:
            print("Invalid command")
            
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main() 