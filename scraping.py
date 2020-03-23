# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    #set news title and paragraph varables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "cerberus": cerberus(browser),
        "schiaparelli": schiaparelli(browser),
        "sytris": syrtis(browser),
        "valles": valles(browser)
    }

    return data

def mars_news(browser):

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    try:
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_paragraph


# Featured Images
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():

    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    #assign columns and set index of df
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    #convert df into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

def cerberus(browser):

    #visit url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #click first picture
    browser.is_element_present_by_text('Cerberus Hemisphere Enhanced', wait_time=1)
    img_pg1 = browser.links.find_by_partial_text("Cerberus Hemisphere Enhanced")
    img_pg1.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #get image url
    cerb_img_url = img_soup.select_one("div.wide-image-wrapper ul li a").get("href")
    
    return cerb_img_url

def schiaparelli(browser):

    #visit url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #click second picture
    browser.is_element_present_by_text('Schiaparelli Hemisphere Enhanced', wait_time=1)
    img_pg2 = browser.links.find_by_partial_text("Schiaparelli Hemisphere Enhanced")
    img_pg2.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #get image url
    schi_img_url = img_soup.select_one("div.wide-image-wrapper ul li a").get("href")
    
    return schi_img_url

def syrtis(browser):

    #visit url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #click third picture
    browser.is_element_present_by_text('Syrtis Major Hemisphere Enhanced', wait_time=1)
    img_pg3 = browser.links.find_by_partial_text("Syrtis Major Hemisphere Enhanced")
    img_pg3.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #get image url
    syrt_img_url = img_soup.select_one("div.wide-image-wrapper ul li a").get("href")
    
    return syrt_img_url

def valles(browser):

    #visit url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #click forth picture
    browser.is_element_present_by_text('Valles Marineris Hemisphere Enhanced', wait_time=1)
    img_pg4 = browser.links.find_by_partial_text("Valles Marineris Hemisphere Enhanced")
    img_pg4.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #get image url
    vall_img_url = img_soup.select_one("div.wide-image-wrapper ul li a").get("href")
    
    return vall_img_url