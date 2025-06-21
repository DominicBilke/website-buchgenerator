#!/usr/bin/env python3
"""
Test script for Unsplash integration
Tests the new image generation functionality using Unsplash API
"""

import os
import sys
import json
import requests

def test_unsplash_api():
    """Test Unsplash API connection and image search"""
    print("🧪 Testing Unsplash API Integration")
    print("=" * 50)
    
    # Check if API key is available
    unsplash_api_key = os.getenv('UNSPLASH_API_KEY')
    if not unsplash_api_key:
        print("❌ UNSPLASH_API_KEY not found in environment variables")
        print("   The system will use fallback images (Picsum Photos)")
        return False
    
    print(f"✅ Found Unsplash API key: {unsplash_api_key[:10]}...")
    
    try:
        # Test Unsplash API connection
        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {unsplash_api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "query": "business professional",
            "per_page": 1
        }
        
        print("🔍 Testing image search...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if result['results']:
            image_url = result['results'][0]['urls']['regular']
            print(f"✅ Successfully found image: {image_url}")
            print(f"   Image ID: {result['results'][0]['id']}")
            print(f"   Photographer: {result['results'][0]['user']['name']}")
            return True
        else:
            print("❌ No images found in search results")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Unsplash API: {e}")
        return False

def test_fallback_images():
    """Test fallback image system"""
    print("\n🔄 Testing Fallback Image System")
    print("=" * 50)
    
    try:
        # Test Picsum Photos fallback
        test_prompt = "professional business meeting"
        seed = hash(test_prompt) % 1000
        fallback_url = f"https://picsum.photos/800/600?random={seed}"
        
        print(f"🔍 Testing fallback URL: {fallback_url}")
        response = requests.get(fallback_url, timeout=10)
        response.raise_for_status()
        
        print("✅ Fallback image system working")
        return True
        
    except Exception as e:
        print(f"❌ Error testing fallback images: {e}")
        return False

def test_prompt_conversion():
    """Test DALL-E prompt to Unsplash search query conversion"""
    print("\n🔄 Testing Prompt Conversion")
    print("=" * 50)
    
    test_prompts = [
        "Create a professional illustration for a book chapter about artificial intelligence. Style: modern, clean, professional. No text in image.",
        "Create a professional book cover for 'Business Success' by John Doe. Style: modern, elegant, professional, suitable for a serious book.",
        "Create a professional illustration for a book chapter about machine learning. Style: modern, clean, professional, relevant to the content."
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}:")
        print(f"Original: {prompt[:80]}...")
        
        # Simulate the conversion logic
        converted = convert_prompt_to_search_query(prompt)
        print(f"Converted: {converted}")
        
        if converted and len(converted.split()) >= 2:
            print("✅ Conversion successful")
        else:
            print("❌ Conversion failed")

def convert_prompt_to_search_query(prompt: str) -> str:
    """Convert DALL-E prompt to Unsplash search query (simplified version)"""
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
    
    return search_query

def main():
    """Main test function"""
    print("🚀 Unsplash Integration Test Suite")
    print("=" * 60)
    
    # Test Unsplash API
    unsplash_working = test_unsplash_api()
    
    # Test fallback system
    fallback_working = test_fallback_images()
    
    # Test prompt conversion
    test_prompt_conversion()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    
    if unsplash_working:
        print("✅ Unsplash API: Working")
        print("   Images will be fetched from Unsplash")
    else:
        print("⚠️  Unsplash API: Not available")
        print("   Images will use fallback system")
    
    if fallback_working:
        print("✅ Fallback System: Working")
        print("   System will work even without Unsplash API")
    else:
        print("❌ Fallback System: Failed")
        print("   Check internet connection")
    
    print("\n🎯 Recommendations:")
    if not unsplash_working:
        print("- Get a free Unsplash API key from: https://unsplash.com/developers")
        print("- Add UNSPLASH_API_KEY to your .env file")
        print("- This will provide better quality and more relevant images")
    
    print("- The system will work with or without Unsplash API")
    print("- Fallback images ensure the system always functions")

if __name__ == "__main__":
    main() 