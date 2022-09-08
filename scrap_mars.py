from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo



# intiate path
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()    
    marsdct = {}

    # Nasa News
    time.sleep(1)
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup=bs(html, 'html.parser')    

    results = soup.find('div', class_='list_text')
    
    #pull titles
    title = results.find('div', class_='content_title').text
    
    #pull articles
    article = results.find('div', class_='article_teaser_body').text


    # Image
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    image_html = browser.html
    image_soup=bs(image_html, 'html.parser')
    path = image_soup.find_all('img')[1]['src']
    final_image= image_url + path


    # Facts
    table_url = "https://galaxyfacts-mars.com/"
    browser.visit(table_url)
    table = pd.read_html(table_url)
    df=table[0]
    X=df.rename(columns={
    0: 'Mars-Earth Comparison',
    1: 'Mars',
    2: 'Earth'
    })
    Y=X.drop([0])
    Z=Y.set_index('Mars-Earth Comparison')

    html_table=Z.to_html()
    final_table = html_table.replace('/n','')


    # Hemispheres
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup=bs(hemispheres_html, 'html.parser')
    Hemisresults = hemispheres_soup.find_all('div', class_='item')

    hemisphereimage = []

    for h in Hemisresults:
        
        try:
            # Extract title
            hem=h.find('div',class_='description')
            X=hem.h3.text
            #finds image url
            pic = hem.a['href']
    
            #opens the image url
            browser.visit(hemispheres_url + pic)
            hemis_html = browser.html
            hemis_soup = bs(hemis_html, 'html.parser')
            hemis_link = hemis_soup.find('div', class_='downloads')
            hemis_url = hemis_link.find('li').a['href']
        
            #create Dictionary
            hemisdct = {}
            hemisdct['title'] = X
            hemisdct['hemis_url'] = hemispheres_url + hemis_url
            hemisphereimage.append(hemisdct)

        except Exception as e:
            print(e)
    

    #final dictionary
    marsdct = {"Title": title, "Article": article,"Final_Image": final_image, 
    "Comparison_Table": final_table, "Hemispheres": hemisphereimage}

    browser.quit()

    return marsdct
