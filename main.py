import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
from webserver import keep_alive
import os


global time_left
global progress_bar


# Function to access a website and get the HTML content
def access_website(url):
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Failed to access {url}: {e}")
    return None


# Function to fill an entry box and press a button using Selenium
def fill_and_submit_form(url, entry_box_name, button_name):
  global time_left
  global progress_bar

  if time_left > 0:
    time_left -= 1
    time.sleep(1)
    progress_bar.update(1)

  else:
    progress_bar.close()

    # Use a web driver with headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
  
    # Access the website
    driver.get(url)
    try:
      # Find the entry box and button using their names or other attributes
      entry_box = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.NAME, entry_box_name)))
      button = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.ID, button_name)))
  
      # Fill the entry box
      entry_box.send_keys("Pekapeque")
  
      # Press the button
      button.click()
      time.sleep(10)
  
    finally:
      # Close the browser window
      driver.quit()
  
      time_left = 900
      progress_bar = tqdm(total=time_left, desc="Waiting...", unit="sec")


# Example usage
website_url = "https://faucet.stormsurge.xyz/"
entry_box_name = "firstname"
button_name = "getDucosButton"

html_content = access_website(website_url)
if html_content:
  # You can use BeautifulSoup to parse the HTML content if needed
  soup = BeautifulSoup(html_content, 'html.parser')

  # Fill and submit the form
  time_left = 0
  progress_bar = tqdm(total=time_left, desc="Waiting...", unit="sec")
  
  while True:
    fill_and_submit_form(website_url, entry_box_name, button_name)
    keep_alive()
