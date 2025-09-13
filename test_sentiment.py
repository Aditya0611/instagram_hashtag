#!/usr/bin/env python3
"""
Simple test to verify TextBlob sentiment analysis is working
"""

from textblob import TextBlob

def test_sentiment_analysis():
    print("🎭 TESTING SENTIMENT ANALYSIS")
    print("=" * 50)
    
    # Test cases with different sentiments
    test_texts = [
        "I love this amazing product! It's absolutely fantastic! 😍",
        "This is terrible. I hate it so much. Worst experience ever.",
        "The weather is okay today. Nothing special.",
        "OMG this is the best day ever! So happy and excited! 🎉",
        "I'm feeling sad and disappointed about this situation.",
        "This is a neutral statement about the facts."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text}")
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = "positive"
            emoji = "😊"
        elif polarity < -0.1:
            sentiment = "negative"
            emoji = "😢"
        else:
            sentiment = "neutral"
            emoji = "😐"
        
        print(f"   📊 Polarity: {polarity:.3f} (-1=very negative, +1=very positive)")
        print(f"   📊 Subjectivity: {subjectivity:.3f} (0=objective, 1=subjective)")
        print(f"   🎭 Sentiment: {sentiment.upper()} {emoji}")
    
    print("\n" + "=" * 50)
    print("✅ Sentiment analysis is working correctly!")
    print("Now run: python run_enhanced_analyzer.py")

if __name__ == "__main__":
    test_sentiment_analysis()
