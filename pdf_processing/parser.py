from tabula.io import read_pdf  
import math
import pandas as pd
import sys
import re


file = sys.argv[1]
df = pd.DataFrame()
x_1 = 24.6
y_1 = 51.24
w = 180.0
h = 70.13
y_2 = y_1 + h
x_2 = x_1 + w
c = 0
ser_no = int(sys.argv[3])
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


print(low,high)
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
            print(y1,x1,y2,x2)
            data = read_pdf(file, pages=page, area=(y1, x1, y2, x2-w/3))
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
            data = read_pdf(file, pages=page, area=(y1, x1, y2, x2-w/3))
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


import re
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_person(name,persons_obj):
  for person in persons_obj:
    if(similar(name,person["Name"])>0.8):
      return person
    

# if get_person("KOTESWARA RA",persons_obj):
# print(get_person("KOTESWARA RA",persons_obj)["Name"])


def get_relations(name,rel,persons_obj):
  person = get_person(name,persons_obj)

  def func(per):
    # print(re.sub(r'[^\w\s]', '', person["Hno"]),re.sub(r'[^\w\s]', '', per["Hno"]))
    if similar(re.sub(r'[^\w\s]', '', person["Hno"]),re.sub(r'[^\w\s]', '', per["Hno"])) > 0.8:
      return True
    else:
      return False

  return list(filter(func, persons_obj))

pn = sys.argv[2].replace('_', ' ')

opp_relations = {'F' : 'S', 'S' : 'F', 'W' : 'H', 'H' : 'W', 'M' : 'S', 'S' : 'M'}
relations = ['F', 'S', 'M', 'H', 'W']

# x = get_relations(pn, '', persons_obj)

person_relations = []

for i in persons_obj:
  if (similar(i['Name'], pn) > 0.8) :
    for r in relations:
      if (i[r]):
          print(i[r], r)

          for i_1 in persons_obj:
            if (similar(i_1['Name'].split()[0], i[r].split()[0]) > 0.8) :
                for r1 in relations:
                    if (i_1[r1]!=""):        
                        print(i_1[r1], r+r1)
          
  else:
    for r in relations:
      if (i[r]!="" and similar(i[r].split()[0], pn.split()[0]) > 0.85):        
        print(i['Name'], opp_relations[r])

        for i_1 in persons_obj:
            for r1 in relations:
                if (i_1[r1]!="" and similar(i_1[r1].split()[0], i["Name"].split()[0]) > 0.85):        
                    print(i_1['Name'], opp_relations[r]+opp_relations[r1])