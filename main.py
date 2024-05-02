from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

phone_numbers = []

path = "https://www.paginegialle.it/ricerca/Stabilimenti%20balneari/Cervia%20(RA)/p-2?suggest=true"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()

def get_phone_numbers():
    ul_element = driver.find_element(By.CLASS_NAME, "search-itm__ballonIcons")

    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    
    for li_element in li_elements:
        phone_number = li_element.text.strip()
        print(phone_number)
        phone_numbers.append(phone_number)

def click_cookies_button():
    button = driver.find_element(By.ID, "iol_cmp_cont_senz_acce")
    button.click()


driver.get(path)

time.sleep(5)
click_cookies_button()

time.sleep(5)

get_phone_numbers()
print(phone_numbers)

driver.quit()
