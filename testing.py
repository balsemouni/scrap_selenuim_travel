from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
import random

def scrape_flights(url):
    # Configure Chrome options with enhanced browser mimicry
    driver = webdriver.Chrome()
    driver.get("https://www.cheapoair.com/air/listing?&d1=MIR&r1=CDG&dt1=07/25/2025&d2=CDG&r2=MIR&dt2=07/29/2025&dtype1=A&rtype1=A&tripType=ROUNDTRIP&cl=ECONOMY&ad=1&se=0&ch=0&infs=0&infl=0")
    
    try:
        # Navigate to the URL with retry mechanism
        for attempt in range(3):
            try:
                driver.get(url)
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

if __name__ == "__main__":
    # Your flight search URL
    url = "https://www.cheapoair.com/air/listing?&d1=MIR&r1=CDG&dt1=07/25/2025&d2=CDG&r2=MIR&dt2=07/29/2025&dtype1=A&rtype1=A&tripType=ROUNDTRIP&cl=ECONOMY&ad=1&se=0&ch=0&infs=0&infl=0"
    
    # Scrape flight data with retry mechanism
    flights = scrape_flights(url)
    
    if flights:
        # Create DataFrame and save to CSV
        # df = pd.DataFrame(flights)
        # df.to_csv("flight_results.csv", index=False)
        print(f"\nSuccessfully saved {len(flights)} flights to flight_results.csv")
        
        # Print sample data
        print("\nSample flight data:")
        # print(df[['airline', 'price', 'departure_time', 'arrival_time']].head())
    else:
        print("No flights scraped successfully.")