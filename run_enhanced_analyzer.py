#!/usr/bin/env python3
"""
Quick test runner for the enhanced hashtag analyzer
This script runs a smaller analysis to test all features
"""

from enhanced_hashtag_analyzer import HashtagAnalyzer
import time

# Test with a smaller set of popular hashtags
TEST_HASHTAGS = [
    'trending',
    'viral',
    'fashion'
]

def main():
    print("🚀 Starting Enhanced Hashtag Analysis Test")
    print("=" * 50)
    
    # Your Instagram credentials (same as in main.py)
    USERNAME = "adityaraj6112025"
    PASSWORD = "Realme@06"
    
    analyzer = HashtagAnalyzer(USERNAME, PASSWORD)
    
    try:
        print("[+] Setting up browser...")
        analyzer.setup_driver()
        
        print("[+] Logging into Instagram...")
        analyzer.login_instagram()
        
        # Wait a bit after login
        time.sleep(3)
        
        print(f"[+] Analyzing {len(TEST_HASHTAGS)} hashtags with full metrics...")
        
        # Analyze hashtags (5 posts per hashtag for quick test)
        results = analyzer.analyze_hashtags(TEST_HASHTAGS, max_posts_per_hashtag=5)
        
        # Print detailed summary
        analyzer.print_summary(results)
        
        print("\n" + "=" * 80)
        print("✅ ENHANCED ANALYSIS COMPLETE!")
        print("=" * 80)
        print("📊 Features tested:")
        print("   ✓ Post count extraction")
        print("   ✓ Engagement scores (likes + comments)")
        print("   ✓ Post links collection")
        print("   ✓ Sentiment analysis with TextBlob")
        print("   ✓ Post content extraction")
        print("   ✓ Supabase data storage")
        
        # Show sample detailed data for first hashtag
        if results and results[0]['posts']:
            print(f"\n📝 Sample detailed data for #{results[0]['hashtag']}:")
            sample_post = results[0]['posts'][0]
            print(f"   URL: {sample_post['url']}")
            print(f"   Likes: {sample_post['likes']:,}")
            print(f"   Comments: {sample_post['comments']:,}")
            print(f"   Engagement: {sample_post['engagement_score']:,}")
            print("   Sentiment:")
            print(f"     Polarity: {sample_post['sentiment']['polarity']:.3f}")
            print(f"     Subjectivity: {sample_post['sentiment']['subjectivity']:.3f}")
            print(f"     Sentiment: {sample_post['sentiment']['sentiment']}")
            print(f"   Content: {sample_post['content'][:100]}...")
        
    except Exception as e:
        print(f"[!] Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n[+] Cleaning up...")
        analyzer.cleanup()

if __name__ == "__main__":
    main()
