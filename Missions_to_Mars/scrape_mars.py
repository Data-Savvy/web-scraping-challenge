# Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    scraped_data={}

    # ******************************************************************************************************************************
    # Scraping Mars News
    # *****************************************************************************************************************************
    url = 'https://mars.nasa.gov/news/'
    print("Scraping Mars News...")
    
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    division_2 = soup.find('div', class_='list_text') 

    content_title = division_2.find('div', class_='content_title')

    news_title = content_title.text.strip()
    news_p = division_2.find('div', class_='article_teaser_body').text.strip()

    print("Mars News: Scraping Complete!")

   
    # *****************************************************************************************************************************
    # Scraping JPL Featured Image URL 
    # *****************************************************************************************************************************
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)
    time.sleep(1)

    print("Scraping JPL Featured Space Image...")

    html2 = browser.html
    soup = bs(html2, 'html.parser')

    picture_div = soup.find('div', class_='carousel_items')
    footer=picture_div.find('footer')
    data_url='https://www.jpl.nasa.gov' + footer.find('a')['data-link']
    
    url_3 = data_url
    browser.visit(url_3)
    time.sleep(1)

    html3 = browser.html
    soup = bs(html3, 'html.parser')
    figure = soup.find('figure', class_='lede')
    large_picture_url=figure.find('a')['href']

    featured_image_url='https://www.jpl.nasa.gov' + large_picture_url

    print("JPL Featured Space Image: Scraping Complete!")


    # *****************************************************************************************************************************
    # Scraping Mars Weather Tweet
    # *****************************************************************************************************************************
    
    url_4 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_4)
    time.sleep(1)

    print("Scraping Mars Weather's Twitter Account...")

    html4 = browser.html
    soup = bs(html4, 'html.parser')

    mars_weather = soup.find_all('span', class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[27].text.replace('\n',' ')
 
    print("Mars Weather: Scraping Complete!")


    # *****************************************************************************************************************************
    #  Scraping Mars Facts
    # *****************************************************************************************************************************
    url_5 = 'https://space-facts.com/mars/'
    browser.visit(url_5)
    time.sleep(1)

    print("Scraping Mars Facts...")
    
    html5 = browser.html
    tables = pd.read_html(html5)

    mars_facts=tables[0]
    mars_facts.columns=['Mars Description', 'Value']
    mars_earth=tables[1]

    mars_facts=mars_facts.to_html(index=False, header=False, border=0, classes="table table-sm table-striped font-weight-light")

    mars_earth=mars_earth.to_html()

    print("Mars Facts: Scraping Complete!")


    # *****************************************************************************************************************************
    #  Scraping Mars Hemisphere images
    # *****************************************************************************************************************************
    url_6 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_6)
    time.sleep(1)

    html6 = browser.html
    soup = bs(html6, 'html.parser')
    hemisphere_results = soup.find_all('div', class_='item')

    hemisphere_image_data =[]

    for hemisphere in range(len(hemisphere_results)):

        # --- use splinter's browser to click on each hemisphere's link in order to retrieve image data ---
        link = browser.find_by_tag("h3")
        link[hemisphere].click()
        time.sleep(1)
        
        # --- create a beautiful soup object with the image detail page's html ---
        img_html = browser.html
        imagesoup = bs(img_html, 'html.parser')
        
        # --- retrieve the full-res image url and save into a variable ---
        img_li = imagesoup.find('li')
        img_url = img_li.find('a')['href']


        img_title = browser.find_by_tag("h2").text
        img_title

        # --- add the key value pairs to python dictionary and append to the list ---
        hemisphere_image_data.append({"title": img_title,
                                "img_url": img_url})
            # --- go back to the main page ---
        browser.back()
    
    # --- close the browser session ---    
    browser.quit()

    print("Mars Hemisphere Images: Scraping Complete!")



    # *****************************************************************************************************************************
    #  Store all values in dictionary
    # *****************************************************************************************************************************

    scraped_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featuredimage_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_fact_table": mars_facts, 
        "mars_earth_comparison":mars_earth,
        "hemisphere_images": hemisphere_image_data
    }

    # --- Return results ---
    return scraped_data