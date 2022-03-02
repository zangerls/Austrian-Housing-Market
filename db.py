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
