from playwright.sync_api import sync_playwright
import os, time
from dotenv import load_dotenv
load_dotenv()          


UNIT_URL = "https://bolig.sit.no/en/unit/ob001-235/"
USERNAME = os.getenv("SIT_USER")
PASSWORD = os.getenv("SIT_PASS")

CHECK_INTERVAL = 10          # sekunder mellom hver sjekk
BUTTON_TEXT    = "Book now"      # endre hvis Sit endrer språk

def main():
    
    with sync_playwright() as p:
        chromium = p.chromium
        browser  = chromium.launch(headless=False, slow_mo=200)
        page     = browser.new_page()
        page.goto(UNIT_URL)
        page.wait_for_timeout(2000)
        print("Visiting page...")
        page.screenshot(path="example.png")
        print("Taking screenshot...")

        try:
            btn = page.locator('button:has-text("Book now")')
            btn.scroll_into_view_if_needed()
            print("Button found!")
        except:
            print("Button not found, trying again...")

        try:
            btn.wait_for(state="visible")
            btn.wait_for(state="enabled")
            btn.click()
        except Exception as e:
            print(f"An error occurred: {e}")


        browser.close()
        

if __name__ == "__main__":
    main()
