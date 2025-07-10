from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
import random

def initialize_driver():
    """Initialize and return a Chrome WebDriver with configured options"""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def set_city(driver, city_name, key_):
    """Set city in the search form"""
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, key_))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_field)
        input_field.clear()
        time.sleep(0.5)
        
        for char in city_name:
            input_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        time.sleep(2)
        input_field.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
        print(f"Successfully set city to: {city_name}")
        return True
    except Exception as e:
        print(f"Error setting city: {str(e)}")
        return False

def select_date(driver, input_id, date_label):
    """Select date from calendar"""
    try:
        wait = WebDriverWait(driver, 10)
        date_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", date_input)
        date_input.click()
        
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendar")))
        
        date_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[@aria-label='{date_label}']"))
        )
        date_element.click()
        print(f"Successfully selected date: {date_label}")
        return True
    except Exception as e:
        print(f"Error selecting date: {str(e)}")
        return False

def set_travelers(driver, adults=1, seniors=0, children=0):
    """Set number of travelers"""
    wait = WebDriverWait(driver, 15)
    
    try:
        traveler_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "travellerButtonFlights"))
        )
        ActionChains(driver).move_to_element(traveler_btn).pause(0.5).click().perform()
        
        wait.until(EC.visibility_of_element_located((By.ID, "travellerDialogBox")))
        time.sleep(0.5)
        
        # Set adults
        current_adults = int(driver.find_element(By.ID, "lbladults").text)
        for _ in range(adults - current_adults):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addADULTS")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Set seniors
        current_seniors = int(driver.find_element(By.ID, "lblseniors").text)
        for _ in range(seniors - current_seniors):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addSENIORS")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Set children
        current_children = int(driver.find_element(By.ID, "lblchild").text)
        for _ in range(children - current_children):
            btn = wait.until(EC.element_to_be_clickable((By.ID, "addCHILD")))
            btn.click()
            time.sleep(random.uniform(0.2, 0.4))
        
        # Close dialog
        done_btn = wait.until(EC.element_to_be_clickable((By.ID, "closeFlightDialog")))
        done_btn.click()
        
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#travellerButtonFlights .travelers-count__number"), 
            str(adults + seniors + children))
        )
        print(f"Successfully set travelers: {adults} adults, {seniors} seniors, {children} children")
        return True
    except Exception as e:
        print(f"Failed to set travelers: {str(e)}")
        return False

def click_search_flights(driver):
    """Click the search flights button"""
    try:
        wait = WebDriverWait(driver, 15)
        search_btn = wait.until(EC.element_to_be_clickable((By.ID, "searchNow")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_btn)
        driver.execute_script("arguments[0].click();", search_btn)
        print("Successfully clicked 'Search Flights' button")
        return True
    except Exception as e:
        print(f"Failed to click search button: {str(e)}")
        return False

def scrape_flights(driver):
    """Scrape flight data from current page"""
    try:
        # Wait for results to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[class*='contract'], div[class*='flight-option']"))
        )
        time.sleep(random.uniform(3, 5))
        
        flight_cards = driver.find_elements(By.CSS_SELECTOR, "article[class*='contract'], div[class*='flight-option']")
        print(f"Found {len(flight_cards)} flight options")
        
        flights_data = []
        
        for index, card in enumerate(flight_cards):
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card)
                time.sleep(random.uniform(0.5, 1.2))
                
                # Extract data with robust error handling
                price = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".fare-details__fare .currency", "get_attribute", "title"),
                    (By.XPATH, ".//span[contains(@class, 'price')]", "text", None)
                ], "N/A")
                
                airline = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".trip__airline--name", "text", None)
                ], "Unknown")
                
                departure_time = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".timeline--list__time:first-child time", "text", None)
                ], "N/A")
                
                departure_airport = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".timeline--list__time:first-child .is--airport-name", "text", None)
                ], "N/A")
                
                arrival_time = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".timeline--list__time:nth-child(3) time", "text", None)
                ], "N/A")
                
                arrival_airport = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".timeline--list__time:nth-child(3) .is--airport-name", "text", None)
                ], "N/A")
                
                duration = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".stop__trip-duration", "text", None)
                ], "N/A")
                
                stops = extract_with_fallback(card, [
                    (By.CSS_SELECTOR, ".is--display-time .stop__number", "text", None)
                ], "N/A")

                flights_data.append({
                    "price": price,
                    "airline": airline,
                    "departure_time": departure_time,
                    "departure_airport": departure_airport,
                    "arrival_time": arrival_time,
                    "arrival_airport": arrival_airport,
                    "duration": duration,
                    "stops": stops
                })
                
                print(f"Scraped flight {index+1}: {airline} - {price}")
                
            except Exception as e:
                print(f"Error processing flight card {index}: {str(e)}")
                continue
                
        return flights_data
        
    except Exception as e:
        print(f"Error scraping flights: {str(e)}")
        return []

def extract_with_fallback(element, selectors, default):
    """Helper function to try multiple selectors"""
    for selector in selectors:
        try:
            if selector[2] == "text":
                return element.find_element(selector[0], selector[1]).text
            elif selector[2] == "get_attribute":
                return element.find_element(selector[0], selector[1]).get_attribute(selector[3])
        except NoSuchElementException:
            continue
    return default

def main():
    driver = initialize_driver()
    try:
        driver.get("https://www.cheapoair.com/")
        
        # Fill out search form
        set_city(driver, "tunis", "fs_originCity_0")
        time.sleep(1)
        set_city(driver, "france", "fs_destCity_0")
        time.sleep(1)
        select_date(driver, "fs_departDate_0", "25 July 2025")
        select_date(driver, "fs_returnDate_0", "29 July 2025")
        set_travelers(driver, adults=2, seniors=1, children=0)
        
        # Search and scrape
        if click_search_flights(driver):
            time.sleep(5)  # Wait for results to start loading
            flights = scrape_flights(driver)
            print(flights)
            if flights:
                df = pd.DataFrame(flights)
                df.to_csv("flight_results.csv", index=False)
                print(f"\nSuccessfully saved {len(flights)} flights to flight_results.csv")
                print("\nSample flight data:")
                print(df.head())
            else:
                print("No flights scraped successfully.")
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()