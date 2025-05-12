from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os, time
from dotenv import load_dotenv
load_dotenv()      



#testunit = "hk10-32"     
#units= ["ob001-235"]   


UNIT =  "ob001-235" #Talha sin
TEST_UNIT = "ob077-102" 

UNIT_URL = "https://bolig.sit.no/en/unit/ob001-235/"
USERNAME = os.getenv("SIT_USER")
PASSWORD = os.getenv("SIT_PASS")

CHECK_INTERVAL = 10          # sekunder mellom hver sjekk

def main():
    #while True:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            context = browser.new_context()
            page    = context.new_page()

            page.goto(UNIT_URL)
            page.wait_for_timeout(2000)
        

            
            login_btn = page.get_by_role("button", name="Login")
            login_btn.wait_for(state="visible")
            login_btn.scroll_into_view_if_needed()
            login_btn.click()

            feide_btn= page.get_by_role("button", name="Log in with Feide")
            feide_btn.wait_for(state="visible")
            feide_btn.scroll_into_view_if_needed()
            feide_btn.click()

            search_box = page.locator('input[placeholder*="Search"]')
            search_box.wait_for(state="visible")
            search_box.fill("NTNU")
            page.wait_for_selector(
            'li:has-text("NTNU")',
            timeout=5_000
            )
            page.click(
                'li:has-text("NTNU")'
            )

            page.click('button:has-text("Continue")')
            
            page.fill('input[name="feidename"]', USERNAME)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            
            #for unit in units:
            unit_url = f"https://bolig.sit.no/en/unit/{TEST_UNIT}/"
            page.goto(unit_url, wait_until="networkidle")
            print("Visiting page...")

            selector = 'button:has-text("Book now"):not([disabled])'
            booked = False

            while not booked:
                try:
                    page.wait_for_selector(selector, timeout=2_000)
                    page.locator(selector).scroll_into_view_if_needed()
                    #page.click(selector)
                    print("Klikket (Book now). Signere kontrakt ...")
                    page.screenshot(path="booked.png")

                    booked = True
                except PlaywrightTimeoutError:
                
                    print(f"Ikke tilgjengelig enda, venter {CHECK_INTERVAL}s...")
                    page.reload(wait_until="networkidle")
                    time.sleep(CHECK_INTERVAL)


            
            page.screenshot(path="example.png")   
            input("Trykk enter for å lukke nettleseren...")
            print("Klar til å signere kontrakt!")     
            #page.pause()        

if __name__ == "__main__":
    main()
