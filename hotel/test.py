from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=options)

url = "https://www.tripadvisor.com/Hotels-g187323-Berlin-Hotels.html#SPLITVIEWMAP"

try:
    # Load the page
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(3)  # Basic wait - consider using explicit waits instead
    
    # Use WebDriverWait for more robust element finding
    wait = WebDriverWait(driver, 10)
    
    try:
        # Hotel name with more specific selector and wait
        hotel_name = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation='hotel-card-title'] h3"))
        ).text
    except TimeoutException:
        hotel_name = "Not found"
        print("Could not find hotel name element")
    
    try:
        # Rating with more specific selector
        rating = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-target='review-score-component'] span:first-child"))
        ).text
    except TimeoutException:
        rating = "Not found"
        print("Could not find rating element")
    
    try:
        # Review count
        review_count = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-test-target='reviews-link'] span:first-child"))
        ).text
    except TimeoutException:
        review_count = "Not found"
        print("Could not find review count element")
    
    try:
        # Mentions - more robust handling
        mentions_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-target='amenities']"))
        )
        mentions = [mention.text for mention in mentions_container.find_elements(By.CSS_SELECTOR, "span:not(.sponsored)")]
    except TimeoutException:
        mentions = []
        print("Could not find mentions elements")
    
    print("\nHotel Information:")
    print(f"Hotel Name: {hotel_name}")
    print(f"Rating: {rating}")
    print(f"Review Count: {review_count}")
    print(f"Mentions: {', '.join(mentions) if mentions else 'No mentions found'}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()