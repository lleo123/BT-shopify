import main
import json

URL = 'https://hhlsstore.myshopify.com'
EMAIL = 'lannguyenhoang582000@gmail.com'
PASSWD = 'lanlan'


def write_file(data, file_name='data.json'):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


cookies_dump = main.get_cookies(url=URL, email=EMAIL, passwd=PASSWD)
list_product = main.get_entity(url=URL, entity='products', cookies=cookies_dump, id=6550476456141)

write_file(data=list_product, file_name='products.json')
