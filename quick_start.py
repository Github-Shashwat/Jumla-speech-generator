#!/usr/bin/env python3
"""
Quick Start Script for Satirical Campaign Speech Simulator
Run this to test the core functionality without Streamlit UI
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_news_fetcher():
    """Test news fetching functionality"""
    print("🔍 Testing News Fetcher...")
    try:
        from news_fetcher import NewsFetcher
        
        fetcher = NewsFetcher()
        topics = fetcher.get_trending_topics()
        
        print(f"✅ Found {len(topics)} trending topics:")
        for i, topic in enumerate(topics[:5], 1):
            print(f"   {i}. {topic}")
        
        return True
    except Exception as e:
        print(f"❌ News fetcher error: {e}")
        return False

def test_speech_generation():
    """Test speech generation with sample parameters"""
    print("\n🎤 Testing Speech Generation...")
    
    # Check for API keys
    groq_key = os.getenv('GROQ_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not groq_key and not openai_key:
        print("❌ No API keys found. Please set GROQ_API_KEY or OPENAI_API_KEY in .env file")
        return False
    
    try:
        from chains import SpeechGenerator
        
        # Use Groq if available, otherwise OpenAI
        if groq_key:
            generator = SpeechGenerator(groq_key, "groq")
            print("   Using Groq (Llama3-70B)")
        else:
            generator = SpeechGenerator(openai_key, "openai")
            print("   Using OpenAI (GPT-3.5-Turbo)")
        
        # Generate sample speech
        print("   Generating sample speech...")
        speech = generator.generate_speech(
            topic="Economic Growth",
            tone=7,
            blame="Opposition",
            freebies=5,
            hindutva=4,
            development=8
        )
        
        print(f"✅ Generated speech ({len(speech)} characters):")
        print(f"   \"{speech[:100]}...\"")
        
        # Generate critique
        print("   Generating critique...")
        critique = generator.critique_speech(speech)
        
        print(f"✅ Generated critique ({len(critique)} characters):")
        print(f"   \"{critique[:100]}...\"")
        
        return True
        
    except Exception as e:
        print(f"❌ Speech generation error: {e}")
        return False

def test_full_pipeline():
    """Test the complete pipeline"""
    print("\n🔄 Testing Full Pipeline...")
    
    try:
        from news_fetcher import NewsFetcher
        from chains import SpeechGenerator
        
        # Get API key
        api_key = os.getenv('GROQ_API_KEY') or os.getenv('OPENAI_API_KEY')
        provider = "groq" if os.getenv('GROQ_API_KEY') else "openai"
        
        if not api_key:
            print("❌ No API key available for full pipeline test")
            return False
        
        # Fetch topics
        fetcher = NewsFetcher()
        topics = fetcher.get_trending_topics()
        
        # Generate speech for first topic
        generator = SpeechGenerator(api_key, provider)
        result = generator.generate_speech_and_critique(
            topic=topics[0],
            tone=6,
            blame="Previous Government",
            freebies=4,
            hindutva=3,
            development=7
        )
        
        print(f"✅ Full pipeline test successful!")
        print(f"   Topic: {topics[0]}")
        print(f"   Speech length: {len(result['speech'])} characters")
        print(f"   Critique length: {len(result['critique'])} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 Satirical Campaign Speech Simulator - Quick Start Test")
    print("=" * 60)
    
    tests = [
        test_news_fetcher,
        test_speech_generation,
        test_full_pipeline
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! You're ready to run the full app:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("   Make sure you have:")
        print("   1. Valid API keys in .env file")
        print("   2. All dependencies installed (pip install -r requirements.txt)")
        print("   3. Internet connection for news fetching")

if __name__ == "__main__":
    main()