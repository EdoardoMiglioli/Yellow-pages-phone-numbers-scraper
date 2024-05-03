from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import time

business_infos = []

path = "https://www.paginegialle.it/ricerca/Stabilimenti%20balneari/Cervia%20(RA)/p-2?suggest=true"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()

def click_cookies_button():
    button = driver.find_element(By.ID, "iol_cmp_cont_senz_acce")
    button.click()

def get_phone_numbers(ul_element):
    phone_numbers = ""

    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    
    for li_element in li_elements:
        li_element_innerHTML = li_element.get_attribute("innerHTML")
        print(type(li_element_innerHTML))
        CLEANR = re.compile('<.*?>') 
        raw_phone_number = re.sub(CLEANR, '', li_element_innerHTML)
        phone_number = int(''.join(i for i in raw_phone_number if i.isdigit()))
        print("phone numebr: ", phone_number)
        phone_numbers += f"{phone_number} "

    return phone_numbers

def append_business_infos(name, phones):
    info = {
        "name": name, 
        "phones": phones
    }

    business_infos.append(info)
    

def get_cards_info():
    cards = driver.find_elements(By.CLASS_NAME, "search-itm")

    for card in cards:
        try:
            ul_element = card.find_element(By.CLASS_NAME, "search-itm__ballonIcons")
        except Exception:
            print("ERROR itereting cards")
            continue

        phones = get_phone_numbers(ul_element)
        name = card.find_element(By.CLASS_NAME, "search-itm__rag").text

        append_business_infos(name, phones)


driver.get(path)

time.sleep(3)
click_cookies_button()

time.sleep(3)

get_cards_info()
print(business_infos)

time.sleep(3)

driver.quit()
