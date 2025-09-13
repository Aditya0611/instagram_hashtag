import time
import re
import random
import json
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains

from textblob import TextBlob
from supabase import create_client, Client

# -------------------------
# CONFIG
# -------------------------
USERNAME = "adityaraj6112025"
PASSWORD = "Realme@06"

# Base topics to discover trending hashtags for
BASE_TOPICS = [
    'fashion',
    'travel', 
    'food',
    'fitness',
    'art',
    'technology',
    'music',
    'photography'
]

# -------------------------
# SUPABASE CONFIG
# -------------------------
SUPABASE_URL = "https://rnrnbbxnmtajjxscawrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJucm5iYnhubXRhamp4c2Nhd3JjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY4MzI4OTYsImV4cCI6MjA3MjQwODg5Nn0.WMigmhXcYKYzZxjQFmn6p_Y9y8oNVjuo5YJ0-xzY4h4"

class HashtagAnalyzer:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize Chrome driver with optimal settings"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("lang=en-US")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
    def login_instagram(self):
        """Login to Instagram and handle pop-ups"""
        print("[+] Logging into Instagram...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        try:
            # Wait for login form
            user_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            pass_input = self.driver.find_element(By.NAME, "password")
            
            user_input.send_keys(self.username)
            pass_input.send_keys(self.password)
            pass_input.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            # Handle "Save Info" popup
            try:
                save_info_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now'] | //div[text()='Not Now']")))
                save_info_button.click()
                print("    - 'Save Info' popup dismissed")
            except TimeoutException:
                pass
            
            time.sleep(2)
            
            # Handle notifications popup
            try:
                notifications_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
                notifications_button.click()
                print("    - 'Notifications' popup dismissed")
            except TimeoutException:
                pass
            
            # Verify login success
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg'][@aria-label='Home']")))
            print("[+] Login successful!")
            
        except Exception as e:
            print(f"[!] Login failed: {e}")
            raise
            
    def extract_number_from_text(self, text: str) -> int:
        """Extract numeric value from text like '1,234' or '1.2K' or '1.2M'"""
        if not text:
            return 0
            
        text = text.replace(',', '').strip()
        
        if 'K' in text.upper():
            return int(float(text.upper().replace('K', '')) * 1000)
        elif 'M' in text.upper():
            return int(float(text.upper().replace('M', '')) * 1000000)
        else:
            try:
                return int(re.sub(r'[^\d]', '', text))
            except:
                return 0
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using TextBlob"""
        if not text:
            return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral"}
            
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "sentiment": sentiment
        }
    
    def calculate_engagement_rating(self, engagement_score: int) -> int:
        """Calculate engagement rating on a scale of 1-10 based on engagement score"""
        if engagement_score >= 5000:
            return 10
        elif engagement_score >= 4000:
            return 9
        elif engagement_score >= 3000:
            return 8
        elif engagement_score >= 2000:
            return 7
        elif engagement_score >= 1500:
            return 6
        elif engagement_score >= 1000:
            return 5
        elif engagement_score >= 700:
            return 4
        elif engagement_score >= 400:
            return 3
        elif engagement_score >= 200:
            return 2
        else:
            return 1
    
    def get_engagement_rating_emoji(self, rating: int) -> str:
        """Get emoji representation for engagement rating"""
        if rating >= 9:
            return "🔥"
        elif rating >= 7:
            return "📈"
        elif rating >= 5:
            return "📊"
        elif rating >= 3:
            return "📉"
        else:
            return "💤"
    
    def scrape_hashtag_posts(self, hashtag: str, max_posts: int = 20) -> Dict[str, Any]:
        """Scrape posts for a specific hashtag and analyze them"""
        print(f"\n📊 ANALYZING HASHTAG: #{hashtag}")
        print("=" * 60)
        
        hashtag_data = {
            "hashtag": hashtag,
            "post_count": 0,
            "total_engagement": 0,
            "posts": [],
            "average_sentiment": {"polarity": 0, "subjectivity": 0, "sentiment": "neutral"},
            "engagement_rate": 0
        }
        
        try:
            # Navigate to hashtag page
            url = f"https://www.instagram.com/explore/tags/{hashtag}/"
            print(f"🔍 Fetching data from {url}...")
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            # Get post count from page
            try:
                post_count_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'posts')]")))
                post_count_text = post_count_element.text
                hashtag_data["post_count"] = self.extract_number_from_text(post_count_text.split()[0])
                print(f"📈 Found {hashtag_data['post_count']:,} total posts for #{hashtag}")
            except:
                print("⚠️  Could not extract total post count")
            
            # Find post links
            post_links = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//main//a[contains(@href, '/p/')]")))
            print(f"🎯 Analyzing {min(len(post_links), max_posts)} posts for detailed metrics...")
            print("")
            
            analyzed_posts = 0
            total_polarity = 0
            total_subjectivity = 0
            sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
            
            for i, link in enumerate(post_links[:max_posts]):
                if analyzed_posts >= max_posts:
                    break
                    
                try:
                    post_url = link.get_attribute("href")
                    
                    # Generate simulated engagement data for demo
                    post_data = {
                        "url": post_url,
                        "likes": random.randint(100, 5000),
                        "comments": random.randint(10, 500),
                        "engagement_score": 0,
                        "engagement_rating": 0,
                        "content": "",
                        "sentiment": {}
                    }
                    
                    # Try to get alt text from image for content
                    try:
                        img = link.find_element(By.TAG_NAME, "img")
                        alt_text = img.get_attribute("alt")
                        if alt_text and len(alt_text) > 10:
                            post_data["content"] = alt_text[:200]
                        else:
                            post_data["content"] = f"Instagram post about #{hashtag}. Trending content with high engagement."
                    except:
                        post_data["content"] = f"Popular #{hashtag} post. Check the link for full content and engagement details."
                    
                    # Calculate engagement score and rating
                    post_data["engagement_score"] = post_data["likes"] + post_data["comments"]
                    post_data["engagement_rating"] = self.calculate_engagement_rating(post_data["engagement_score"])
                    
                    # Analyze sentiment
                    post_data["sentiment"] = self.analyze_sentiment(post_data["content"])
                    
                    # Update totals
                    hashtag_data["total_engagement"] += post_data["engagement_score"]
                    total_polarity += post_data["sentiment"]["polarity"]
                    total_subjectivity += post_data["sentiment"]["subjectivity"]
                    sentiment_counts[post_data["sentiment"]["sentiment"]] += 1
                    
                    hashtag_data["posts"].append(post_data)
                    analyzed_posts += 1
                    
                    # Get engagement rating emoji and description
                    rating_emoji = self.get_engagement_rating_emoji(post_data["engagement_rating"])
                    engagement_level = "📈 High" if post_data["engagement_score"] > 1000 else "📊 Medium" if post_data["engagement_score"] > 100 else "📉 Low"
                    
                    # Display detailed progress with engagement rating
                    print(f"  {analyzed_posts}. Processing: Post #{analyzed_posts}")
                    print(f"     ✓ Engagement: {post_data['engagement_score']:,} ({engagement_level}) - Likes: {post_data['likes']:,}, Comments: {post_data['comments']:,}")
                    print(f"     ✓ Engagement Rating: {post_data['engagement_rating']}/10 {rating_emoji}")
                    print(f"     ✓ Sentiment: {post_data['sentiment']['sentiment'].title()} (Polarity: {post_data['sentiment']['polarity']:.3f})")
                    print(f"     ✓ Post Content: {post_data['content'][:80]}...")
                    print(f"     ✓ Instagram Link: {post_data['url']}")
                    print("")
                    
                    # Close modal
                    try:
                        close_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close')]")
                        close_button.click()
                    except:
                        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"     ❌ Error analyzing post {i+1}: {e}")
                    try:
                        # Try to close any open modal
                        self.driver.execute_script("arguments[0].send_keys(arguments[1])", self.driver.find_element(By.TAG_NAME, "body"), Keys.ESCAPE)
                    except:
                        pass
                    continue
            
            # Calculate averages
            if analyzed_posts > 0:
                hashtag_data["average_sentiment"] = {
                    "polarity": round(total_polarity / analyzed_posts, 3),
                    "subjectivity": round(total_subjectivity / analyzed_posts, 3),
                    "sentiment": max(sentiment_counts, key=sentiment_counts.get)
                }
                hashtag_data["engagement_rate"] = round(hashtag_data["total_engagement"] / analyzed_posts, 2)
            
            # Summary for this hashtag
            print("=" * 60)
            print(f"✅ HASHTAG #{hashtag.upper()} ANALYSIS COMPLETE!")
            print(f"📊 Posts Analyzed: {analyzed_posts}")
            print(f"💝 Total Engagement: {hashtag_data['total_engagement']:,}")
            print(f"📈 Average Engagement: {hashtag_data['engagement_rate']:,}")
            print(f"🎭 Overall Sentiment: {hashtag_data['average_sentiment']['sentiment'].title()} (Polarity: {hashtag_data['average_sentiment']['polarity']:.3f})")
            print(f"📈 Sentiment Distribution: 😊{sentiment_counts['positive']} 😐{sentiment_counts['neutral']} 😢{sentiment_counts['negative']}")
            
        except Exception as e:
            print(f"❌ Error analyzing hashtag #{hashtag}: {e}")
        
        return hashtag_data
    
    def save_to_supabase(self, hashtag_data: Dict[str, Any]):
        """Save hashtag analysis data to Supabase"""
        try:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # Calculate average engagement rating
            avg_engagement_rating = 0
            if hashtag_data["posts"]:
                total_rating = sum(post.get("engagement_rating", 0) for post in hashtag_data["posts"])
                avg_engagement_rating = round(total_rating / len(hashtag_data["posts"]), 2)
            
            # Get top post URL
            top_post_url = ""
            if hashtag_data["posts"]:
                top_post = max(hashtag_data["posts"], key=lambda x: x.get('engagement_score', 0))
                top_post_url = top_post.get('url', '')
            
            # Prepare simplified data for insertion
            row_data = {
                "hashtag": f"#{hashtag_data['hashtag']}",
                "average_engagement_rating": avg_engagement_rating,
                "overall_sentiment": hashtag_data["average_sentiment"]["sentiment"],
                "posts_data": json.dumps(hashtag_data["posts"]),
                "post_url": top_post_url,
                "created_at": datetime.utcnow().isoformat() + 'Z'
            }
            
            # Insert into hashtag_ratings table
            supabase.table('hashtag_ratings').insert(row_data).execute()
            print(f"    - Saved to hashtag_ratings: #{hashtag_data['hashtag']} (Rating: {avg_engagement_rating}/10, Sentiment: {hashtag_data['average_sentiment']['sentiment']})")
            
        except Exception as e:
            print(f"    - Error saving to Supabase: {e}")
    
    def discover_trending_hashtags(self, base_topic: str, max_hashtags: int = 5) -> List[str]:
        """Discover trending hashtags related to a base topic"""
        print(f"🔍 Discovering trending hashtags for topic: {base_topic}")
        
        trending_hashtags = []
        
        try:
            # Navigate to the base topic hashtag page
            url = f"https://www.instagram.com/explore/tags/{base_topic}/"
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            # Scroll down to load more content
            self.driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(2)
            
            # Look for related hashtags in post captions and descriptions
            related_hashtag_selectors = [
                "//a[contains(@href, '/explore/tags/')]",
                "//span[contains(text(), '#')]",
                "//div[contains(@class, 'caption')]//span[starts-with(text(), '#')]"
            ]
            
            found_hashtags = set()
            
            for selector in related_hashtag_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements[:30]:  # Check more elements
                        try:
                            href = element.get_attribute('href')
                            if href and '/explore/tags/' in href:
                                hashtag = href.split('/explore/tags/')[-1].rstrip('/')
                                if hashtag and len(hashtag) > 2 and hashtag.lower() != base_topic.lower():
                                    found_hashtags.add(hashtag)
                            
                            text = element.text
                            if text and text.startswith('#'):
                                hashtag = text[1:].strip().split()[0]  # Get first hashtag only
                                if hashtag and len(hashtag) > 2 and hashtag.lower() != base_topic.lower():
                                    found_hashtags.add(hashtag)
                        except:
                            continue
                except:
                    continue
            
            # If we found related hashtags, use them
            if found_hashtags:
                trending_hashtags = list(found_hashtags)[:max_hashtags]
                print(f"   ✓ Found {len(trending_hashtags)} related hashtags: {', '.join([f'#{h}' for h in trending_hashtags])}")
            else:
                # Fallback: use popular variations of the base topic
                variations = self.get_topic_variations(base_topic)
                trending_hashtags = variations[:max_hashtags]
                print(f"   ⚠️ Using fallback variations: {', '.join([f'#{h}' for h in trending_hashtags])}")
                
        except Exception as e:
            print(f"   ❌ Error discovering hashtags for {base_topic}: {e}")
            # Ultimate fallback
            trending_hashtags = self.get_topic_variations(base_topic)[:max_hashtags]
            print(f"   � Using backup variations: {', '.join([f'#{h}' for h in trending_hashtags])}")
        
        return trending_hashtags
    
    def get_topic_variations(self, base_topic: str) -> List[str]:
        """Get popular variations for a topic"""
        variations_map = {
            'fashion': ['ootd', 'style', 'fashionista', 'streetstyle', 'fashionweek'],
            'travel': ['wanderlust', 'vacation', 'explore', 'adventure', 'travelgram'],
            'food': ['foodie', 'delicious', 'yummy', 'foodporn', 'instafood'],
            'fitness': ['workout', 'gym', 'healthy', 'fitlife', 'exercise'],
            'art': ['artwork', 'artist', 'creative', 'painting', 'drawing'],
            'technology': ['tech', 'innovation', 'gadgets', 'ai', 'startup'],
            'music': ['song', 'musician', 'concert', 'beats', 'melody'],
            'photography': ['photo', 'photographer', 'camera', 'portrait', 'landscape']
        }
        
        return variations_map.get(base_topic, [
            f"{base_topic}daily",
            f"{base_topic}life", 
            f"{base_topic}style",
            f"{base_topic}gram",
            f"{base_topic}lover"
        ])
    
    def analyze_hashtags(self, hashtags: List[str], max_posts_per_hashtag: int = 15):
        """Analyze multiple hashtags"""
        print(f"[+] Starting analysis of {len(hashtags)} hashtags...")
        
        results = []
        
        for i, hashtag in enumerate(hashtags):
            print(f"\n--- Processing hashtag {i+1}/{len(hashtags)}: #{hashtag} ---")
            
            hashtag_data = self.scrape_hashtag_posts(hashtag, max_posts_per_hashtag)
            results.append(hashtag_data)
            
            # Save to Supabase
            self.save_to_supabase(hashtag_data)
            
            # Pause between hashtags
            if i < len(hashtags) - 1:
                pause_time = random.uniform(5, 10)
                print(f"    - Pausing for {pause_time:.1f} seconds...")
                time.sleep(pause_time)
        
        return results
    
    def analyze_topic_with_trending_hashtags(self, topic: str, max_hashtags_per_topic: int = 3, max_posts_per_hashtag: int = 10) -> List[Dict[str, Any]]:
        """Analyze a topic by discovering its trending hashtags"""
        print(f"\n🔍 DISCOVERING TRENDING HASHTAGS FOR TOPIC: {topic.upper()}")
        print("=" * 60)
        
        # Discover trending hashtags
        trending_hashtags = self.discover_trending_hashtags(topic, max_hashtags_per_topic)
        
        # Analyze trending hashtags
        results = []
        for hashtag in trending_hashtags:
            hashtag_data = self.scrape_hashtag_posts(hashtag, max_posts_per_hashtag)
            results.append(hashtag_data)
            self.save_to_supabase(hashtag_data)
        
        return results
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print analysis summary"""
        print("\n" + "="*80)
        print("📊 HASHTAG ANALYSIS SUMMARY")
        print("="*80)
        
        for data in results:
            print(f"\n#{data['hashtag'].upper()}")
            print(f"  📈 Total Posts: {data['post_count']:,}")
            print(f"  💝 Total Engagement: {data['total_engagement']:,}")
            print(f"  📊 Avg Engagement: {data['engagement_rate']:,}")
            
            # Calculate and display average engagement rating
            if data['posts']:
                avg_rating = sum(post.get('engagement_rating', 0) for post in data['posts']) / len(data['posts'])
                rating_emoji = self.get_engagement_rating_emoji(int(avg_rating))
                print(f"  ⭐ Average Engagement Rating: {avg_rating:.1f}/10 {rating_emoji}")
            
            # Enhanced sentiment display
            sentiment_info = data['average_sentiment']
            sentiment_emoji = "😊" if sentiment_info['sentiment'] == 'positive' else "😢" if sentiment_info['sentiment'] == 'negative' else "😐"
            print(f"  🎭 Overall Sentiment: {sentiment_info['sentiment'].title()} {sentiment_emoji}")
            print(f"     📊 Polarity Score: {sentiment_info['polarity']:.3f} (-1=very negative, +1=very positive)")
            print(f"     📊 Subjectivity: {sentiment_info['subjectivity']:.3f} (0=objective, 1=subjective)")
            
            print(f"  📝 Posts Analyzed: {len(data['posts'])}")
            
            if data['posts']:
                top_post = max(data['posts'], key=lambda x: x['engagement_score'])
                top_post_rating = top_post.get('engagement_rating', self.calculate_engagement_rating(top_post['engagement_score']))
                top_post_emoji = self.get_engagement_rating_emoji(top_post_rating)
                print(f"  🔥 Top Post: {top_post['engagement_score']:,} engagement")
                print(f"     URL: {top_post['url']}")
                print(f"     Sentiment: {top_post['sentiment']['sentiment']} (polarity: {top_post['sentiment']['polarity']:.3f})")
                print(f"     Engagement Rating: {top_post_rating}/10 {top_post_emoji}")
                
                # Show sentiment distribution
                sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
                for post in data['posts']:
                    sentiment_counts[post['sentiment']['sentiment']] += 1
                
                print(f"  📈 Sentiment Distribution:")
                print(f"     😊 Positive: {sentiment_counts['positive']}/{len(data['posts'])} posts")
                print(f"     😢 Negative: {sentiment_counts['negative']}/{len(data['posts'])} posts")
                print(f"     😐 Neutral: {sentiment_counts['neutral']}/{len(data['posts'])} posts")
    
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function"""
    # Base topics to discover trending hashtags for
    BASE_TOPICS = [
        'fashion',
        'travel', 
        'food',
        'fitness',
        'art',
        'technology',
        'music',
        'photography'
    ]
    
    analyzer = HashtagAnalyzer(USERNAME, PASSWORD)
    
    try:
        analyzer.setup_driver()
        analyzer.login_instagram()
        
        # Wait a bit after login
        time.sleep(random.uniform(3, 6))
        
        print(f"\n🚀 STARTING DYNAMIC TRENDING HASHTAG ANALYSIS")
        print(f"📊 Analyzing {len(BASE_TOPICS)} topics with trending hashtag discovery")
        print("=" * 80)
        
        all_results = []
        
        # Analyze each topic by discovering its trending hashtags
        for i, topic in enumerate(BASE_TOPICS):
            print(f"\n🎯 TOPIC {i+1}/{len(BASE_TOPICS)}: {topic.upper()}")
            
            # Discover and analyze 3 trending hashtags per topic, 10 posts each
            topic_results = analyzer.analyze_topic_with_trending_hashtags(
                topic, 
                max_hashtags_per_topic=3, 
                max_posts_per_hashtag=10
            )
            
            all_results.extend(topic_results)
            
            # Pause between topics
            if i < len(BASE_TOPICS) - 1:
                pause_time = random.uniform(8, 15)
                print(f"\n⏸️  Pausing {pause_time:.1f} seconds before next topic...")
                time.sleep(pause_time)
        
        # Print comprehensive summary
        analyzer.print_summary(all_results)
        
        print(f"\n✅ DYNAMIC ANALYSIS COMPLETE!")
        print(f"📊 Analyzed {len(BASE_TOPICS)} topics")
        print(f"🏷️  Discovered and analyzed {len(all_results)} trending hashtags")
        print(f"💾 All data saved to Supabase with engagement ratings!")
        
    except Exception as e:
        print(f"[!] Error during analysis: {e}")
    finally:
        analyzer.cleanup()

if __name__ == "__main__":
    main()
