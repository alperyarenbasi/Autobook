"""
Test script to verify that all modules are working correctly.
Run this to check if persistent_status.py is functioning.
"""

def test_persistent_status():
    """Test the persistent_status module"""
    try:
        from persistent_status import log_event
        print("+ persistent_status module imported successfully")
        
        # Test logging
        log_event("test", unit="test-unit", ok=True)
        print("+ log_event function works")
        
        return True
    except Exception as e:
        print(f"- persistent_status test failed: {e}")
        return False

def main():
    print("Testing AutoBook modules...\n")
    
    status_ok = test_persistent_status()
    
    print(f"\nTest Results:")
    print(f"- persistent_status: {'PASS' if status_ok else 'FAIL'}")
    
    if status_ok:
        print("\nAll modules are working correctly!")
        print("\nTo run the main application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up your .env file with SIT_USER, SIT_PASS, and FEIDE_DISPLAY_NAME")
        print("3. Run: python sit_autobook.py")
    else:
        print("\nSome modules have issues. Check the error messages above.")

if __name__ == "__main__":
    main()
