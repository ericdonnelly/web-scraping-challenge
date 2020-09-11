from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from flask_pymongo import PyMongo as pymongo
import requests

#urls
nasa_news_url = 'https://mars.nasa.gov/news/'
space_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
space_fact_url = "https://space-facts.com/mars/"
base_hemisphere_url = "https://astrogeology.usgs.gov"
hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "./chromedriver.exe"}
    return Browser("chrome", **executable_path)


def scrape_mars():
    browser = init_browser()
#nasa news url
    try:
        # Visit visitcostarica.herokuapp.com
        browser.visit(nasa_news_url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        #a = soup.find('div', class_="list_text")
        news_title = soup.find('div', class_= "content_title").text
        news_paragraph = soup.find('div', class_= "rollover_description_inner").text
    except:
        news_title = 'abort mission'
        news_paragraph ='abort mission'
#space image url
    try:
        # Visit visitcostarica.herokuapp.com
        browser.visit(space_image_url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        featured_image = soup.find("img", class_="thumb")["src"]
        featured_image_url ="https://jpl.nasa.gov"+ featured_image
    except:
        featured_image = 'abort mission'
#hemisphere
    try:
        browser.visit(hemisphere_url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        items = soup.find_all('div', class_='item')
        hemisphere_image_urls = []
        for item in items: 
            title = item.find('h3').text
            partial_img_url = item.find('a', class_='itemLink product-item')['href']
            url = base_hemisphere_url + partial_img_url
            browser.visit(url)
            html = browser.html
            soup = bs( html, 'html.parser')
            img_url = base_hemisphere_url + soup.find('img', class_='wide-image')['src']
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    except:
        hemisphere_image_urls = 'abort mission'

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls,
    }
    mars_data['hemisphere_image_urls'] =hemisphere_image_urls
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data