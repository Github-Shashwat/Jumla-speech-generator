import requests
import feedparser
from bs4 import BeautifulSoup
import yake
from typing import List, Dict
import streamlit as st

class NewsFetcher:
    def __init__(self):
        self.google_news_rss = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        
    def fetch_google_news(self, max_articles: int = 20) -> List[Dict]:
        """Fetch news from Google News RSS feed"""
        try:
            feed = feedparser.parse(self.google_news_rss)
            articles = []
            
            for entry in feed.entries[:max_articles]:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else '',
                    'summary': entry.summary if hasattr(entry, 'summary') else entry.title
                })
            
            return articles
        except Exception as e:
            st.error(f"Error fetching Google News: {e}")
            return []
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords using YAKE"""
        try:
            kw_extractor = yake.KeywordExtractor(
                lan="en",
                n=3,
                dedupLim=0.7,
                top=max_keywords
            )
            keywords = kw_extractor.extract_keywords(text)
            return [kw[1] for kw in keywords]
        except Exception as e:
            st.error(f"Error extracting keywords: {e}")
            return []
    
    def get_trending_topics(self) -> List[str]:
        """Get trending topics from news articles"""
        articles = self.fetch_google_news()
        if not articles:
            return self.get_fallback_topics()
        
        # Combine all headlines
        all_headlines = " ".join([article['title'] for article in articles])
        
        # Extract keywords
        keywords = self.extract_keywords(all_headlines, max_keywords=15)
        
        # Create topic clusters manually (simplified approach)
        topics = []
        
        # Check for common political/news themes
        topic_keywords = {
            "Economic Policy": ["economy", "inflation", "budget", "tax", "employment", "gdp"],
            "International Relations": ["china", "pakistan", "usa", "border", "trade", "diplomacy"],
            "Social Issues": ["education", "healthcare", "poverty", "women", "farmer", "youth"],
            "Technology & Innovation": ["digital", "technology", "startup", "ai", "internet", "cyber"],
            "Infrastructure": ["road", "railway", "transport", "construction", "development", "smart city"],
            "Environment": ["pollution", "climate", "green", "renewable", "environment", "clean"],
            "Governance": ["corruption", "transparency", "democracy", "election", "policy", "reform"],
            "Security": ["terrorism", "defense", "army", "police", "security", "law and order"]
        }
        
        keyword_lower = [kw.lower() for kw in keywords]
        
        for topic_name, topic_kw in topic_keywords.items():
            if any(kw in " ".join(keyword_lower) for kw in topic_kw):
                topics.append(topic_name)
        
        # Add some keywords as direct topics if they're prominent
        for keyword in keywords[:5]:
            if len(keyword.split()) <= 2 and keyword.lower() not in [t.lower() for t in topics]:
                topics.append(keyword.title())
        
        return topics[:8] if topics else self.get_fallback_topics()
    
    def get_fallback_topics(self) -> List[str]:
        """Fallback topics if news fetching fails"""
        return [
            "Economic Growth",
            "Unemployment Crisis",
            "Farmer Protests",
            "Digital India",
            "Women's Safety",
            "Education Reform",
            "Healthcare System",
            "Infrastructure Development"
        ]
    
    def get_headlines_text(self) -> str:
        """Get all headlines as text for LLM processing"""
        articles = self.fetch_google_news()
        headlines = [article['title'] for article in articles]
        return "\n".join(headlines[:15])  # Limit to avoid token limits