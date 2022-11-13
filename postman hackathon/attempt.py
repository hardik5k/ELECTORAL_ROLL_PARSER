from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import os
import subprocess
import time
import pyautogui
import pyperclip
from difflib import SequenceMatcher
import warnings
from tkinter import *
import pytesseract
import cv2 
import linecache
import requests


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
warnings.filterwarnings("ignore")

def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.maximize_window()
driver.get("https://electoralsearch.in/")
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"continue"))).click()
file = open("info.txt")
name = file.readline()
father_husband_name = file.readline()
age = file.readline()
city = file.readline()
state = file.readline()
district = file.readline()
loc_area = file.readline()
vot_id = file.readline()
gender = file.readline()

WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"name1"))).send_keys(name)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"txtFName"))).send_keys(father_husband_name)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"ageList"))).send_keys(age)

gen_dropdown = Select(driver.find_element(By.ID,"listGender"))
gen_dropdown.select_by_value('M')

state_dropdown = Select(driver.find_element(By.ID,"nameStateList"))
state_dropdown.select_by_visible_text(state.strip())

bool = True
while bool:
    with open('captcha.png','wb') as file:
        image = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"captchaDetailImg")))
        file.write(image.screenshot_as_png)
    
    img = cv2.imread("captcha.png")
    img = cv2.resize(img, None, fx=2, fy=2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 20)
    f = (pytesseract.image_to_string(adaptive)).strip()

    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"txtCaptcha"))).send_keys(f)
    time.sleep(1)
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[4]/div[2]/div/div/div[1]/form/fieldset/div/div[4]/div[2]/div[2]/button"))).click()
    time.sleep(1)
    text = "कुल परिणाम / Number of Record(s) Found: 0"
    if text in driver.page_source:
        bool = True
    else:
        bool = False
    os.remove("captcha.png")

path_given =  os.getcwd()
pyperclip.copy(path_given)
print(path_given)
print("ok")
time.sleep(3)
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[5]/div[3]/div[2]/div/table/tbody/tr/td[1]/form/input[25]"))).click()
time.sleep(2)
pyautogui.hotkey('ctrl','s')
time.sleep(1)
# path_given = "D:\College\postman hackathon"
pyautogui.hotkey('ctrl','v')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.press('enter')
time.sleep(5)

assembly_num = linecache.getline('ECI _ Voter Information.html', 213).replace('<', '>').split('>')[2]
sn = linecache.getline('ECI _ Voter Information.html', 287).replace('<', '>').split('>')[2]

print(assembly_num)
print(sn)

driver.close()
os.remove("ECI _ Voter Information.html")

driver = webdriver.Chrome(options=options)
driver.get("https://ceogoa.nic.in/appln/UIL/ElectoralRoll.aspx")
driver.maximize_window()
select = Select(driver.find_element(By.ID,"ctl00_Main_drpAC"))
max = -1
ans = district + 
for opt in select.options:
    if(similar(opt.text,district) > max):
        max  = similar(opt.text,district)
        final = opt

final.click()
part = 12
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"ctl00_Main_btnSearch"))).click()
pdf_url = driver.find_element(By.XPATH,"/html/body/form/div[3]/div[3]/div[1]/div[5]/div/div[12]/div[{}]/a".format((part*2)+1)).get_attribute("href")
time.sleep(1)

response = requests.get(pdf_url, verify=False)
if response.status_code == 200:
    with open("file.pdf","wb") as f:
        f.write(response.content)
else:
    print(response.status_code)

subprocess.call(['sh', './test.sh'])
