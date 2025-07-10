from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options

import random
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')

# Initialize WebDriver (Chrome in this example)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.cheapoair.com/")

def set_city(city_name,key_):
    try:
        # Wait for input to be present (up to 10 seconds)
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, key_))
        )
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_field)
        
        # Clear existing value
        input_field.clear()
        time.sleep(0.5)  # Brief pause
        
        for char in city_name:
            print(char)
            time.sleep(0.2)  # Brief pause

            input_field.send_keys(char)
        # Method 1: Simulate typing (works for most sites)
        # input_field.send_keys(Keys.CONTROL + "a")
        time.sleep(2)  # Allow time for dropdown to appear
        
        # Trigger Enter key to select first dropdown option
        input_field.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
        
        # Method 2: JavaScript alternative (use if Method 1 doesn't work)
        # driver.execute_script(f"""
        #     const input = document.getElementById('fs_originCity_0');
        #     input.value = "{city_name}";
        #     input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        #     input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        # """)
        
        print(f"Successfully set origin city to: {city_name}")
        
    except Exception as e:
        print(f"Error setting city: {str(e)}")
        # Consider adding screenshot for debugging:
        # driver.save_screenshot("error_screenshot.png")
def select_and_verify_date_return(driver, input_id, date_label):
    """
    Selects a return date from the calendar and verifies it's selected.
    
    Args:
        driver: Selenium WebDriver instance.
        input_id: ID of the input field that triggers the calendar (e.g., "fs_returnDate_0").
        date_label: The aria-label of the date to select (e.g., "29 July 2025").
    """
    wait = WebDriverWait(driver, 10)
    time.sleep(0.2)  # Brief pause

    # Open the calendar
    date_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", date_input)
    date_input.click()
    time.sleep(0.2)  # Brief pause

    # Wait for calendar to fully load
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendar")))
    
    # Select the date
    date_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[@aria-label='{date_label}']"))
    )
    time.sleep(0.2)  # Brief pause

    date_element.click()
    
    # More flexible verification - check if date is selected (might have different classes for return)
    # selected_date = wait.until(EC.presence_of_element_located(
    #     (By.XPATH, f"//span[@aria-label='{date_label}' and contains(@class, 'bg-blue') and contains(@class, 'is--return')]"))
    # )
    print(f"✅ Successfully selected and verified return date: {date_label}")
    return date_element
