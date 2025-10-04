# Instagram Trending Hashtag Analyzer

A comprehensive Instagram hashtag analysis tool that discovers trending hashtags, extracts detailed post metrics, performs sentiment analysis, and provides engagement ratings. This project includes multiple analyzers and testing utilities for robust hashtag research.

## 🚀 Key Features

### Enhanced Analyzer ([enhanced_hashtag_analyzer.py](cci:7://file:///e:/instagram/enhanced_hashtag_analyzer.py:0:0-0:0))
✅ **Dynamic Trending Discovery**: Automatically discovers trending hashtags for 8 base topics  
✅ **Engagement Rating System**: 1-10 rating scale with emoji indicators (🔥📈📊📉💤)  
✅ **Advanced Sentiment Analysis**: TextBlob-powered sentiment analysis with polarity scores  
✅ **Topic-Based Analysis**: Analyzes 8 base topics (fashion, travel, food, fitness, art, technology, music, photography)  
✅ **Comprehensive Post Metrics**: Likes, comments, engagement scores, and content extraction  
✅ **Supabase Integration**: Automatic data storage with engagement ratings in `hashtag_ratings` table  
✅ **Smart Rate Limiting**: Human-like behavior with randomized delays (3-15 seconds)  

### Original Analyzer ([main.py](cci:7://file:///e:/instagram/main.py:0:0-0:0))
✅ **Direct Hashtag Analysis**: Analyze 8 specific predefined hashtags (trending, viral, fashion, photography, travel, foodie, fitness, art)  
✅ **Post Metrics Extraction**: Likes, comments, and engagement data  
✅ **Sentiment Analysis**: TextBlob sentiment analysis with polarity/subjectivity scores  
✅ **Database Storage**: Supabase integration with `hashtag_analysis` table  
✅ **Posts Per Hashtag**: 5 posts each (40 total posts analyzed)

## 📁 Project Structure
├── enhanced_hashtag_analyzer.py # 🔥 Main enhanced analyzer with trending discovery ├── main.py # 📊 Original hashtag analyzer (8 predefined hashtags) ├── run_enhanced_analyzer.py # 🧪 Quick test runner for enhanced analyzer ├── quick_test.py # ✅ TextBlob installation and setup checker ├── test_sentiment.py # 🎭 Sentiment analysis testing utility ├── requirements.txt # 📦 Python dependencies └── README.md # 📖 This documentation


## 🛠️ Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
Dependencies included:

selenium==4.15.0 - Web automation
textblob==0.17.1 - Sentiment analysis
supabase==2.0.2 - Database integration
webdriver-manager==4.0.1 - ChromeDriver management
requests==2.31.0 - HTTP requests
beautifulsoup4==4.12.2 - HTML parsing
pandas==2.1.3 - Data analysis
numpy==1.24.3 - Numerical computing
2. Install ChromeDriver
Download ChromeDriver from official site
Add to PATH or place in project directory
3. Setup TextBlob (First Time)
bash
python quick_test.py
This will automatically install TextBlob and download required corpora.

4. Test Sentiment Analysis
bash
python test_sentiment.py
⚙️ Configuration
Instagram Credentials
Update credentials in both 
enhanced_hashtag_analyzer.py
 and 
main.py
:

python
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"
Supabase Setup
Update Supabase configuration:

python
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
Required Supabase Tables
For Enhanced Analyzer - hashtag_ratings table:

