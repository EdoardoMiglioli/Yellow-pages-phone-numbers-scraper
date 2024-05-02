from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
    print(li_elements)
    
    for li_element in li_elements:
        phone_number = li_element.text
        print(phone_number)
        phone_numbers += f"{li_element} "

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
