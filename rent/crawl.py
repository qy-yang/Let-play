from bs4 import BeautifulSoup
import requests
import csv
import time
import lxml
import re

# url = 'https://bj.58.com/pinpaigongyu/?minprice=1500_2000'
url = 'https://www.99.co/singapore/rent?listing_type=rent&page_num=10'
'&page_size=25&price_max=1500&price_min=1000&property_segments=residential'

# Completed pages
page = 0

csv_file = open('rent.csv', 'w')
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print('Fetch: ', url.format(page=page))
    time.sleep(1)
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text, features='lxml')

    # break the loop when no new house list
#   if not house_list:
#       break

    # house title
    house_title = html.select('h4')
    if not house_title:  # break the loop until the last page
        break
    # house price
    house_money = html.select('h5')
    # house address
    house_addr = html.select('p[class="listing-list-item__subtitle__DYgqU"]')
    pattern = re.compile('.*D[0-9]+')
    house_location = [h.string for h in house_addr if h.string is not None and pattern.match(h.string)]
    # house url
    house_url = house.select('a')['href']
    # house_info_list = house_title.split()

    rows = zip([house_title, house_location, house_money, house_url])
    for row in rows:
        csv_writer.writerow(row)


    csv_file.close()