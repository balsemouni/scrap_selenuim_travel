from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def select_date(driver, target_date):
    """
    Selects a date in the TripAdvisor calendar
    :param driver: WebDriver instance
    :param target_date: Tuple (year, month, day) e.g., (2025, 7, 15)
    """
    year, month, day = target_date
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    month_name = month_names[month]
    month_year = f"{month_name} {year}"
    
    try:
        # Wait for calendar to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
        )
        
        # Find all month containers
        month_containers = driver.find_elements(By.CSS_SELECTOR, "div.lunjU")
        
        for container in month_containers:
            # Check if this container has the target month
            header = container.find_element(By.CSS_SELECTOR, "h2.nxFFd")
            if header.text == month_year:
                # Find the date cell in this month
                date_cell = container.find_element(
                    By.XPATH,
                    f".//div[@role='gridcell']//div[contains(@class, 'tuqBW') and text()='{day}']"
                )
                
                # Scroll to and click the date
                driver.execute_script("arguments[0].scrollIntoView(true);", date_cell)
                ActionChains(driver).move_to_element(date_cell).click().perform()
                return True
        
        return False
        
    except Exception as e:
        print(f"Error selecting date: {e}")
        return False

# Usage example:
driver = webdriver.Chrome()
driver.get("https://www.tripadvisor.com/Search?q=france&geo=1&ssrc=h&searchNearby=false&searchSessionId=000669c3645722fd.ssid&offset=0")

try:
    # Open the date picker (check-in example)
    checkin_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation='checkin']"))
    )
    driver.execute_script("arguments[0].click();", checkin_button)
    
    # Select July 15, 2025
    if select_date(driver, (2025, 7, 15)):
        print("Date selected successfully!")
    else:
        print("Failed to select date")
        
    time.sleep(2)  # See the result
    
finally:
    driver.quit()