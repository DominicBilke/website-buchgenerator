#!/usr/bin/env python3
"""
AI Content Generator for Book Generator v2.0
Enhanced version with better error handling, logging, and cross-platform compatibility
"""

import os
import sys
import json
import requests
import base64
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
from pathlib import Path
import time
import re

# Configure logging
def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'ai_generator.log', encoding='utf-8')
            # logging.StreamHandler(sys.stdout)
        ]
    )

class AIGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI Generator with OpenAI API key and Unsplash API key"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Unsplash API configuration
        self.unsplash_api_key = os.getenv('UNSPLASH_API_KEY')
        if not self.unsplash_api_key:
            logging.warning("UNSPLASH_API_KEY not found. Using fallback image URLs.")
        
        self.openai_base_url = "https://api.openai.com/v1"
        self.unsplash_base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        # Default settings
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        self.image_size = os.getenv('DALL_E_SIZE', '1024x1024')
        
        logging.info(f"AI Generator initialized with model: {self.model}")
    
    def _make_request(self, url: str, data: Dict, timeout: int = 60) -> Dict:
        """Make HTTP request with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=self.headers, json=data, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    logging.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    logging.error(f"Request failed after {max_retries} attempts: {e}")
                    raise
        
        # This should never be reached, but satisfies the type checker
        raise Exception("Request failed after all retry attempts")
    
    def generate_text(self, prompt: str, max_tokens: Optional[int] = None, 
                     temperature: Optional[float] = None) -> str:
        """Generate text using OpenAI GPT API"""
        try:
            url = f"{self.openai_base_url}/chat/completions"
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a professional book writer and content creator. Write engaging, informative, and well-structured content in the requested language."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature or self.temperature
            }
            
            result = self._make_request(url, data)
            content = result['choices'][0]['message']['content'].strip()
            logging.info(f"Generated text successfully, length: {len(content)}")
            return content
            
        except Exception as e:
            logging.error(f"Error generating text: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, size: Optional[str] = None) -> str:
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
            logging.error(f"Error getting Unsplash image: {str(e)}")
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
    
    def generate_book_content(self, author: str, topics: Union[str, List[str]], 
                            language: str = "German") -> Dict:
        """Generate complete book content including chapters and images"""
        try:
            # Normalize topics
            if isinstance(topics, str):
                topics = [topic.strip() for topic in topics.split(',')]
            
            topics = [t for t in topics if t]  # Remove empty topics
            
            if not topics:
                raise ValueError("At least one topic is required")
            
            logging.info(f"Starting book generation for author: {author}, topics: {topics}")
            
            # Generate book title
            title_prompt = f"""Create a compelling and professional book title for a book about {', '.join(topics)}. 
            Author: {author}. Language: {language}. 
            The title should be engaging and reflect the content accurately.
            Return only the title, no quotes or additional text."""
            
            book_title = self.generate_text(title_prompt, max_tokens=100, temperature=0.8)
            logging.info(f"Generated short book title: {book_title}")
            
            # Generate table of contents
            toc_prompt = f"""Create a detailed table of contents for a book titled "{book_title}" about {', '.join(topics)}. 
            Include 8 chapters with descriptive and engaging titles.
            Format as a numbered list using markdown:
            - Use 1. 2. 3. format for chapter numbers
            - Each chapter title on a new line
            - Make titles descriptive and engaging
            - No subtitles or subnumbers and no descriptions
            Language: {language}
            Make sure the chapters flow logically and cover the topics comprehensively."""
            
            table_of_contents = self.generate_text(toc_prompt, max_tokens=1000, temperature=0.7)
            logging.info("Generated table of contents")
            
            # Generate chapters
            chapters = []
            chapter_titles = self._extract_chapter_titles(table_of_contents)
            
            for i, chapter_title in enumerate(chapter_titles[:8], 1):
                logging.info(f"Generating chapter {i}: {chapter_title}")
                
                chapter_prompt = f"""Write a comprehensive and engaging chapter for the book "{book_title}" titled "{chapter_title}".
                Topics to cover: {', '.join(topics)}
                Language: {language}
                
                Requirements:
                - Make it engaging, informative, and well-structured
                - Use markdown formatting for better organization:
                  * Use ## for subheadings
                  * Use **bold** for emphasis
                  * Use *italic* for important terms
                  * Use bullet points (- or *) for lists
                  * Use numbered lists (1. 2. 3.) where appropriate
                  * Use > for important quotes or callouts
                - Length: 800-1200 words
                - Professional tone but accessible
                - Include practical examples where relevant
                - Ensure good flow and readability
                - Structure with clear sections and subsections"""
                
                chapter_content = self.generate_text(chapter_prompt, max_tokens=2000, temperature=0.7)
                
                # Generate image for chapter
                image_prompt = f"""Create a professional illustration about {chapter_title}. 
                Style: modern, clean, professional, relevant to the content.
                No text in image. High quality and visually appealing."""
                
                try:
                    chapter_image = self.generate_image(image_prompt)
                    logging.info(f"Generated image for chapter {i}")
                except Exception as e:
                    logging.warning(f"Failed to generate image for chapter {i}: {e}")
                    chapter_image = ""
                
                chapters.append({
                    "title": chapter_title,
                    "content": chapter_content,
                    "image": chapter_image,
                    "word_count": len(chapter_content.split())
                })
            
            # Generate afterword
            afterword_prompt = f"""Write a thoughtful and professional afterword for the book "{book_title}" by {author}.
            Language: {language}
            
            Use markdown formatting:
            - Use **bold** for emphasis
            - Use *italic* for personal reflections
            - Use bullet points (- or *) for acknowledgments
            - Use > for final thoughts or quotes
            
            Include:
            - Author's final thoughts and reflections
            - Acknowledgments
            - Call to action or closing thoughts
            - Professional tone but personal touch"""
            
            afterword = self.generate_text(afterword_prompt, max_tokens=800, temperature=0.7)
            logging.info("Generated afterword")
            
            # Generate cover image
            cover_prompt = f"""Create a professional book cover for '{book_title}' by {author}. 
            Style: modern, elegant, professional, suitable for a serious book.
            Include visual elements related to: {', '.join(topics)}
            Clean design with space for title and author name."""
            
            try:
                cover_image = self.generate_image(cover_prompt, size="1024x1024")
                logging.info("Generated cover image")
            except Exception as e:
                logging.warning(f"Failed to generate cover image: {e}")
                cover_image = ""
            
            # Calculate total word count
            total_words = sum(chapter.get('word_count', 0) for chapter in chapters)
            
            book_content = {
                "title": book_title,
                "author": author,
                "topics": topics,
                "language": language,
                "table_of_contents": table_of_contents,
                "chapters": chapters,
                "afterword": afterword,
                "cover_image": cover_image,
                "total_words": total_words,
                "chapter_count": len(chapters),
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0"
            }
            
            logging.info(f"Successfully generated complete book: {book_title} ({total_words} words)")
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
                    if char in '.- ':
                        continue
                    else:
                        title = line[i:].strip()
                        break
                if title:
                    titles.append(title)
        
        return titles[:8]  # Limit to 8 chapters
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            test_prompt = "Hello, this is a test message."
            self.generate_text(test_prompt, max_tokens=10)
            return True
        except Exception as e:
            logging.error(f"API connection test failed: {e}")
            return False

def main():
    """Main function for command line usage"""
    setup_logging()
    
    if len(sys.argv) < 2:
        print("Usage: python ai_generator_v2.py <command> [args]")
        print("Commands:")
        print("  text <prompt> - Generate text")
        print("  image <prompt> - Generate image")
        print("  book <author> <topics> [language] - Generate complete book")
        print("  test - Test API connection")
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
            topics = sys.argv[3]
            language = sys.argv[4] if len(sys.argv) > 4 else "German"
            
            result = generator.generate_book_content(author, topics, language)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif command == "test":
            success = generator.test_connection()
            print(json.dumps({"connection_test": success}, ensure_ascii=False, indent=2))
            
        else:
            print("Invalid command or missing arguments")
            
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main() 