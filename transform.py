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