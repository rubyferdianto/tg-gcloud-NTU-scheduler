#!/usr/bin/env python3
"""
Test script to verify the Telegram bot setup
"""

import os
import sys
import requests
import time

def test_telegram_bot_token():
    """Test if the Telegram bot token is valid"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        return False
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                print(f"✅ Bot token is valid: @{bot_info['result']['username']}")
                return True
            else:
                print(f"❌ Bot token error: {bot_info}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking bot token: {e}")
        return False

def test_webhook_url():
    """Test if webhook URL is accessible"""
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        print("⚠️  WEBHOOK_URL not set (normal for local development)")
        return True
    
    try:
        response = requests.get(f"{webhook_url}/")
        if response.status_code == 200:
            print(f"✅ Webhook URL is accessible: {webhook_url}")
            return True
        else:
            print(f"❌ Webhook URL error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking webhook URL: {e}")
        return False

def test_local_imports():
    """Test if all required modules can be imported"""
    try:
        from src.telegram_bot import TelegramBot
        from src.scheduler import schedule_daily_notification
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🧪 Testing Telegram Bot Setup\n")
    
    tests = [
        ("Telegram Bot Token", test_telegram_bot_token),
        ("Module Imports", test_local_imports),
        ("Webhook URL", test_webhook_url),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    if all(results):
        print("🎉 All tests passed! Your bot setup looks good.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
