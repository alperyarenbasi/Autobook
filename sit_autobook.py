from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os, time, random, traceback
from dotenv import load_dotenv
from persistent_status import log_event      

load_dotenv()

UNIT             = os.getenv("SIT_UNIT") 
UNIT_URL         = f"https://bolig.sit.no/en/unit/{UNIT}/?code=xxsitxxSITYY"
USERNAME         = os.getenv("SIT_USER")
PASSWORD         = os.getenv("SIT_PASS")
FEIDE_DISPLAY_NAME = os.getenv("FEIDE_DISPLAY_NAME")
CHECK_INTERVAL   = 0           # seconds between checks
MAX_BACKOFF      = 60          # max seconds when backing off on HTTP failures


# --------------------------------------------------------------------------- helpers

def safe_goto(page, url: str, wait_until="domcontentloaded"):
    """Navigate with exponential backoff if HTTP fails (404/500/cloudflare)."""
    attempt, delay = 0, 2
    while True:
        try:
            page.goto(url, wait_until=wait_until)
            return
        except Exception as e:
            attempt += 1
            delay = min(MAX_BACKOFF, delay * 1.6)
            print(f"goto failed ({e!r}) - retrying in {delay:.1f}s")
            time.sleep(delay)

def safe_reload(page, wait_until="domcontentloaded"):
    attempt, delay = 0, 2
    while True:
        try:
            page.reload(wait_until=wait_until)
            #dismiss_popups(page)
            return
        except Exception as e:
            attempt += 1
            delay = min(MAX_BACKOFF, delay * 1.6)
            print(f"reload failed ({e!r}) - retrying in {delay:.1f}s")
            time.sleep(delay)

def feide_login(page):
    print("Feide full login …")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="Log in with Feide").click()

    search = page.locator('input[placeholder*="Search"]')
    search.click(); search.fill("NTNU")
    page.wait_for_selector('li:has-text("NTNU")')
    page.click('li:has-text("NTNU")')
    page.click('button:has-text("Continue")')

    page.fill('input[name="feidename"]', USERNAME)
    page.fill('input[name="password"]',  PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_selector('nav >> text=MyPage', timeout=15_000)
    log_event("login", unit="all", ok=True)

def feide_relogin(page):
    print("Logging in with Feide again...")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="Log in with Feide").click()
    page.locator("text=What user account").wait_for(timeout=10_000)
    
    page.locator(f"h3:has-text('{FEIDE_DISPLAY_NAME}')").first.click()

    if page.locator('input[name="feidename"]').is_visible():
        page.fill('input[name="feidename"]', USERNAME)
        page.fill('input[name="password"]',  PASSWORD)
        page.click('button[type="submit"]')

    # Wait until we're back on Sit
    page.wait_for_selector('nav >> text=MyPage', timeout=15_000)
    print("Quick re-login complete")
    log_event("re-login", unit=UNIT, ok=True)


def is_logged_in(page):
    for _ in range(20):                 # 20 × 100 ms ≈ 2 s max
        if page.locator('nav >> text=MyPage').is_visible():
            return True
        page.wait_for_timeout(100)
    return False

def ensure_logged_in(page):
    if is_logged_in(page):
        return

    print("Session expired - running quick re-login")
    try:
        feide_relogin(page)                    # attempt fast path
        safe_goto(page, UNIT_URL)
    except Exception as e:
        print(f"Quick re-login failed ({e!r}), falling back to full login")
        safe_goto(page, UNIT_URL)
        feide_login(page)                        # full flow

def ensure_on_right_page(page, target_url: str, goto_fn):
    """
    Guarantee that `page` is on `target_url`.
    If it drifted elsewhere, call `goto_fn(page, target_url)` to navigate back.

    Parameters
    ----------
    page : playwright.sync_api.Page
        The active Playwright page object.
    target_url : str
        The exact URL we expect to be on.
    goto_fn : Callable[[Page, str], None]
        A navigation helper (e.g. your `safe_goto`) that takes (page, url).
    """
    if page.url != target_url:
        print(f"Detected redirect: {page.url} != {target_url} - going back")
        goto_fn(page, target_url)
        log_event("wrong- page", unit=UNIT, ok=True)


# --------------------------------------------------------------------------- main loop
def run_autobooker():
    if not USERNAME or not PASSWORD or not FEIDE_DISPLAY_NAME or not UNIT:
        raise RuntimeError("Set SIT_USER, SIT_PASS, FEIDE_DISPLAY_NAME and SIT_UNIT in .env")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        safe_goto(page, UNIT_URL)

        # first login
        feide_login(page)
        safe_goto(page, UNIT_URL)

        selector = 'button:has-text("Book now"):not([disabled])'
        booked   = False
        print(f"Monitoring unit {UNIT} every {CHECK_INTERVAL}s…")

        while not booked:
            start = time.time()

            ensure_logged_in(page)
            ensure_on_right_page(page, UNIT_URL, safe_goto)

            try:
                page.wait_for_selector(selector, timeout=2_000)
                page.click(selector)
                booked = True
                log_event("booked", unit=UNIT, ok=True)
            except PlaywrightTimeoutError:
                safe_reload(page)
                elapsed   = time.time() - start
                # tiny random jitter to look less bot-like
                remaining = max(0, CHECK_INTERVAL - elapsed) #+ random.uniform(0, 0.7)
                print(f"--> not available, retrying in {remaining:.1f}s")
                page.wait_for_timeout(remaining * 1_000)

        # booked!
        page.screenshot(path="booked.png")
        print("UNIT BOOKED")

        print("Ready to sign contract.")
        page.pause()
        #browser.close()    


def main():
    try:
        run_autobooker()
    except Exception:
        tb = traceback.format_exc()
        log_event("crash", unit="n/a", ok=False, error=tb)
        print("ERROR OCCURRED!")
        input("Press Enter to continue...")
        raise

if __name__ == "__main__":
    main()
