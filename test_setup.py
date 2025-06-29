"""
Quick test to verify Playwright installation and basic functionality
"""

def test_playwright():
    try:
        from playwright.sync_api import sync_playwright
        print("+ Playwright imported successfully")
        
        with sync_playwright() as p:
            print("+ Playwright context created")
            browser = p.chromium.launch(headless=True)
            print("+ Chromium browser launched (headless)")
            page = browser.new_page()
            print("+ New page created")
            page.goto("https://example.com")
            print("+ Successfully navigated to example.com")
            title = page.title()
            print(f"+ Page title: {title}")
            browser.close()
            print("+ Browser closed successfully")
            
        return True
    except Exception as e:
        print(f"- Playwright test failed: {e}")
        return False

def test_env_vars():
    import os
    from dotenv import load_dotenv
    
    try:
        load_dotenv()
        sit_user = os.getenv("SIT_USER")
        sit_pass = os.getenv("SIT_PASS") 
        feide_name = os.getenv("FEIDE_DISPLAY_NAME")
        sit_unit = os.getenv("SIT_UNIT")
        
        print("+ Environment variables check:")
        print(f"  - SIT_USER: {'SET' if sit_user else 'NOT SET'}")
        print(f"  - SIT_PASS: {'SET' if sit_pass else 'NOT SET'}")
        print(f"  - FEIDE_DISPLAY_NAME: {'SET' if feide_name else 'NOT SET'}")
        print(f"  - SIT_UNIT: {'SET' if sit_unit else 'NOT SET'}")
        
        if sit_user and sit_pass and feide_name and sit_unit:
            print("+ All required environment variables are set")
            return True
        else:
            print("- Some required environment variables are missing")
            return False
            
    except Exception as e:
        print(f"- Environment test failed: {e}")
        return False

def main():
    print("AutoBook Setup Verification\n")
    print("=" * 40)
    
    pw_ok = test_playwright()
    env_ok = test_env_vars()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"- Playwright: {'PASS' if pw_ok else 'FAIL'}")
    print(f"- Environment: {'PASS' if env_ok else 'FAIL'}")
    
    if pw_ok and env_ok:
        print("\nSetup is ready! You can now run: python sit_autobook.py")
    else:
        print("\nSetup issues detected. Please fix the above errors.")

if __name__ == "__main__":
    main()
