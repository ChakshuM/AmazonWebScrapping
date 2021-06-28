# '''
# To work on this project you needed to install 3 important libraries
# pip install beautifulsoup4
# pip install selenium
# pip install msedge-selenium-tools
# '''

import csv
from bs4 import BeautifulSoup
import pandas as pd



#firefox and chrome
from selenium import webdriver
chrome_path = r"C:\Users\chakshu\PycharmProjects\WebScrapping\chromedriver.exe"
# from msedge.selenium_tools import Edge, EdgeOptions
# from webdriver_manager.chrome import ChromeDriverManager




def get_url(search_term):
    """Generate a URL from search term"""
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ','+')

    # add term query to URL
    url = template.format(search_term)

    # add page query placeholder
    url += '&page{}'

    return url


def extract_record(item):
    """Extract and return data from a single record"""

    #a description and URL
    atag = item.h2.a
    description = atag.text.strip()
    url = 'http://www.amazon.com' + atag.get('href')

    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except  AttributeError:
        return

    try:
        # Rank and Rating
        rating = item.i.text
        review_count = item.find('span',{'class':'a-size-base'}).text
    except AttributeError:
        rating = ""
        review_count = ""

    result = (description, price, rating, review_count, url)

    return result


def main(search_term):
    """Run main program routine"""
    # startup the webdriver
    driver = webdriver.Chrome(chrome_path)

    records = []
    url = get_url(search_term)

    for page in range(1, 2):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results  = soup.find_all('div', {'data-component-type':'s-search-result'})

        for item in results:
            record  = extract_record(item)
            if record:
                records.append(record)
    driver.close()


    # Save data to Csv file
    with open(r'results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','Url'])
        for i in records:
            writer.writerow(i)




main('ultrawide monitor')
#main('shoes')
