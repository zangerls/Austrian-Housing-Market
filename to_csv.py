import csv

def create_csv(data):
    headers = ['postal_code', 'rooms', 'area', 'garden_area', 'price']

    with open('estates.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

