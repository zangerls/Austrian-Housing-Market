import scrape as sc
import transform as tr
import estate as es
import db

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