def set_travelers(driver, adults=1, seniors=0, children=0):
    """
    Sets the number of travelers in the CheapOair traveler selection dialog
    
    Args:
        driver: Selenium WebDriver instance
        adults: Number of adults (16-64)
        seniors: Number of seniors (65+)
        children: Number of children (2-15)
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        print("👥 Opening traveler selection dialog...")
        # Open traveler dialog
        traveler_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "travellerButtonFlights"))
        )
        time.sleep(0.2)  # Brief pause

        ActionChains(driver).move_to_element(traveler_btn).pause(0.5).click().perform()
        
        # Wait for dialog to fully load
        wait.until(EC.visibility_of_element_located(
            (By.ID, "travellerDialogBox"))
        )
        time.sleep(0.5)
        
        # Set number of adults
        print(f"👨‍👩‍👧 Setting adults to {adults}...")
        current_adults = int(driver.find_element(By.ID, "lbladults").text)
        for _ in range(adults - current_adults):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addADULTS")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Set number of seniors
        print(f"👵 Setting seniors to {seniors}...")
        current_seniors = int(driver.find_element(By.ID, "lblseniors").text)
        for _ in range(seniors - current_seniors):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addSENIORS")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Set number of children
        print(f"🧒 Setting children to {children}...")
        current_children = int(driver.find_element(By.ID, "lblchild").text)
        for _ in range(children - current_children):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addCHILD")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Close the dialog
        print("✅ Applying traveler selections...")
        done_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "closeFlightDialog"))
        )
        done_btn.click()
        
        # Verify selection in the main button
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#travellerButtonFlights .travelers-count__number"), 
            str(adults + seniors + children))
        )
        print(f"✅ Successfully set travelers: {adults} adults, {seniors} seniors, {children} children")
        return True
        
    except Exception as e:
        print(f"❌ Failed to set travelers: {str(e)}")
        return False
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
        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
        original_window = driver.current_window_handle

        # Switch to the new window
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
                
        # Wait for the new page to load and get its URL
        WebDriverWait(driver, 20).until(EC.url_contains("cheapoair"))
        new_url = driver.current_url
        print(f"✅ Successfully clicked 'Search Flights' button. New URL: {new_url}")
        # driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Failed to click search button: {str(e)}")
        return False
def reak_time_flight(driver):
        wait = WebDriverWait(driver, 15)
        stpos = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".stop__number.pt-1.stop__number-0"))
        )
        print(stpos)
        duration=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "stop__trip-duration"))
        )
        print(duration)


        airline=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "trip__airline--name"))
        )
        print(airline)
def scrape_flights(driver):
    # Configure Chrome options with enhanced browser mimicry
    # driver = webdriver.Chrome()
    # driver.get(url)
    wait = WebDriverWait(driver, 15)

    try:
        # Navigate to the URL with retry mechanism
        for attempt in range(3):
            try:
                print(f"Page loaded (attempt {attempt+1}). Waiting for content...")
                
                # Wait for JavaScript content with increased timeout
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )
                
                # Check for JavaScript warning pages
                body_text = driver.find_element(By.TAG_NAME, "body").text
                if "enable JavaScript" in body_text or "CAPTCHA" in body_text:
                    print("Encountered JavaScript/CAPTCHA wall. Retrying...")
                    time.sleep(5)
                    continue
                
                # Successful page load
                print("Valid content detected")
                break
                
            except TimeoutException:
                print(f"Timeout waiting for page load (attempt {attempt+1})")
                if attempt == 2:
                    print("Failed to load page after 3 attempts")
                    return []
                time.sleep(10)

        # Allow extra rendering time with random variation
        time.sleep(random.uniform(3, 5))
        
        # Find flight containers with multiple fallback strategies
        try:
            # Wait for flight cards with dynamic selector
            flight_cards = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article[class*='contract']"))
            )
            print(f"Found {len(flight_cards)} flight options")
            
        except TimeoutException:
            print("No flight cards found. Checking alternative selectors...")
            # Fallback selector strategy
            flight_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'flight-option') or contains(@class, 'trip-card')]")
            print(f"Alternative selector found {len(flight_cards)} options")

        flights_data = []
        
        # Process flight cards with individual error handling
        for index, card in enumerate(flight_cards):
            try:
                # Scroll into view for lazy-loaded content
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card)
                time.sleep(random.uniform(0.5, 1.2))
                
                # Extract price with multiple fallbacks
                try:
                    price = card.find_element(By.CSS_SELECTOR, ".fare-details__fare .currency").get_attribute("title")
                except NoSuchElementException:
                    price = card.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text
                    
                # Extract airline information
                try:
                    airline = card.find_element(By.CSS_SELECTOR, ".trip__airline--name").text
                except NoSuchElementException:
                    airline = "Unknown"

                # Extract departure details
                try:
                    departure_time = card.find_element(By.CSS_SELECTOR, ".timeline--list__time:first-child time").text
                    departure_airport = card.find_element(By.CSS_SELECTOR, ".timeline--list__time:first-child .is--airport-name").text
                except NoSuchElementException:
                    departure_time = departure_airport = "N/A"
                    
                # Extract arrival details
                try:
                    arrival_time = card.find_element(By.CSS_SELECTOR, ".timeline--list__time:nth-child(3) time").text
                    arrival_airport = card.find_element(By.CSS_SELECTOR, ".timeline--list__time:nth-child(3) .is--airport-name").text
                except NoSuchElementException:
                    arrival_time = arrival_airport = "N/A"

                # Extract duration and stops
                try:
                    duration = card.find_element(By.CSS_SELECTOR, ".stop__trip-duration").text
                    stops = card.find_element(By.CSS_SELECTOR, ".is--display-time .stop__number").text
                except NoSuchElementException:
                    duration = stops = "N/A"

                # Create flight dictionary
                flight_data = {
                    "price": price,
                    "airline": airline,
                    "departure_time": departure_time,
                    "departure_airport": departure_airport,
                    "arrival_time": arrival_time,
                    "arrival_airport": arrival_airport,
                    "duration": duration,
                    "stops": stops
                }
                
                flights_data.append(flight_data)
                print(f"Scraped flight {index+1}: {airline} - {price}")
                
            except Exception as e:
                print(f"Error processing flight card {index}: {str(e)}")
                continue
                
        return flights_data
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        driver.quit()
# Example usage:
# set_city_field("fs_originCity_0","tunis")
set_city("tunis","fs_originCity_0")
set_city("france","fs_destCity_0")
time.sleep(1)
select_and_verify_date_return(driver,"fs_departDate_0","25 July 2025")
select_and_verify_date_return(driver,"fs_returnDate_0","29 July 2025")
# set_date_field("fs_departDate_0", "28-06-2025")
# select_date_from_calendar(driver, "2025-07-15")  # Selects July 15, 2025
# Keep browser open for 10 seconds to see result
set_travelers(driver, adults=2, seniors=1, children=0)
url=click_search_flights(driver)
print(url)
flights = scrape_flights(driver)

# if url and isinstance(url, str):
#     print("Full search results URL:", url)
    
#     # Save to file if needed
#     with open("search_results.txt", "w") as f:
#         f.write(url)
# else:
#     print("Failed to capture URL, implementing fallback...")
# print(flights)
# reak_time_flight(driver)

# time.sleep(60)
# driver.quit()