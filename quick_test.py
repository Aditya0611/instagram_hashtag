#!/usr/bin/env python3
"""
Quick test to check if TextBlob is installed and working
"""

def check_textblob():
    try:
        from textblob import TextBlob
        print("✅ TextBlob is installed!")
        
        # Quick test
        test_text = "I love this amazing product! It's fantastic!"
        blob = TextBlob(test_text)
        print(f"📝 Test text: {test_text}")
        print(f"🎭 Sentiment: {blob.sentiment}")
        print("✅ TextBlob sentiment analysis working!")
        return True
        
    except ImportError:
        print("❌ TextBlob not installed. Installing now...")
        import subprocess
        import sys
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob"])
            print("✅ TextBlob installed successfully!")
            
            # Download required corpora
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('brown', quiet=True)
            print("✅ TextBlob corpora downloaded!")
            
            return True
        except Exception as e:
            print(f"❌ Failed to install TextBlob: {e}")
            return False

if __name__ == "__main__":
    print("🔍 Checking TextBlob installation...")
    if check_textblob():
        print("\n🚀 Ready to run enhanced Instagram analyzer!")
        print("Run: python run_enhanced_analyzer.py")
    else:
        print("\n❌ Please install TextBlob manually: pip install textblob")
