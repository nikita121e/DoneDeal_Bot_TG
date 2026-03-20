# 🚗 DoneDeal Telegram Bot Scraper

A powerful Python bot that monitors **DoneDeal.ie** for new car listings and sends instant notifications to Telegram. Perfect for catching "hot" deals on automatic and electric cars under a specific budget.

## ✨ Features
- **Real-time Monitoring:** Checks for new ads every X minutes.
- **Deep Scrapping:** Automatically enters each ad to extract:
  - 📸 High-quality Photo
  - 🛣️ Exact Mileage
  - ⚙️ Transmission type (Auto/Electric/Manual)
  - 💰 Current Price
- **Direct Links:** Get a clickable link to the car immediately in your chat.
- **Smart Filter:** Ignores old ads on the first run to prevent spam.

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nikita121e/donedeal-bot.git]




2.Install dependencies:

Bash
pip install -r requirements.txt
playwright install chromium



3.Configuration:
Open main.py and fill in your credentials:

TOKEN: Your Telegram Bot Token from @BotFather.
CHAT_ID: Your Telegram User ID from @userinfobot.
SEARCH_URL: Your custom DoneDeal search link with filters




⚠️ Disclaimer
This project is for educational purposes only. Be respectful of DoneDeal's Terms of Service regarding web scraping.
