from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_search_flights(driver):
    """
    Clicks the 'Search Flights' button
    
    Args:
        driver: Selenium WebDriver instance
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        print("🛫 Clicking 'Search Flights' button...")
        # Locate the button by its ID
        search_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "searchNow"))
        )
        
        # Scroll into view (if needed)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_btn)
        
        # Click using JavaScript for reliability
        driver.execute_script("arguments[0].click();", search_btn)
        print("✅ Successfully clicked 'Search Flights' button")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to click search button: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.cheapoair.com/")
    
    try:
        # Click the search button
        click_search_flights(driver)
        
        # Add delay to keep browser open for inspection
        print("Browser will remain open for 60 seconds...")
        time.sleep(60)  # 60 seconds delay for manual inspection
        
    finally:
        # Only quit if you want to
        # driver.quit()  # You can comment this out to keep browser open indefinitely
        pass