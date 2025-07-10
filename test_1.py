from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc  # Use undetected-chromedriver to bypass bot detection

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation flag
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Proxy configuration (replace with your actual proxy details)
PROXY_HOST = "144.22.175.58"
PROXY_PORT = 1080
chrome_options.add_argument(f"--proxy-server=http://{PROXY_HOST}:{PROXY_PORT}")

# Initialize WebDriver with undetected-chromedriver
driver = uc.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    url = "https://www.tripadvisor.com/Hotels"
    driver.get(url)
    
    # Wait for cookie consent banner (customize selector as needed)
    time.sleep(20)
    
finally:
    driver.quit()