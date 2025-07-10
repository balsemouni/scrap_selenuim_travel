from selenium import webdriver
from selenium.webdriver.common.by import By

# Assuming you already have the driver set up
url = "https://www.tripadvisor.com/Hotels-g187323-Berlin-Hotels.html#SPLITVIEWMAP"

driver = webdriver.Chrome()
driver.get(url)
# Find the hotel name
hotel_name = driver.find_element(By.CSS_SELECTOR, "h3.biGQs._P.fiohW.OgHoE").text

# Find the rating (3.8)
rating = driver.find_element(By.CSS_SELECTOR, "div.biGQs._P.pZUbB.ZNjnF span").text

# Find the review count (823 reviews)
review_count = driver.find_element(By.CSS_SELECTOR, "a[data-automation='bubbleReviewCount'] span").text

# Find the mentions (Classic • Residential Neighborhood • Quiet)
mentions = [mention.text for mention in driver.find_elements(By.CSS_SELECTOR, "div.hJhgY.cpoJM.KJzpk span.biGQs._P.navcl") if mention.text != "Sponsored"]

print(f"Hotel Name: {hotel_name}")
print(f"Rating: {rating}")
print(f"Review Count: {review_count}")
print(f"Mentions: {', '.join(mentions)}")