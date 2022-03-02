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