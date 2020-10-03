import requests
import urllib
from bs4 import BeautifulSoup as bs
import re
import os
import time
import random

# TO DO:
# see qualifications to check that the price is reasonable


def get_soup(url):

    req = requests.get(url)
    soup = bs(req.text, 'html.parser')

    return soup


class Picture:   # no parenthesis if not sub-classing, i.e. class_name(is subclass of this class)

    def __init__(self, title, price, img_link):
        self.title = title
        self.price = price
        self.img_link = img_link


def page_scraper(soup):

    titles = []
    prices = []
    image_links = []

    ad_containers = soup.find_all('div', {'class': 'clearfix'})

    for ad_container in ad_containers:
        # need to check if the title exists or the strip() will give errors
        # could replace this with exception handling
        title = ad_container.find('div', {"class": "title"})
        price = ad_container.find('div', {"class": "price"})
        link = ad_container.find('img')   # checking the overall link-container - checking for the url below
        if title and price and link:
            # no wanted, trades/swap or please contact
            wanted = 'wanted' in ad_container.find('div', {"class": "title"}).text.lower()
            # TO-DO: reasonable_price = need to add code for checking if the price is reasonable, i.e. sub $100k
            # cancel: bad code style but I catch it later
            please_contact = ad_container.find('div', {"class": "price"}).text.strip() == 'Please Contact'
            trade = 'trade ' in ad_container.find('div', {"class": "price"}).text.lower()
            url_exists = ad_container.find('img').get('data-src')
            # used following tests to get a good idea for the right length of a title to exclude ads (70 chars)
            title_string = re.sub(' +', ' ', title.text.strip())
            title_length = len(title_string)
            print("Title: {}, length: {}".format(title_string, title_length))
            if not wanted and not please_contact and title_length < 70 and not trade and url_exists:
                prices.append(ad_container.find('div', {"class": "price"}).text.strip())
                # strip inner whitespace
                titles.append(re.sub(' +', ' ', ad_container.find('div', {"class": "title"}).text.strip()))
                # note using the .get to select subparts of html elements
                image_links.append(ad_container.find('img').get('data-src'))
    print('\n')


    return titles, prices, image_links


def saving_pictures(prices_list, titles_list, image_links_list):
    '''

    :param prices_list: list of prices
    :param titles_list: list of titles
    :param image_links_list: list of image_links
    :return: directory of images with prices values for names
    '''

    # set save directory
    os.chdir(r'C:\Users\Nicholas\Programming\ArtPriceEstimator\images')

    # -----saving the images to directory----

    for price, title, image_link in zip(prices_list, titles_list, image_links_list):

        # remove punctuation from title
        title = ''.join([ch for ch in title if ch.isalpha()])
        price = "".join([ch for ch in price if ch == '$' or ch == "." or ch.isdigit()])

        print("Title: {}, Price: {}, Link: {}".format(title, price, image_link))

        image = urllib.request.urlopen(image_link)

        if image.length > 1000:
            name = "{} - {}.jpeg".format(title, price)
            imagefile = open(name, 'wb')
            imagefile.write(image.read())
            imagefile.close()

        time.sleep(10*random.random())


def scrape_first_page():

    current_soup = get_soup('https://www.kijiji.ca/b-art-collectibles/ontario/painting/k0c12l9004?origin=rs ')
    titles, prices, image_links = page_scraper(current_soup)
    print("scraping done / lists populated")
    saving_pictures(prices, titles, image_links)
    print("Post saving images")


# scrape_first_page()


def scrape_second_onwards():

    regular_url = "https://www.kijiji.ca/b-art-collectibles/ontario/art/page-{}/k0c12l9004"
    urls = [regular_url.format(i) for i in range(2, 10)]
    for index, url in enumerate(urls):
        print("CURRENTLY SCRAPING PAGE {}".format(index))
        current_soup = get_soup(url)
        titles, prices, image_links = page_scraper(current_soup)
        saving_pictures(prices, titles, image_links)

        time.sleep(60)

scrape_second_onwards()