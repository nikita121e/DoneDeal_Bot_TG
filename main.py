import time
import requests
from playwright.sync_api import sync_playwright

TOKEN = "UR_BOT_TOKEN_FROM_BOT.FATHER"
CHAT_ID = "UR_ID_OF_ACCOUNT"
CHECK_INTERVAL = 300
SEARCH_URL = "https://www.donedeal.ie/cars?transmission=[Automatic/Manuel]&price_to=[Put here ur max price of a car]&source=private&sort=publishdate%20desc" 
#remove brackets and pick something that u want e.g.:"https://www.donedeal.ie/cars?transmission=Automatic&price_to=25000&source=private&sort=publishdate%20desc"
seen_ads = set()
def send_telegram(message, photo_url=None):
    payload = {"chat_id": CHAT_ID, "parse_mode": "HTML"}
    if photo_url:
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        payload["photo"] = photo_url
        payload["caption"] = message
    else:
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload["text"] = message

    try:
        res = requests.post(api_url, json=payload, timeout=15)
        if not res.ok and photo_url:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
    except Exception as e:
        print(f"Networking mistake Telegram: {e}")
def get_car_details(context, ad_url):
    page = context.new_page()
    info = {"mileage": "Not specified", "transmission": "Автомат", "photo": None}
    try:
        page.goto(ad_url, wait_until="domcontentloaded", timeout=30000)
        m_el = page.query_selector('li[data-testid="key-fact-Mileage"] span:last-child')
        if m_el: info["mileage"] = m_el.inner_text().strip()
        t_el = page.query_selector('li[data-testid="key-fact-Transmission"] span:last-child')
        if t_el: info["transmission"] = t_el.inner_text().strip()
        img_el = page.query_selector('div[class*="Carousel"] img')
        if img_el:
            img_src = img_el.get_attribute('src')
            if img_src:
                info["photo"] = img_src.split('?')[0]
    except Exception as e:
        print(f"Can't read details {ad_url}: {e}")
    finally:
        page.close()
    return info
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-IE"
        )
        main_page = context.new_page()
        print(f"🚀 The bot is running! Monitoring {SEARCH_URL}")
        first_run = True
        while True:
            try:
                main_page.goto(SEARCH_URL, wait_until="networkidle", timeout=60000)
                main_page.wait_for_selector('li[data-testid="search-result"]', timeout=20000)
                ads = main_page.query_selector_all('li[data-testid="search-result"]')
                for ad in ads:
                    link_el = ad.query_selector('a')
                    if not link_el: continue
                    raw_link = link_el.get_attribute('href')
                    direct_url = "https://www.donedeal.ie" + raw_link if not raw_link.startswith('http') else raw_link
                    ad_id = direct_url.split('/')[-1]
                    if ad_id not in seen_ads:
                        if first_run:
                            seen_ads.add(ad_id)
                            continue
                        title_el = ad.query_selector('p[data-testid="title"]')
                        price_el = ad.query_selector('p[data-testid="price"]')
                        title = title_el.inner_text() if title_el else "No title"
                        price = price_el.inner_text() if price_el else "Price not specifed"
                        print(f"🔎 Checking: {title} ({price})")
                        details = get_car_details(context, direct_url)
                        msg = (f"🔔 <b>NEW ANNOUNCEMENT</b>\n\n"
                               f"🚘 <b>{title}</b>\n"
                               f"💰 Price: <b>{price}</b>\n"
                               f"🛣️ Milage: <code>{details['mileage']}</code>\n"
                               f"⚙️ Transmission: {details['transmission']}\n\n"
                               f"🔗 <b>Link:</b>\n{direct_url}")
                        send_telegram(msg, details['photo'])
                        seen_ads.add(ad_id)
                        time.sleep(2)
                if first_run:
                    print(f"✅ The database has been initialized ({len(seen_ads)} авто). Starting survillance...")
                    first_run = False
            except Exception as e:
                print(f"⚠️ Main loop error: {e}")
                time.sleep(30)
            time.sleep(CHECK_INTERVAL)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("The bot was stopped manually.")