from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()
driver.get("https://www.cheapoair.com/")

# Wait for the calendar to load (if needed)
wait = WebDriverWait(driver, 10)
def select_and_verify_date_return(driver, input_id, date_label):
    """
    Selects a return date from the calendar and verifies it's selected.
    
    Args:
        driver: Selenium WebDriver instance.
        input_id: ID of the input field that triggers the calendar (e.g., "fs_returnDate_0").
        date_label: The aria-label of the date to select (e.g., "29 July 2025").
    """
    wait = WebDriverWait(driver, 10)
    
    # Open the calendar
    date_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", date_input)
    date_input.click()
    
    # Wait for calendar to fully load
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendar")))
    
    # Select the date
    date_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[@aria-label='{date_label}']"))
    )
    date_element.click()
    
    # More flexible verification - check if date is selected (might have different classes for return)
    selected_date = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//span[@aria-label='{date_label}' and contains(@class, 'selected')]"))
    )
    print(f"✅ Successfully selected and verified return date: {date_label}")
    return selected_date
def select_and_verify_date_return(driver, input_id, date_label):
    """
    Selects a return date from the calendar and verifies it's selected.
    
    Args:
        driver: Selenium WebDriver instance.
        input_id: ID of the input field that triggers the calendar (e.g., "fs_returnDate_0").
        date_label: The aria-label of the date to select (e.g., "29 July 2025").
    """
    wait = WebDriverWait(driver, 10)
    
    # Open the calendar
    date_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", date_input)
    date_input.click()
    
    # Wait for calendar to fully load
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendar")))
    
    # Select the date
    date_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[@aria-label='{date_label}']"))
    )
    date_element.click()
    
    # More flexible verification - check if date is selected (might have different classes for return)
    # selected_date = wait.until(EC.presence_of_element_located(
    #     (By.XPATH, f"//span[@aria-label='{date_label}' and contains(@class, 'bg-blue') and contains(@class, 'is--return')]"))
    # )
    print(f"✅ Successfully selected and verified return date: {date_label}")
    return date_element
    
    # Open the calendar
    date_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", date_input)
    date_input.click()
    print("hi")
    # Select the date
    date_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[@aria-label='{date_label}']"))
    )
    date_element.click()
    
    # Verify the date is selected (has `bg-blue is--depart` classes)
    selected_date = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//span[@aria-label='{date_label}' and contains(@class, 'bg-blue') and contains(@class, 'is--return')]"))
    )
    print(f"✅ Successfully selected and verified: {date_label}")
    return selected_date
select_and_verify_date_return(driver,"fs_departDate_0","25 July 2025")
select_and_verify_date_return(driver,"fs_returnDate_0","29 July 2025")

# Set Departure Date (July 12, 2025)
# depart_date_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID,  "fs_departDate_0"))
#         )
# driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", depart_date_input)
# depart_date_input.click()
# date_element = wait.until(EC.element_to_be_clickable(
#     (By.XPATH, "//span[@aria-label='25 July 2025']"))
# )
# date_element.click()
# selected_date = wait.until(EC.presence_of_element_located(
#     (By.XPATH, "//span[@aria-label='12 July 2025' and contains(@class, 'bg-blue') and contains(@class, 'is--depart')]"))
# )
# depart_date_input = wait.until(EC.element_to_be_clickable((By.ID, "fs_departDate_0")))
# depart_date_input.clear()
# depart_date_input.send_keys("Jul 30, 2025")  # Format may vary based on site

# Set Return Date (July 19, 2025)
# return_date_input = wait.until(EC.element_to_be_clickable((By.ID, "fs_returnDate_0")))
# return_date_input.clear()
# return_date_input.send_keys("Jul 19, 2025")  # Format may vary based on site

# Alternatively, if the calendar requires clicking (instead of direct input)

# return_date_btn = wait.until(EC.element_to_be_clickable(
#     (By.XPATH, "//span[@aria-label='19 July 2025']"))
# )
# return_date_btn.click()

# Close the browser
driver.quit()