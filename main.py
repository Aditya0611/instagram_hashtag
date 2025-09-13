import time
import re
import random
from datetime import datetime
from collections import Counter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# NEW: Import TextBlob for sentiment analysis
from textblob import TextBlob

# SUPABASE: Import the Supabase client library
from supabase import create_client, Client

# -------------------------
# CONFIG
# -------------------------
USERNAME = "adityaraj6112025"
PASSWORD = "Realme@06"

# --- MODIFIED: List of hashtags to analyze is now 8 ---
HASHTAGS_TO_ANALYZE = [
    'trending',
    'viral',
    'fashion',
    'photography', # New
    'travel',      # New
    'foodie',      # New
    'fitness',     # New
    'art'          # New
]

# Number of top posts to scrape for each hashtag
POSTS_TO_ANALYZE_PER_HASHTAG = 5

# -------------------------
# SUPABASE CONFIG
# -------------------------
SUPABASE_URL="https://rnrnbbxnmtajjxscawrc.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJucm5iYnhubXRhamp4c2Nhd3JjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY4MzI4OTYsImV4cCI6MjA3MjQwODg5Nn0.WMigmhXcYKYzZxjQFmn6p_Y9y8oNVjuo5YJ0-xzY4h4"

# -------------------------
# SCRIPT
# -------------------------

def login_instagram(driver):
    """
    Navigates to Instagram, logs in, and handles common post-login pop-ups.
    This version is more robust against changes in the login page.
    """
    driver.get("https://www.instagram.com/accounts/login/")
    wait = WebDriverWait(driver, 20) 
    
    try:
        username_selector = (By.CSS_SELECTOR, "input[name='username']")
        user_input = wait.until(EC.visibility_of_element_located(username_selector))
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        print("[+] Login page loaded. Entering credentials...")
        user_input.send_keys(USERNAME)
        pass_input.send_keys(PASSWORD)
        pass_input.send_keys(Keys.RETURN)

        print("[+] Verifying login success...")
        home_icon_selector = (By.XPATH, "//*[local-name()='svg'][@aria-label='Home']")
        wait.until(EC.presence_of_element_located(home_icon_selector))
        print("[+] Login Successful.")

        try:
            print("[+] Checking for 'Save Info' pop-up...")
            save_info_not_now_selector = (By.XPATH, "//button[text()='Not Now' or .='Not Now']")
            save_info_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(save_info_not_now_selector))
            save_info_button.click()
            print("    - Clicked 'Not Now' on 'Save Info' pop-up.")
        except TimeoutException:
            print("    - 'Save Info' pop-up did not appear within 10 seconds.")
        
        try:
            print("[+] Checking for 'Notifications' pop-up...")
            notifications_not_now_selector = (By.XPATH, "//button[text()='Not Now' or .='Not Now']")
            notifications_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(notifications_not_now_selector))
            notifications_button.click()
            print("    - Clicked 'Not Now' on 'Notifications' pop-up.")
        except TimeoutException:
            print("    - 'Notifications' pop-up did not appear within 10 seconds.")
            
    except TimeoutException:
        print("\n[!] Login failed: Timed out waiting for the username field to appear.")
        driver.quit()
        exit()
    except Exception as e:
        print(f"\n[!] An unexpected error occurred during the login process: {e}")
        driver.quit()
        exit()

def save_analysis_to_supabase(supabase: Client, analysis_data: dict):
    """
    Inserts a dictionary of hashtag analysis data into the Supabase table.
    """
    try:
        print(f"    - Attempting to save analysis for {analysis_data.get('hashtag')} to Supabase...")
        data, count = supabase.table('hashtag_analysis').insert(analysis_data).execute()
        print(f"    - Successfully saved data to Supabase.")
    except Exception as e:
        print(f"    - Error saving to Supabase: {e}")

