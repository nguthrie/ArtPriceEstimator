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

# refactor this code:
# get clearfix class, which has all info, get images and price, save together
# instead of in two separate loops
# will need to go into the urls to get the full size pictures...


# NOTE: not working
ads = soup.find_all('div', {'class': 'clearfix'})
for ad in ads:
    # using regrex to strip internal empty space
    #print(re.sub(' +', ' ', ad.find('a', {"class": "title"}).text.strip()))
    print(ad.find('a', {"class": "title"}).text.strip())
    print(ad.find('div', {"class": "price"}).text.strip())
    print(ad.find('image'))


# this is the syntax for getting attributes with specific tags
info_containers = soup.find_all('div', {"class": "info-container"})
for ad in info_containers:
    # print(ad)
    # print(ad.find('a', {"class": "title"}).text.strip())
    print(re.sub(' +', ' ', ad.find('a', {"class": "title"}).text.strip()))
    print(ad.find('div', {"class": "price"}).text.strip())
    if ad.find('div', {"class": "description"}) != "":
        print(ad.find('div', {"class": "description"}).text.strip())
    else:
        print("No description.")
    break


images = soup.find_all('img')
for image in images:
    print(image)
    print(image.get('data-src'))

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
