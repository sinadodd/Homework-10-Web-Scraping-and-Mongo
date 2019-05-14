from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pymongo
import pandas as pd

def scrape():

    final_dict = {}

    # ### NASA Mars News:
    # example:
    # news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
    # news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    final_dict['news_title'] = news_title
    final_dict['news_p']= news_p
    
    browser.quit()

    # ### JPL Mars Space Images - Featured Image
    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA18249_hires.jpg'

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')
    time.sleep(1)
    featured_image_url = browser.url
    final_dict["featured_image_url"] = featured_image_url

    browser.quit()

    # ### Mars Weather
    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    # # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    final_dict['mars_weather'] = mars_weather

    browser.quit()

    # ### Mars Facts
    # * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # * Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    df = tables[0]
    df.rename(columns={0:'Fact', 1:'Value'}, inplace=True)
    df.set_index('Fact', inplace=True)

    html_table = df.to_html()
    final_dict['html_table'] = html_table

    # ### Mars Hemispheres
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    #     ]

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls = []
    hemisphere_names = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']

    for name in hemisphere_names:
        browser.click_link_by_partial_text(name)
        time.sleep(1)
        hemisphere_url = browser.find_link_by_partial_text('Sample').first['href']
        hemisphere_image_urls.append({"title": name, "img_url": hemisphere_url})
        browser.back()   
    browser.quit()

    final_dict["hemisphere_image_urls"] = hemisphere_image_urls

    return final_dict

    # ## Step 2 - MongoDB and Flask Application
    # 
    # Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
    # 
    # * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
    # 
    # * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
    # 
    #   * Store the return value in Mongo as a Python dictionary.
    # 
    # * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
    # 
    # * Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.