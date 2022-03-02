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