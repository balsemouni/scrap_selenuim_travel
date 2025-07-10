import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def human_delay(min_sec=0.5, max_sec=2.0):
    """Random delay to mimic human thinking time"""
    time.sleep(random.uniform(min_sec, max_sec))

def human_type(element, text, speed=0.1):
    """Type text with variable speed and occasional typos"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(speed/2, speed*1.5))
    # Occasionally backspace and retype
    if random.random() > 0.7:
        for _ in range(1, 3):
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(random.uniform(0.1, 0.3))
        for char in text[-2:]:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))

def smooth_scroll(driver, element):
    """Smooth scroll to element with intermediate positions"""
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()
    human_delay(0.2, 0.5)

def human_click(driver, element):
    """Click with mouse movement imperfections"""
    actions = ActionChains(driver)
    # Move to element with slight overshoot
    actions.move_to_element_with_offset(element, random.randint(-10, 10), random.randint(-10, 10))
    actions.pause(random.uniform(0.1, 0.3))
    # Correct position with small movement
    actions.move_to_element(element)
    actions.pause(random.uniform(0.1, 0.5))
    actions.click()
    actions.perform()
    human_delay(0.3, 1.0)

def get_hotel_details(driver, timeout=10, scroll_to_load=False, max_scroll_attempts=3):
    """
    Extract hotel details including name, evaluation, price, and mentions
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Wait timeout in seconds
        scroll_to_load: Whether to scroll to load more content
        max_scroll_attempts: Maximum scroll attempts if scroll_to_load=True
        
    Returns:
        List of dictionaries containing hotel details
    """
    hotels_data = []
    
    # Handle scrolling for lazy-loaded content
    if scroll_to_load:
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        
        while scroll_attempts < max_scroll_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Allow time for loading
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height

    # Find all hotel listings
    hotel_listings = driver.find_elements(By.CSS_SELECTOR, "li")
    
    for hotel in hotel_listings:
        try:
            # Extract hotel name
            name = hotel.find_element(
                By.CSS_SELECTOR, 
                ".biGQs._P.fiohW.OgHoE"
            ).text.strip()
            
            # Extract evaluation (if available)
            try:
                evaluation = hotel.find_element(
                    By.CSS_SELECTOR, 
                    ".biGQs._P.pZUbB.ZNjnF"
                ).text.strip()
            except NoSuchElementException:
                evaluation = None
                
            # Extract price (if available)
            try:
                price = hotel.find_element(
                    By.CSS_SELECTOR, 
                    "span[data-automation='metaRegularPrice']"
                ).text.strip()
            except NoSuchElementException:
                price = None
                
            # Extract mentions (if available)
            mentions = []
            try:
                mention_container = hotel.find_element(
                    By.CSS_SELECTOR, 
                    "div.cbdko.K"
                )
                mention_spans = mention_container.find_elements(
                    By.CSS_SELECTOR, 
                    "span.TNAar"
                )
                mentions = [span.text.strip() for span in mention_spans]
            except NoSuchElementException:
                pass

            # Collect hotel data
            if None not in (name, evaluation, price):
                hotels_data.append({
                    "name": name,
                    "evaluation": evaluation,
                    "price": price,
                    "mentions": mentions
                })
                print("name:", name, "evaluation:", evaluation, "price:", price, "mentions:", mentions, '\n')
            else:
                print("Skipping entry due to missing data.")
        except (NoSuchElementException, StaleElementReferenceException):
            continue
    return hotels_data

def search_destination(driver, wait):
    human_delay(1, 3)  # Think before acting
    search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    smooth_scroll(driver, search_input)
    search_input = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    
    # Human-like input clearing
    human_click(driver, search_input)
    search_input.send_keys(Keys.CONTROL + "a")
    human_delay(0.1, 0.3)
    search_input.send_keys(Keys.BACKSPACE)
    human_delay(0.5, 1.0)
    
    # Type destination naturally
    human_type(search_input, "Berlin")
    human_delay(0.5, 1.5)  # Pause before submitting
    search_input.submit()

def click_hotel(driver, wait):
    human_delay(2, 4)  # Browse results before clicking
    hotels_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'Hotels-g')]"))
    )
    human_click(driver, hotels_link)

def main():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

    try:
        # Use context manager for automatic cleanup
        with uc.Chrome(options=chrome_options, use_subprocess=True) as driver:
            wait = WebDriverWait(driver, 20)
            url = "https://www.tripadvisor.com/Hotels"
            driver.get(url)
            
            # Random browsing pattern
            for _ in range(random.randint(1, 3)):
                driver.execute_script("window.scrollBy(0, {})".format(random.randint(200, 600)))
                human_delay(0.5, 1.5)
            
            search_destination(driver, wait)
            click_hotel(driver, wait)
            
            # Human-like date selection
            human_delay(1, 2)
            date_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='July 11, 2025']"))
            )
            smooth_scroll(driver, date_element)
            human_click(driver, date_element)
            
            # Simulate post-action browsing
            driver.execute_script("window.scrollBy(0, {})".format(random.randint(300, 700)))
            human_delay(1, 3)
            date_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='July 16, 2025']"))
            )
            smooth_scroll(driver, date_element)
            human_click(driver, date_element)
            
            # Simulate post-action browsing
            driver.execute_script("window.scrollBy(0, {})".format(random.randint(300, 700)))
            human_delay(1, 3)
            
            # Get hotel details
            hotels=get_hotel_details(driver)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()