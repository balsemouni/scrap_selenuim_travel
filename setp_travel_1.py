from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Configure Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Disable automation flags
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)

# Make Selenium less detectable
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
})
driver.execute_script("delete navigator.__proto__.webdriver;")

try:
    driver.get("https://www.tripadvisor.com/Hotels-g31350-Scottsdale_Arizona_Hotels.html ")

    # Wait until hotel cards appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.uitk-card'))
    )
    time.sleep(2)

    # Scroll multiple times to load more results
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get all hotel containers
    hotels = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-stid="hotel-title"]'))
    )

    print(f"Found {len(hotels)} hotels")

    for i, hotel_card in enumerate(hotels):
        try:
            name = hotel_card.find_element(By.CSS_SELECTOR, '.uitk-heading .is-visually-hidden').text.split("review")[0].strip()
        except Exception:
            name = "N/A"

        try:
            rating_text = hotel_card.find_element(By.CSS_SELECTOR, '[data-testid="rating-stars"]').get_attribute("aria-label")
            rating = rating_text.split()[0] if rating_text else "N/A"
        except Exception:
            rating = "N/A"

        try:
            reviews = hotel_card.find_element(By.CSS_SELECTOR, '[data-testid="review-count"]').text
        except Exception:
            reviews = "N/A"

        try:
            price = hotel_card.find_element(By.CSS_SELECTOR, '.uitk-text.uitk-type-medium.uitk-type-weight-bold').text
        except Exception:
            price = "Not available"

        try:
            amenities = hotel_card.find_element(By.CSS_SELECTOR, '.AmenitiesWrapper__amenity_text').text
        except Exception:
            amenities = "None"

        print("\n" + "=" * 50)
        print(f"Hotel {i+1}")
        print(f"Name: {name}")
        print(f"Rating: {rating}/5")
        print(f"Reviews: {reviews}")
        print(f"Price: {price}")
        print(f"Amenities: {amenities}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()