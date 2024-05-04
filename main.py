from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import re
import requests
import time
import psycopg2
import os

load_dotenv()

conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST"),
    port='5432'
)

cur = conn.cursor()

business_infos = []

path = "https://www.paginegialle.it/ricerca/stabilimenti%20balneari/Cervia%20(RA)"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()

def click_cookies_button():
    button = driver.find_element(By.ID, "iol_cmp_cont_senz_acce")
    button.click()

def click_more_button():
    button = driver.find_element(By.CLASS_NAME, "next-page-btn")
    button.click()

def get_phone_numbers(ul_element):
    phone_numbers = []

    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    
    for li_element in li_elements:
        li_element_innerHTML = li_element.get_attribute("innerHTML")

        phone_number_pattern = r'\b0?\d{4}\s\d{6}\b'

        matches = re.findall(phone_number_pattern, li_element_innerHTML)
        
        for match in matches:
            phone_numbers.append(match)

        phone_number_pattern_2 = r'\b3\d{2}\s?\d{7}\b'

        matches = re.findall(phone_number_pattern_2, li_element_innerHTML)
        
        for match in matches:
            phone_numbers.append(match)

    return phone_numbers

def append_business_infos(name, phones):
    info = {
        "name": name, 
        "tel": phones
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

def post_info_db(data):
        for row in data:
            try:
                cur.execute(
                "INSERT INTO business (name, tel) VALUES (%s, %s)",
                (row['name'], row['tel'])
                )
        
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("error fetching data to db: ", e)
        



driver.get(path)

time.sleep(3)
click_cookies_button()

time.sleep(3)

is_more_button = True

while is_more_button:
    try:
        click_more_button()
    except:
        is_more_button = False

get_cards_info()


time.sleep(3)

post_info_db(business_infos)

driver.quit()

cur.close()
conn.close()
