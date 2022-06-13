from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    mars_url = "https://redplanetscience.com/"
    browser.visit(mars_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find_all(class_='content_title')[0].text
    news_p = soup.find_all(class_='article_teaser_body')[0].text

    
    # JPL Mars Space Images - Featured Image
    marsimg_url = "https://spaceimages-mars.com/"
    browser.visit(marsimg_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find_all('img', class_='headerimage')[0]["src"]
    mars_image = marsimg_url + image
    
    # Obtain high resolution images and image title for each of Mars' hemispheres.
    mars_hemurl = 'https://marshemispheres.com/'
    browser.visit(mars_hemurl)

    html = browser.html
    soup = bs(html, 'html.parser')

    results_hemispheres = soup.find_all(class_='description')

    hemisphere_image_urls = []
    url_list = []
    for hem in results_hemispheres:
        hem_name = hem.find('h3').text
        hem_url = hem.find('a')['href']
        url_list.append(hem_url)

        hem_img_url = ['https://marshemispheres.com/' +
                       url for url in url_list]
        for link in hem_img_url:
            browser.visit(link)
            img_link = browser.find_link_by_text('Sample').first
            image_url = img_link['href']
            browser.back()
        hemisphere_image_urls.append({'title': hem_name, 'img_url': image_url})
    

    # Using Pandas to scrape tabular data from a page
    mars_factsurl = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(mars_factsurl)

    mars_df = tables[1]

    # Fixing column names
    cols = list(mars_df.columns)
    cols[0] = "Items"
    cols[1] = "Value"
    mars_df.columns = cols

    marshtml_table = mars_df.to_html()
    mars_table = marshtml_table.replace('\n', '')

    mars_info = {"news_title": news_title, "news_text": news_p, "featured_image": mars_image,
                 "mars_facts": mars_table, "mars_hemisphere": hemisphere_image_urls}
    browser.quit()
    
    return mars_info