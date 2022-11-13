from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
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
warnings.filterwarnings("ignore")
import pytesseract
import cv2
import linecache
import requests
import math
import pandas as pd

from tabula.io import read_pdf
import re
from difflib import SequenceMatcher

NAME = ''
sn = 0

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
app = Flask(__name__)
api = Api(app)

post_args = reqparse.RequestParser()
post_args.add_argument('n', type=str, required = True)
post_args.add_argument('a', type=str, required = True)
post_args.add_argument("fn", type=str, required = True)
post_args.add_argument('s', type=str, required = True)


def similar(a,b):
        return SequenceMatcher(None,a,b).ratio()

def manda(name,father_husband_name,age,state,city="",district="",vot_id="",gender="",loc_area=""):
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.get("https://electoralsearch.in/")
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"continue"))).click()
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
    pyautogui.hotkey('ctrl','v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)

    assembly_num = linecache.getline('ECI _ Voter Information.html', 213).replace('<', '>').split('>')[2]
    global sn
    sn = linecache.getline('ECI _ Voter Information.html', 287).replace('<', '>').split('>')[2]
    pn = int(linecache.getline('ECI _ Voter Information.html', 272).replace('<', '>').split('>')[2])

    driver.close()
    os.remove('ECI _ Voter Information.html')

    driver = webdriver.Chrome(options=options)
    driver.get("https://ceogoa.nic.in/appln/UIL/ElectoralRoll.aspx")
    driver.maximize_window()
    select = Select(driver.find_element(By.ID,"ctl00_Main_drpAC"))
    max = -1
    assembly = ''.join(assembly_num.split(' ')[: : -1]).strip()
    for opt in select.options:
        print(opt.text + " " + str(similar(opt.text,assembly)))
        if(similar(opt.text,assembly) > max):
            max  = similar(opt.text,assembly)
            final = opt

    final.click()
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"ctl00_Main_btnSearch"))).click()
    pdf_url = driver.find_element(By.XPATH,"/html/body/form/div[3]/div[3]/div[1]/div[5]/div/div[{}]/div[{}]/a".format(pn,(pn*2)+1)).get_attribute("href")
    time.sleep(1)

    response = requests.get(pdf_url, verify=False)
    if response.status_code == 200:
        with open("file.pdf","wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)

    

class ELectoral(Resource):
    def post(self):
        args = post_args.parse_args()
        global NAME, sn
        NAME = args["n"]
        
        manda(args["n"],args["fn"],args["a"],args["s"])
        sn = int(sn)
        os.system('qpdf --decrypt file.pdf out.pdf')
        sn_1 = int(sn/31) + 2
        sn_2 = sn_1 + 1
        sn_3 = sn_1 + 2
        os.system('ocrmypdf --pages {},{},{} out.pdf out.pdf'.format(sn_1, sn_2, sn_3))

        x_1 = 24.6
        y_1 = 51.24
        w = 180.0
        h = 70.13
        y_2 = y_1 + h
        x_2 = x_1 + w
        c = 0
        ser_no = sn
        # print(tb.read_pdf(file, pages=3, area=(y1, x1, y2, x2)))
        persons = []

        low=0
        high=0
        if ser_no%31 >= 27:
            low = math.floor(ser_no/31) + 3
            high = low + 1
        elif ser_no%31 <= 4:
            high = math.floor(ser_no/31) + 3
            low = high - 1
        else:
            high = math.floor(ser_no/31) + 3
            low = math.floor(ser_no/31) + 3

        flag = low-high
        for page in range(low,high+1,1):

            if flag==0:
                for i in range(3):
                    x1 = x_1 +  i*w
                    x2 = x_2 +  i*w

                    y1 = y_1 + (math.floor((ser_no%31)/3 - 2))*h
                    y2 = y_1 + h + (math.floor((ser_no%31)/3 - 2))*h
                    for j in range(3):
                        y1 = y1 +  h 
                        y2 = y2 +  h 
                # print(y1,x1,y2,x2)
                        data = read_pdf('out.pdf', pages=page, area=(y1, x1, y2, x2-w/3), encoding='ISO-8859-1')
                        persons.append(data)
            else:
                for i in range(3):
                    x1 = x_1 +  i*w
                    x2 = x_2 +  i*w

                    y1 = y_1
                    y2 = y_1 + h

                    for j in range(10):
                        y1 = y_1 +  j*h 
                        y2 = y_2 +  j*h 

                    # print(y1,x1,y2,x2)
                        data = read_pdf('out.pdf', pages=page, area=(y1, x1, y2, x2-w/3), encoding='ISO-8859-1')
                        persons.append(data)

        def remove_el(el,list1):
            for i in el:
                while (list1.count(i)):
                    list1.remove(i)
            return list1

        def person_dict(person):
            list1 = person.split()
            rem_el = ["0","1","2","3","4","NaN",":","Unnamed:","=","|"]
            list1 = remove_el(rem_el,list1)

            Relations = ["Father's","Mother's","Wife's","Husband's"]

            if "Name" not in list1[0]:
                list1.pop(0)

            dict1 = {"Name":"","F":"","W":"","H":"","M":"","S":"","Hno":"","Age":"","Gender":""}

            i=0
            while i<len(list1):
                j=1
                str1 = ""
                while j<len(list1) and list1[j] not in Relations:
                    str1 += list1[j] + " "
                    j+=1
                dict1["Name"] = str1

                if list1[i] in  Relations:
                    j = i+2
                    str1 = ""
                    while "House".lower() not in list1[j].lower():
                        str1 += list1[j]+" "
                        j+=1

                    if list1[i].lower() in "Father's".lower():
                        dict1["F"] = str1
                
                    if list1[i].lower() in "Mother's".lower():
                        dict1["M"] = str1

                    if list1[i].lower() in "Wife's".lower():
                        dict1["W"] = str1

                    if list1[i].lower() in "Husband's".lower():
                        dict1["H"] = str1
                

                if  i+1<len(list1) and "Gender".lower() in list1[i].lower():
                    dict1["Gender"] = list1[i+1]

                if i+1<len(list1) and "Age".lower() in list1[i].lower():
                    dict1["Age"] = list1[i+1]

            

                if 'House'.lower() in list1[i].lower():
                    str1 = ""
                    j=i+2
                    while j<len(list1) and "Age".lower() not in list1[j].lower():
                        if j<len(list1):
                            str1 += list1[j]
                            j+=1
                    dict1["Hno"] = str1
                
                i+=1
            print(dict1)
            return dict1



        persons_obj = []
        for i in range(len(persons)):
            if (len(persons[i]) > 0):
                persons_obj.append(person_dict(persons[i][0].to_string()))

        print(persons_obj)




        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        def get_person(name,persons_obj):
            for person in persons_obj:
                if(similar(name,person["Name"])>0.8):
                    return person




        def get_relations(name,rel,persons_obj):
            person = get_person(name,persons_obj)

            def func(per):
                # print(re.sub(r'[^\w\s]', '', person["Hno"]),re.sub(r'[^\w\s]', '', per["Hno"]))
                if similar(re.sub(r'[^\w\s]', '', person["Hno"]),re.sub(r'[^\w\s]', '', per["Hno"])) > 0.8:
                    return True
                else:
                    return False

            return list(filter(func, persons_obj))

        pn = NAME

        opp_relations = {'F' : 'S', 'S' : 'F', 'W' : 'H', 'H' : 'W', 'M' : 'S', 'S' : 'M'}
        relations = ['F', 'S', 'M', 'H', 'W']

    # x = get_relations(pn, '', persons_obj)

        

        output = []
        for i in persons_obj:
            if (similar(i['Name'], pn) > 0.8) :
                for r in relations:
                    if (i[r]):
                        output.append({'Name' : i[r], 'Relation' : r})

                        for i_1 in persons_obj:
                            if (similar(i_1['Name'].split()[0], i[r].split()[0]) > 0.8) :
                                for r1 in relations:
                                    if (i_1[r1]!=""):  
                                        output.append({'Name' : i_1[r1], 'Relation' :  r+opp_relations[r1]})      
                                        
            else:
                for r in relations:
                    if (i[r]!="" and similar(i[r].split()[0], pn.split()[0]) > 0.85):        
                        output.append({'Name' : i['Name'], 'Relation' : opp_relations[r]})

                        for i_1 in persons_obj:
                            for r1 in relations:
                                if (i_1[r1]!="" and similar(i_1[r1].split()[0], i["Name"].split()[0]) > 0.85):
                                    output.append({'Name' : i_1['Name'], 'Relation' :  opp_relations[r]+opp_relations[r1]})        
                                  

        return output


api.add_resource(ELectoral, '/electoral')

if __name__ == '__main__':
    app.run(debug = True)
   
    

