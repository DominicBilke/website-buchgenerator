#!/usr/bin/env python3
"""
AI Content Generator for Book Generator
Handles text generation and image creation using OpenAI APIs
"""

import os
import sys
import json
import requests
import base64
from typing import Dict, List, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_generator.log'),
        logging.StreamHandler()
    ]
)

class AIGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.openai_base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Generate text using OpenAI GPT API"""
        try:
            url = f"{self.openai_base_url}/chat/completions"
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a professional book writer and content creator. Write engaging, informative, and well-structured content."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            logging.info(f"Generated text successfully, length: {len(content)}")
            return content
            
        except Exception as e:
            logging.error(f"Error generating text: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """Generate image using OpenAI DALL-E API"""
        try:
            url = f"{self.openai_base_url}/images/generations"
            data = {
                "prompt": prompt,
                "n": 1,
                "size": size,
                "response_format": "url"
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            image_url = result['data'][0]['url']
            logging.info(f"Generated image successfully: {image_url}")
            return image_url
            
        except Exception as e:
            logging.error(f"Error generating image: {str(e)}")
            raise
    
    def generate_book_content(self, author: str, topics: List[str], language: str = "German") -> Dict:
        """Generate complete book content including chapters and images"""
        try:
            # Generate book title
            title_prompt = f"Create a compelling book title for a book about {', '.join(topics)}. Author: {author}. Language: {language}. Return only the title, no quotes."
            book_title = self.generate_text(title_prompt, max_tokens=100, temperature=0.8)
            
            # Generate table of contents
            toc_prompt = f"""Create a detailed table of contents for a book titled "{book_title}" about {', '.join(topics)}. 
            Include 8-12 chapters with descriptive titles. Format as a numbered list.
            Language: {language}"""
            table_of_contents = self.generate_text(toc_prompt, max_tokens=1000, temperature=0.7)
            
            # Generate chapters
            chapters = []
            chapter_titles = self._extract_chapter_titles(table_of_contents)
            
            for i, chapter_title in enumerate(chapter_titles[:8], 1):  # Limit to 8 chapters
                chapter_prompt = f"""Write a comprehensive chapter for the book "{book_title}" titled "{chapter_title}".
                Topics to cover: {', '.join(topics)}
                Language: {language}
                Make it engaging, informative, and well-structured with subheadings.
                Length: 800-1200 words."""
                
                chapter_content = self.generate_text(chapter_prompt, max_tokens=2000, temperature=0.7)
                
                # Generate image for chapter
                image_prompt = f"Create a professional illustration for a book chapter about {chapter_title}. Style: modern, clean, professional. No text in image."
                try:
                    chapter_image = self.generate_image(image_prompt)
                except:
                    chapter_image = ""  # Fallback if image generation fails
                
                chapters.append({
                    "title": chapter_title,
                    "content": chapter_content,
                    "image": chapter_image
                })
                
                logging.info(f"Generated chapter {i}: {chapter_title}")
            
            # Generate afterword
            afterword_prompt = f"""Write a thoughtful afterword for the book "{book_title}" by {author}.
            Language: {language}
            Include author's final thoughts and acknowledgments."""
            afterword = self.generate_text(afterword_prompt, max_tokens=800, temperature=0.7)
            
            # Generate cover image
            cover_prompt = f"Create a professional book cover for '{book_title}' by {author}. Style: modern, elegant, professional. Include title and author name."
            try:
                cover_image = self.generate_image(cover_prompt, size="1024x1024")
            except:
                cover_image = ""
            
            book_content = {
                "title": book_title,
                "author": author,
                "topics": topics,
                "language": language,
                "table_of_contents": table_of_contents,
                "chapters": chapters,
                "afterword": afterword,
                "cover_image": cover_image,
                "generated_at": datetime.now().isoformat()
            }
            
            logging.info(f"Successfully generated complete book: {book_title}")
            return book_content
            
        except Exception as e:
            logging.error(f"Error generating book content: {str(e)}")
            raise
    
    def _extract_chapter_titles(self, toc_text: str) -> List[str]:
        """Extract chapter titles from table of contents text"""
        lines = toc_text.split('\n')
        titles = []
        
        for line in lines:
            line = line.strip()
            if line and any(char.isdigit() for char in line[:3]):  # Lines starting with numbers
                # Remove numbering and clean up
                title = line
                for i, char in enumerate(line):
                    if char.isdigit() or char in '.- ':
                        continue
                    else:
                        title = line[i:].strip()
                        break
                if title:
                    titles.append(title)
        
        return titles[:8]  # Limit to 8 chapters

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python ai_generator.py <command> [args]")
        print("Commands:")
        print("  text <prompt> - Generate text")
        print("  image <prompt> - Generate image")
        print("  book <author> <topics> [language] - Generate complete book")
        return
    
    try:
        generator = AIGenerator()
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
            topics = sys.argv[3].split(',')
            language = sys.argv[4] if len(sys.argv) > 4 else "German"
            
            result = generator.generate_book_content(author, topics, language)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        else:
            print("Invalid command or missing arguments")
            
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main() 