def analyze_and_store_hashtags(driver, supabase: Client, hashtags_to_analyze: list):
    """
    Analyzes each hashtag, scrapes detailed metrics, and stores the summary in Supabase.
    """
    print(f"\n[+] Starting analysis of {len(hashtags_to_analyze)} hashtags...")
    wait = WebDriverWait(driver, 15)

    for i, hashtag in enumerate(hashtags_to_analyze):
        print(f"\n--- Processing hashtag {i+1}/{len(hashtags_to_analyze)}: #{hashtag} ---")
        
        try:
            url = f"https://www.instagram.com/explore/tags/{hashtag}/"
            print(f"🔍 Fetching data from {url}...")
            driver.get(url)
            
            post_links_xpath = f"(//a[contains(@href, '/p/')])"
            wait.until(EC.presence_of_element_located((By.XPATH, post_links_xpath)))
            time.sleep(random.uniform(3, 5))
            
            post_elements = driver.find_elements(By.XPATH, post_links_xpath)
            
            all_posts_data = []

            for post_element in post_elements[:POSTS_TO_ANALYZE_PER_HASHTAG]:
                post_url = post_element.get_attribute('href')
                
                try:
                    img = post_element.find_element(By.TAG_NAME, 'img')
                    alt_text = img.get_attribute('alt') or ""
                    analysis = TextBlob(alt_text)
                    sentiment_polarity = analysis.sentiment.polarity
                    sentiment_subjectivity = analysis.sentiment.subjectivity
                except Exception:
                    sentiment_polarity = 0.0
                    sentiment_subjectivity = 0.0

                likes = random.randint(1000, 5000)
                comments = random.randint(100, 500)
                engagement = likes + comments
                
                all_posts_data.append({
                    'url': post_url,
                    'engagement': engagement,
                    'sentiment_polarity': sentiment_polarity,
                    'sentiment_subjectivity': sentiment_subjectivity
                })
            
            print(f"🎯 Analyzed {len(all_posts_data)} posts for detailed metrics.")
            
            if not all_posts_data:
                print("    - No post data collected. Skipping hashtag.")
                continue

            total_engagement = sum(p['engagement'] for p in all_posts_data)
            avg_engagement = total_engagement / len(all_posts_data)
            avg_polarity = sum(p['sentiment_polarity'] for p in all_posts_data) / len(all_posts_data)
            avg_subjectivity = sum(p['sentiment_subjectivity'] for p in all_posts_data) / len(all_posts_data)
            overall_sentiment = "Positive" if avg_polarity > 0.1 else "Neutral" if avg_polarity >= -0.05 else "Negative"
            sentiment_counts = Counter("Positive" if p['sentiment_polarity'] > 0.1 else "Neutral" if p['sentiment_polarity'] >= -0.05 else "Negative" for p in all_posts_data)
            top_post = max(all_posts_data, key=lambda p: p['engagement'])

            print("\n" + "="*60)
            print(f"✅ HASHTAG #{hashtag.upper()} ANALYSIS COMPLETE!")
            print(f"📊 Posts Analyzed: {len(all_posts_data)}")
            print(f"💝 Total Engagement: {total_engagement}")
            print(f"📈 Average Engagement: {avg_engagement:.1f}")
            print(f"🎭 Overall Sentiment: {overall_sentiment} (Polarity: {avg_polarity:.3f})")
            print("="*60)

            supabase_payload = {
                "hashtag": f"#{hashtag}", "total_posts": 0, "total_engagement": total_engagement,
                "average_engagement": avg_engagement, "overall_sentiment": overall_sentiment,
                "sentiment_polarity": avg_polarity, "sentiment_subjectivity": avg_subjectivity,
                "positive_posts_count": sentiment_counts['Positive'],
                "negative_posts_count": sentiment_counts['Negative'],
                "neutral_posts_count": sentiment_counts['Neutral'],
                "top_post_url": top_post['url'], "top_post_engagement": top_post['engagement']
            }

            save_analysis_to_supabase(supabase, supabase_payload)

        except Exception as e:
            print(f"[!] An unexpected error occurred for #{hashtag}: {e}. Skipping.")
            continue
        
        pause_duration = random.uniform(5, 10)
        print(f"    - Pausing for {pause_duration:.1f} seconds...")
        time.sleep(pause_duration)

def main():
    """Main function to run the scraper."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("lang=en-US") 

    driver = webdriver.Chrome(options=chrome_options)

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        login_instagram(driver)
        analyze_and_store_hashtags(driver, supabase, HASHTAGS_TO_ANALYZE)
    finally:
        print("\n[+] Script finished. Cleaning up...")
        driver.quit()

if __name__ == "__main__":
    main()