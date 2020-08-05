import requests
import urllib
from bs4 import BeautifulSoup as bs
import re
import os

def get_soup(url):

    req = requests.get(url)
    soup = bs(req.text, 'html.parser')

    return soup


soup = get_soup('https://www.kijiji.ca/b-ontario/art/k0l9004?dc=true')

# TO DO: filter for good ads
# 1) remove wanted in title
# 2) remove non-numeric ads
# 3)


class Picture:   # no parenthesis if not sub-classing, i.e. class_name(is subclass of this class)

    def __init__(self, title, price, img_link):
        self.title = title
        self.price = price
        self.img_link = img_link


def print_test():

    ad_containers = soup.find_all('div', {'class': 'clearfix'})
    # skip the first clearfix container
    for ad_container in ad_containers:
        # need to check if the title exists of the strip() will give errors
        # could replace this with exception handling
        if ad_container.find('div', {"class": "title"}):
            print(ad_container.find('div', {"class": "title"}).text.strip())
        if ad_container.find('div', {"class": "price"}):
            print(re.sub(' +', ' ', ad_container.find('div', {"class": "price"}).text.strip()))
        if ad_container.find('img'):
            print(ad_container.find('img').get('data-src'))

# print_test()


def first_page_scraper():

    titles = []
    prices = []
    image_links = []

    ad_containers = soup.find_all('div', {'class': 'clearfix'})

    for ad_container in ad_containers:
        # need to check if the title exists of the strip() will give errors
        # could replace this with exception handling
        if ad_container.find('div', {"class": "title"}) and ad_container.find('div', {"class": "price"}):
            titles.append(ad_container.find('div', {"class": "title"}).text.strip())
            prices.append(re.sub(' +', ' ', ad_container.find('div', {"class": "price"}).text.strip()))  # strip inner whitespace
            image_links.append(ad_container.find('img').get('data-src'))



    return titles, prices, image_links


titles, prices, image_links = first_page_scraper()
print("done")


def saving_pictures():


    # ----- getting the images ----

    images = soup.find_all('img')
    for image in images:
        print(image)
        print(image.get('data-src'))

    # -----saving the images to directory----

        nametemp = image.get('alt')

        i = 0
        if len(nametemp) == 0:
            filename = str(i)
            i += 1
        else:
            filename = nametemp

        image_link = image.get('data-src')
        current_image = urllib.request.urlopen(image_link)
        print(help(current_image))
        print(current_image.length)

        # change directory to save
        os.chdir(r'C:\Users\Nicholas\Programming\ArtPriceEstimator\images')

        if current_image.length > 1000:
            imagefile = open(filename + ".jpeg", 'wb')
            imagefile.write(urllib.request.urlopen(image_link).read())
            imagefile.close()

        break



# a method for getting all the links on the page
''' 
for link in soup.find_all('a'):
    print(link.get('href'))
    print("-------------")
    print(link.text)
'''

# regular_URL = "https://www.kijiji.ca/b-art-collectibles/ontario/art/page-2/k0c12l9004"

# for page in range(1, 10):
