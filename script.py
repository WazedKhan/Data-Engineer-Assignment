import os
import csv
import time
import sqlite3
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from pathlib import Path
Path("product").mkdir(parents=True, exist_ok=True)
Path("offers").mkdir(parents=True, exist_ok=True)


# providing location by automating browser
driver = webdriver.Chrome("D:\Selenium\chromedriver.exe")
driver.get('https://www.pizzahutbd.com/deals/all')
driver.find_element(By.CLASS_NAME, 'tab-content').click()

loc_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'pac-input')))
loc_input.click()
loc_input.send_keys('Dhaka')
time.sleep(5)
loc_input.send_keys(Keys.ARROW_DOWN)
loc_input.send_keys(Keys.ENTER)


# sleep 10 sec to load the page proparly
time.sleep(10)
soup = BeautifulSoup(driver.page_source)



# to extract data for different products from PizzaHut
def ETL(soup2):
    category = soup2.find('a', attrs={'class':'nav-link active'}).text
    page_name = 'PizzaHut'

    items = soup2.find_all('div', class_ = 'pizzaPrice')

    csv_file = open(f'product/{category}.csv','w', newline = '')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['name', 'description', 'category', 'price','page_name', 'loc'])

    items = soup2.find_all('div', class_ = 'container thame collapseExample')

    count = 0
    for item in items:
        name = item.find('div', class_ = 'left-con-pizzas').text
        type = item.find('label', class_ = 'product_size_label').text
        name = name+' - '+type
        description = item.find('p', class_ = 'short_desc').text
        price = item.find('span', class_ = 'pro_price').text
        category = category
        page_name = page_name
        loc = 'Dhaka' # setting default loc to Dhaka
        count += 1
        csv_writer.writerow([name, description, category, price,page_name, loc])

    csv_file.close()



list_ = ['pasta', 'appetisers', 'drinks']
for i in list_:
   driver.get(f'https://www.pizzahutbd.com/{i}/all')
   time.sleep(10)
   soup2 = BeautifulSoup(driver.page_source)
   ETL(soup2)
# Storing offer page for pizzaHut
driver.get('https://www.pizzahutbd.com/deals/all')
hutOffer = BeautifulSoup(driver.page_source)
driver.close()


page_name = 'PizzaHut'
category = soup.find('a', attrs={'class':'nav-link active'}).text

items = soup.find_all('div', class_ = 'pizzaPrice')
prices = []

for i in items:
    prices.append(i.text)

price_list =  [' '.join(prices[i:i+3]) for i in range(0, len(prices), 3)]

csv_file = open('product/Pizza.csv','w', newline = '')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'description', 'category', 'price','page_name', 'loc'])


items = soup.find_all('div', class_ = 'container thame collapseExample')

count = 0
for item in items:
    name = item.find('div', class_ = 'left-con-pizzas').text
    description = item.find('p', class_ = 'short_desc').text
    price = price_list[count]
    category = category
    page_name = page_name
    loc = 'Dhaka'
    count += 1
    csv_writer.writerow([name, description, category, price,page_name, loc])

csv_file.close()


df = pd.read_csv('product/Pizza.csv')
df.head()



df[['Personal_S_Price', 'price', 'Large_S_Price']] = df['price'].str.split(' ', expand=True)


df.to_csv('product/Pizza.csv')
df = pd.read_csv('product/Pizza.csv')
df.head()


URL = "https://madchef.com.bd/menu"
page = requests.get(URL).text

soup = BeautifulSoup(page, features="xml")

page_name = 'Madchef'
items = soup.find_all('div', class_ = 'menumodal modal')

csv_file = open('product/Madchef.csv','w', newline = '')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'description', 'category', 'price','page_name', 'loc'])

# finding locs of Madchef's

loc_page = requests.get('https://madchef.com.bd/contact#branches').text
soup_loc = BeautifulSoup(loc_page, features="xml")

locs = soup_loc.find_all('div', class_ ='branch-name ')
locations=[]
for i in locs:
    locations.append((i.text).strip())

for item in items:

    name = (item.find('div', class_='menumodal-title').text).strip()
    if name.split()[-1] == '🌶':
        name = ' '.join(name.split()[:-1])

    description = (item.find('div', class_='menumodal-description').text).strip()
    category = ((item.find('div', class_='menumodal-category').text).strip().split(':')[1]).strip()
    price = (item.find('div', class_='menumodal-price').text).strip().split()[1]
    page_name = page_name
    loc = locations

    csv_writer.writerow([name, description, category, price, page_name, loc])


csv_file.close()

df = pd.read_csv('product/Madchef.csv')
df.head(50)



page_name = 'PizzaHut'

csv_file = open(f'offers/hut.csv','w', newline = '')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'description', 'category', 'price','page_name'])

items = hutOffer.find_all('div', class_ = 'deals_card')
for item in items:
    name = (item.find('div', class_ = 'deal-item-name').text).strip()
    description = (item.find('div', class_ = 'deal-item-desc').text).strip()
    category = 'Pizza'
    page_name = page_name
    csv_writer.writerow([name, description, category, page_name])

csv_file.close()



filepath= './product/'

filenames = list(filter(lambda x: '.csv' in x, os.listdir(filepath)))
li = []

for filename in filenames:
    df = pd.read_csv(filepath+filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.tail(50)
df = frame.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1, errors='ignore')
df['Personal_S_Price'] = df['Personal_S_Price'].fillna(0)
df['Large_S_Price'] = df['Large_S_Price'].fillna(0)
df.tail()

df.to_csv('products.csv')

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS products (name text, description text, price number, page_name text, low_price number, high_price number)')
conn.commit()

c.execute('CREATE TABLE IF NOT EXISTS offers (name text, description text, category text, page_name text)')
conn.commit()

offer = pd.read_csv('offers/hut.csv')
offer.head()

offer.to_sql('offers', conn, if_exists='replace', index = False)


df.to_sql('products', conn, if_exists='replace', index = False)
