from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Open Google Maps in headless mode (no browser visible)
options = Options()
options.add_argument("--headless")
options.add_argument("no-sandbox")
service = ChromeService()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com/maps")
driver.implicitly_wait(10)


# Pass destination into text input on Gmaps
def search(destination):
    sleep(1)
    address = driver.find_element(By.ID, "searchboxinput")
    address.send_keys(destination)
    search_button = driver.find_element(By.ID, "searchbox-searchbutton")
    search_button.click()


# Press directions button on Gmaps
def directions():
    sleep(1)
    directions_button = driver.find_element(By.XPATH,
                                     "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
    directions_button.click()


# Press arrive by, and set time user should arrive by, meridiem meaning am or pm
def arrive_by(hour: int, minute: int, meridiem: str):
    sleep(1)
    leave_now = driver.find_element(By.XPATH,
                                   "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/div")
    leave_now.click()
    arrival = driver.find_element(By.ID, ":2")
    arrival.click()
    input_time = driver.find_element(By.XPATH,
                                    "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/span[1]/input")
    sleep(1)
    input_time.clear()
    input_time.send_keys(f"{hour}:{minute}{meridiem}")
    input_time.send_keys(Keys.ENTER)


# Set transportation type from either driving, transit, walking, cycling
def using_transportation(transport_type: int):
    sleep(1)
    transport = driver.find_element(By.XPATH,
                                    "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[1]/button")

    if transport_type == 1:
        transport = driver.find_element(By.XPATH,
                                        "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button")
    elif transport_type == 2:
        transport_type = driver.find_element(By.XPATH,
                                             "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[5]/button")
    elif transport_type == 3:
        transport_type = driver.find_element(By.XPATH,
                                             "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[3]/button")
    elif transport_type == 4:
        transport_type = driver.find_element(By.XPATH,
                                             "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[5]/button")

    transport.click()


# Set starting address
def set_start(start: str):
    sleep(1)
    input_start = driver.find_element(By.XPATH,
                                     "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input")

    input_start.send_keys(f"{start}")
    search_button = driver.find_element(By.XPATH,
                                       "/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/button[1]")
    search_button.click()


# Get "depart by" time
def get_departure():
    sleep(1)
    time = driver.find_element(By.XPATH,
                               "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div/div[1]/div[2]/span")
    return time.text


# Main function that calls all helpers and passes through their required parameters
def scrape_maps(start: str, destination: str, transport_type: int, hour: int, minute: int, meridiem: str):
    search(destination)
    directions()
    using_transportation(transport_type)
    set_start(start)
    arrive_by(hour, minute, meridiem)
    departure = get_departure()
    driver.quit()
    return departure
