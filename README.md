# Austrian Housing Market

In this project I scraped the data of over 20.000 available properties in Austria, including postal code (and province), number of rooms, indoor area, garden area and price.
The data has subsequently been transformed and cleaned before being loaded into a local MariaDB database and temporarily being saved inside Python as Estate objects.

With every scraping of the web page, the data is also loaded into a csv file, which is used for training and testing three simple regression models to predict the house's price.

## Scraping the data

The data source is Austrian real-estate website [ImmobilienScout24.](https://www.immobilienscout24.at/regional/oesterreich/immobilie-kaufen/aktualitaet)

The tool used to scrape the data from the aforementioned webpage is Python's library 'BeautifulSoup'.

### scrape.py

```python
from bs4 import BeautifulSoup
import requests

# get html-content of page
def get_page(url):
    page = requests.get(url)
    page = page.content
    soup = BeautifulSoup(page, 'html.parser', from_encoding='iso-8859-1')
    return soup

# get every estate on page
def get_all_estates(page):
    estates_list = page.find('ol', class_='ZJTqu')
    estates = estates_list.find_all('li', class_='lSese')
    return estates

# get relevant data of every estate on page
def get_estates_data(estates):
    estate_data_collection = []
    for estate in estates:
        estate_data = estate.find('section', class_='gSPlT')
        estate_data_collection.append(estate_data)
    return estate_data_collection

# get address of individual estate
def get_address(estate):
    address = (estate.find('address')).text.strip()
    return address

# get key data (rooms, square metres, price, ...)
def get_key_data(estate):
    key_data = estate.find('ul', class_='DHILY')
    key_data_li = key_data.find_all('li')

    features = []
    for li in key_data_li:
        features.append(li.text.strip())
    
    return features
```

## Cleaning & Transforming the data

The scraped data reaches the Python environment in neither the right data types nor in a uniform structure. Therefore, the data is subsequently cleaned and further transformed to be properly stored in the database and csv file.

### transform.py

```python
def classify_key_data(key_data):
    rooms = 0
    sqm = 0
    sqm_garden = 0
    price = 0

    # get price
    price_raw = key_data[-1].encode()
    key_data.pop()

    price_raw = (str(price_raw))[2:]

    price_raw = price_raw.split(' ')
    price_raw = price_raw[0]

    price_raw = price_raw.replace('.','')
    price_raw = price_raw.replace(',','')
    try:
        price = int(price_raw)
    except:
        price = 0

    for item in key_data:
        if 'Zimmer' in item:
            rooms = int(''.join([x for x in item if x.isdigit()]))
        elif 'Garten' in item:
            parts = item.split(' ')
            parts = parts[0].replace('.','')
            parts = parts.replace(',','.')
            sqm_garden = int(float(parts))
        elif 'Fl' in item:
            parts = item.split(' ')
            parts = parts[0].replace('.','')
            parts = parts.replace(',','.')
            sqm = int(float(parts))
        else:
            continue

    return [rooms, sqm, sqm_garden, price]
            
def postal_code(address):
    if address[:4].isdigit():
        return int(address[:4])
    else:
        try:
            parts = address.split(',')
            area = parts[1]
            area = area.strip()
            return int(area[:4])
        except:
            return None
```

## Creating 'Estate' Objects

To conveniently and uniformly store the vast amounts of estates, scraped from the webpage, I create an Estate object with the previously transformed data.

### estate.py

```python
from transform import postal_code


class Estate:
    def __init__(self, postal_code, rooms, area, garden_area, price):
        self.postal_code = postal_code
        self.rooms = rooms
        self.area = area
        self.garden_area = garden_area
        self.price = price

    def get_postal_code(self):
        return self.postal_code

    def get_rooms(self):
        return self.rooms

    def get_area(self):
        return self.area

    def get_garden_area(self):
        return self.garden_area

    def get_price(self):
        return self.price

all_estates = []
def estate_collection(estate):
    all_estates.append(estate)

estates_list = []
def append_estates_list(postal_code, rooms, area, garden_area, price):
    estate_lst = [postal_code, rooms, area, garden_area, price]
    estates_list.append(estate_lst)
```

## Database functionality in Python

The DBMS used for the project was a locally hosted MariaDB database on my personal PC.

### db.py

```python
import mariadb as mdb
import sys

def create_connection():
    try:
        con = mdb.connect(
            user='root',
            host='localhost',
            database='housing'
        )
    except mdb.Error as e:
        print(e)
        sys.exit(1)

    return con.cursor()

def insert(estate, cursor):
    postal_code = estate.get_postal_code()
    rooms = estate.get_rooms()
    area = estate.get_area()
    garden_area = estate.get_garden_area()
    price = estate.get_price()

    try:
        cursor.execute(
            'INSERT INTO estates (postal_code, rooms, area, garden_area, price) VALUES (?,?,?,?,?);',
            (postal_code, rooms, area, garden_area, price)
        )
    except mdb.Error as e:
        print(e)
```

## Creating a CSV file

Apart from saving the data during the session in Python as 'Estate' objects and in a MariaDB database, the data is also saved as a csv file for the training of the machine learning models.

### to_csv.py

```python
import csv

def create_csv(data):
    headers = ['postal_code', 'rooms', 'area', 'garden_area', 'price']

    with open('estates.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
```

## Running the program

All the aforementioned files are imported and executed in the main script.

### main.py

```python
import scrape as sc
import transform as tr
import estate as es
import db
import to_csv as csv

# create connection to MariaDB database
cursor = db.create_connection()

# create url
main_URL = 'https://www.immobilienscout24.at/regional/oesterreich/immobilie-kaufen/aktualitaet'

# create function to scrape and transform the data, create an object and insert data into database
def run(url):
    # get raw html from page
    page_html = sc.get_page(url)
    raw_estates = sc.get_all_estates(page_html)
    estates_data = sc.get_estates_data(raw_estates)
    
    # get every individual estate from page
    for estate in estates_data:
        address = sc.get_address(estate)

        # get only postal code from address
        postal = tr.postal_code(address)

        key_data = sc.get_key_data(estate)

        # list of features [rooms (int), square metres (int), square metres garden (int), price (int)] ('None' if missing)
        clean_key_data = tr.classify_key_data(key_data)
        rooms = clean_key_data[0]
        sqm = clean_key_data[1]
        garden = clean_key_data[2]
        price = clean_key_data[3]

        # create Estate Object from the data
        my_estate = es.Estate(postal, rooms, sqm, garden, price)
        # save estate in Python
        es.estate_collection(my_estate)
        # pass Estate object to database function and insert its attributes into database
        db.insert(my_estate, cursor)
        # create csv file for regressioestn models
        es.append_estates_list(postal, rooms, sqm, garden, price)
        csv.create_csv(es.estates_list)
        
    return

# upper bound = number of pages to scrape (1-100) <- RUN THIS FUNCTION TO START THE PROCESS
def pages(upper_bound):
    # scrape data from {upper bound} pages
    for i in range(1,upper_bound+1):
        if i == 1:
            url = main_URL
        else:
            extension = f'/seite-{i}'
            url = main_URL + extension
        run(url)

if __name__ == '__main__':
    pages(100)
```

## Machine Learning

As a quick preview to how the data might get used for analysis, I created a small machine learning note