sql
CREATE TABLE hashtag_ratings (
  id SERIAL PRIMARY KEY,
  hashtag TEXT,
  average_engagement_rating FLOAT,
  overall_sentiment TEXT,
  posts_data JSONB,
  post_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
For Original Analyzer - hashtag_analysis table:

sql
CREATE TABLE hashtag_analysis (
  id SERIAL PRIMARY KEY,
  hashtag TEXT,
  total_posts INTEGER,
  total_engagement INTEGER,
  average_engagement FLOAT,
  overall_sentiment TEXT,
  sentiment_polarity FLOAT,
  sentiment_subjectivity FLOAT,
  positive_posts_count INTEGER,
  negative_posts_count INTEGER,
  neutral_posts_count INTEGER,
  top_post_url TEXT,
  top_post_engagement INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
🚀 Usage
Enhanced Analyzer (Recommended)
Full Analysis - Dynamic Trending Discovery
bash
python enhanced_hashtag_analyzer.py
Analyzes 8 base topics: fashion, travel, food, fitness, art, technology, music, photography
Discovers 3 trending hashtags per topic (24 total hashtags)
Analyzes 10 posts per hashtag (240 total posts)
Provides engagement ratings and comprehensive metrics
Saves to hashtag_ratings table
Quick Test
bash
python run_enhanced_analyzer.py
Tests 3 hashtags: #trending, #viral, #fashion
Analyzes 5 posts per hashtag (15 total posts)
Perfect for testing setup and functionality
Original Analyzer
bash
python main.py
Analyzes 8 predefined hashtags: trending, viral, fashion, photography, travel, foodie, fitness, art
5 posts per hashtag analysis (40 total posts)
Saves to hashtag_analysis table
📊 What Each Tool Extracts
Enhanced Analyzer Output
📊 ANALYZING HASHTAG: #fashionista
============================================================
🔍 Fetching data from https://www.instagram.com/explore/tags/fashionista/...
📈 Found 2,456,789 total posts for #fashionista
🎯 Analyzing 10 posts for detailed metrics...

  1. Processing: Post #1
     ✓ Engagement: 3,245 (📈 High) - Likes: 2,890, Comments: 355
     ✓ Engagement Rating: 8/10 📈
     ✓ Sentiment: Positive (Polarity: 0.625)
     ✓ Post Content: Amazing street style look with vintage accessories...
     ✓ Instagram Link: https://instagram.com/p/ABC123/

============================================================
✅ HASHTAG #FASHIONISTA ANALYSIS COMPLETE!
📊 Posts Analyzed: 10
💝 Total Engagement: 28,456
📈 Average Engagement: 2,845
🎭 Overall Sentiment: Positive (Polarity: 0.234)
📈 Sentiment Distribution: 😊7 😐2 😢1
Data Structure
Individual Post Data
json
{
  "url": "https://instagram.com/p/ABC123/",
  "likes": 2890,
  "comments": 355,
  "engagement_score": 3245,
  "engagement_rating": 8,
  "content": "Amazing street style look with vintage accessories...",
  "sentiment": {
    "polarity": 0.625,
    "subjectivity": 0.6,
    "sentiment": "positive"
  }
}
Hashtag Summary
json
{
  "hashtag": "fashionista",
  "post_count": 2456789,
  "total_engagement": 28456,
  "engagement_rate": 2845.6,
  "average_sentiment": {
    "polarity": 0.234,
    "subjectivity": 0.456,
    "sentiment": "positive"
  },
  "posts": [/* array of individual posts */]
}
🎯 Engagement Rating System
The enhanced analyzer includes a 1-10 engagement rating system:

Rating	Engagement Score	Emoji	Description
10	5000+	🔥	Viral content
9	4000-4999	🔥	Extremely high
8	3000-3999	📈	Very high
7	2000-2999	📈	High
6	1500-1999	📊	Above average
5	1000-1499	📊	Average
4	700-999	📊	Below average
3	400-699	📉	Low
2	200-399	📉	Very low
1	<200	💤	Minimal
🎭 Sentiment Analysis
Uses TextBlob for comprehensive sentiment analysis:

Polarity: -1.0 (very negative) to +1.0 (very positive)
Subjectivity: 0.0 (objective) to 1.0 (subjective)
Categories: Positive (>0.1), Neutral (-0.1 to 0.1), Negative (<-0.1)
Test Sentiment Analysis
bash
python test_sentiment.py
Example output:

🎭 TESTING SENTIMENT ANALYSIS
==================================================

Test 1: I love this amazing product! It's absolutely fantastic! 😍
   📊 Polarity: 0.625 (-1=very negative, +1=very positive)
   📊 Subjectivity: 0.900 (0=objective, 1=subjective)
   🎭 Sentiment: POSITIVE 😊
🔍 Trending Discovery Algorithm
The enhanced analyzer discovers trending hashtags by:

Base Topic Analysis: Starts with 8 core topics
Related Hashtag Extraction: Scrapes related hashtags from topic pages
Fallback Variations: Uses predefined variations if discovery fails
Smart Filtering: Removes duplicates and irrelevant hashtags