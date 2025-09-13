# Instagram Hashtag Analyzer

A comprehensive Instagram hashtag analysis tool that extracts post metrics, engagement scores, sentiment analysis, and post content for specific hashtags.

## Features

✅ **Post Count**: Get total number of posts for each hashtag  
✅ **Engagement Metrics**: Extract likes and comments for engagement scoring  
✅ **Post Links**: Collect direct URLs to analyzed posts  
✅ **Sentiment Analysis**: Analyze post content sentiment using TextBlob  
✅ **Post Content**: Extract captions and text content from posts  
✅ **Database Storage**: Save all data to Supabase for persistence  
✅ **Comprehensive Reporting**: Generate detailed analysis summaries  

## What the Tool Extracts

For each hashtag, the analyzer provides:

- **Total Post Count**: Number of posts using the hashtag
- **Individual Post Data**:
  - Post URL/Link
  - Like count
  - Comment count
  - Engagement score (likes + comments)
  - Post content/caption
  - Sentiment analysis (positive/negative/neutral with polarity scores)
- **Aggregate Metrics**:
  - Total engagement across all analyzed posts
  - Average engagement per post
  - Overall sentiment distribution
  - Top performing posts

## Installation

1. **Clone or download the files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install ChromeDriver**: Make sure you have Chrome browser and ChromeDriver installed
4. **Download TextBlob corpora** (first time only):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('brown')
   ```

## Configuration

### 1. Instagram Credentials
Update the credentials in `enhanced_hashtag_analyzer.py`:
```python
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"
```

### 2. Target Hashtags
Modify the `TARGET_HASHTAGS` list with hashtags you want to analyze:
```python
TARGET_HASHTAGS = [
    'trending',
    'viral',
    'fashion',
    'food',
    'travel',
    # Add your hashtags here
]
```

### 3. Supabase Setup (Optional)
If you want to store data in Supabase:
- Create a Supabase project
- Create a table called `hashtag_analysis` with these columns:
  - `id` (int8, primary key)
  - `hashtag` (text)
  - `post_count` (int8)
  - `total_engagement` (int8)
  - `engagement_rate` (float8)
  - `sentiment_polarity` (float8)
  - `sentiment_subjectivity` (float8)
  - `overall_sentiment` (text)
  - `posts_analyzed` (int8)
  - `posts_data` (jsonb)
  - `created_at` (timestamptz)

## Usage

### Basic Usage
```bash
python enhanced_hashtag_analyzer.py
```

### Customizing Analysis
You can modify these parameters in the script:
- `max_posts_per_hashtag`: Number of posts to analyze per hashtag (default: 15)
- `TARGET_HASHTAGS`: List of hashtags to analyze

## Output

The tool provides:

### Console Output
```
📊 HASHTAG ANALYSIS SUMMARY
================================================================================

#TRENDING
  📈 Total Posts: 1,234,567
  💝 Total Engagement: 45,678
  📊 Avg Engagement: 3,045
  🎭 Overall Sentiment: Positive
  📝 Posts Analyzed: 15
  🔥 Top Post: 12,456 engagement
     URL: https://instagram.com/p/ABC123/
```

### Supabase Data
All data is automatically saved to your Supabase database including:
- Hashtag metrics
- Individual post data (JSON format)
- Sentiment scores
- Timestamps

## Data Structure

### Individual Post Data
```json
{
  "url": "https://instagram.com/p/ABC123/",
  "likes": 1250,
  "comments": 89,
  "engagement_score": 1339,
  "content": "Amazing sunset today! #trending #photography",
  "sentiment": {
    "polarity": 0.625,
    "subjectivity": 0.6,
    "sentiment": "positive"
  }
}
```

### Hashtag Summary
```json
{
  "hashtag": "trending",
  "post_count": 1234567,
  "total_engagement": 45678,
  "engagement_rate": 3045.2,
  "average_sentiment": {
    "polarity": 0.234,
    "subjectivity": 0.456,
    "sentiment": "positive"
  },
  "posts": [/* array of individual posts */]
}
```

## Sentiment Analysis

The tool uses TextBlob for sentiment analysis, providing:
- **Polarity**: Range from -1 (negative) to 1 (positive)
- **Subjectivity**: Range from 0 (objective) to 1 (subjective)
- **Sentiment Label**: Categorized as positive, negative, or neutral

## Rate Limiting & Best Practices

The script includes built-in delays and human-like behavior:
- Random pauses between requests (3-10 seconds)
- Randomized user agent and browser settings
- Graceful error handling
- Automatic modal closing

## Troubleshooting

### Common Issues
1. **Login Failed**: Check your Instagram credentials
2. **ChromeDriver Error**: Ensure ChromeDriver is installed and in PATH
3. **Element Not Found**: Instagram may have changed their layout - selectors might need updating
4. **Rate Limited**: Reduce the number of hashtags or increase delays

### Tips
- Use a test Instagram account
- Don't analyze too many hashtags at once
- Monitor console output for errors
- Check Supabase logs if database insertion fails

## Legal & Ethical Considerations

- Respect Instagram's Terms of Service
- Use responsibly and don't overload their servers
- Consider the privacy of users whose posts you're analyzing
- This tool is for educational and research purposes

## Files Structure

```
├── enhanced_hashtag_analyzer.py    # Main analysis script
├── main.py                        # Original scraper (backup)
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your Instagram credentials
3. Ensure all dependencies are installed
4. Check if Instagram has changed their page structure
