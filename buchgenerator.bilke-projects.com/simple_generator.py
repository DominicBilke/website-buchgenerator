#!/usr/bin/env python3
"""
Simple AI Generator for Book Generator
Handles text generation and image creation using OpenAI APIs and Unsplash
"""

import os
import sys
import json
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleAIGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Unsplash API configuration
        self.unsplash_api_key = os.getenv('UNSPLASH_API_KEY')
        if not self.unsplash_api_key:
            logging.warning("UNSPLASH_API_KEY not found. Using fallback image URLs.")
        
        self.base_url = "https://api.openai.com/v1"
        self.unsplash_base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt):
        """Generate text using OpenAI GPT API"""
        try:
            url = f"{self.base_url}/chat/completions"
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a professional book writer and content creator. Write engaging, informative, and well-structured content in the requested language."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            logging.info(f"Generated text successfully, length: {len(content)}")
            return content
            
        except Exception as e:
            logging.error(f"Error generating text: {e}")
            raise
    
    def generate_image(self, prompt):
        """Generate image using Unsplash API instead of DALL-E"""
        try:
            if not self.unsplash_api_key:
                # Fallback to placeholder images if no Unsplash API key
                return self._get_fallback_image(prompt)
            
            # Convert prompt to search terms for Unsplash
            search_query = self._convert_prompt_to_search_query(prompt)
            
            # Search for images on Unsplash
            url = f"{self.unsplash_base_url}/search/photos"
            headers = {
                "Authorization": f"Client-ID {self.unsplash_api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "query": search_query,
                "per_page": 1,
                "orientation": "landscape" if "cover" in prompt.lower() else "portrait"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result['results']:
                image_url = result['results'][0]['urls']['regular']
                logging.info(f"Found Unsplash image: {image_url}")
                return image_url
            else:
                logging.warning(f"No Unsplash images found for query: {search_query}")
                return self._get_fallback_image(prompt)
                
        except Exception as e:
            logging.error(f"Error getting Unsplash image: {e}")
            return self._get_fallback_image(prompt)
    
    def _convert_prompt_to_search_query(self, prompt: str) -> str:
        """Convert DALL-E prompt to Unsplash search query"""
        # Remove common DALL-E specific terms
        prompt = prompt.lower()
        prompt = prompt.replace("create a professional", "")
        prompt = prompt.replace("create a", "")
        prompt = prompt.replace("style: modern, clean, professional", "")
        prompt = prompt.replace("no text in image", "")
        prompt = prompt.replace("high quality and visually appealing", "")
        prompt = prompt.replace("suitable for a serious book", "")
        prompt = prompt.replace("clean design with space for title and author name", "")
        
        # Extract key terms
        words = prompt.split()
        # Keep only meaningful words (remove common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs'}
        
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Take first 3-5 meaningful words
        search_query = " ".join(meaningful_words[:5])
        
        # If no meaningful words, use a default
        if not search_query.strip():
            search_query = "professional business"
        
        logging.info(f"Converted prompt '{prompt}' to search query: '{search_query}'")
        return search_query
    
    def _get_fallback_image(self, prompt: str) -> str:
        """Get fallback image URL when Unsplash is not available"""
        # Use Picsum Photos as fallback
        import random
        seed = hash(prompt) % 1000
        return f"https://picsum.photos/800/600?random={seed}"
    
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