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

    try:
        # Visit visitcostarica.herokuapp.com
        browser.visit(nasa_news_url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        news_title = soup.find('div', class_= "content_title").text

        news_paragraph = soup.find('div', class_= "rollover_description_inner").text
    except:
        news_title = 'abort mission'
        news_paragraph ='abort mission'

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
