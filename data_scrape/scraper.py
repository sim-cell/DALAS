from urllib import request
import requests
from bs4 import BeautifulSoup
import re
import json
import bs4
import lxml
import pandas as pd
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

def scrape_items(main_url,max_page):
    links = []
    req = requests.get(main_url,headers=headers)
    page = bs4.BeautifulSoup(req.content, "lxml")

    items = page.find_all('li')
    for item in items:
        link = item.find('a', class_='db7c79')
        if link:
            href = link.get('href')
            links.append(href)

    for nb in range(2,max_page+1):
        print(nb)
        url = main_url+'?page='+str(nb)
        req = requests.get(url,headers=headers)
        page = bs4.BeautifulSoup(req.content, "lxml")

        items = page.find_all('li') #,class_='product-item'
        for item in items:
            link = item.find('a', class_='db7c79')
            if link:
                href = link.get('href')
                links.append(href)
    return links

def scrape_details(links):
    material_lists = []
    names = []
    prices = []
    i = 0
    for link in links:
        if i%100 == 0:
            print(i)
        i+=1
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        if not soup:
            names.append('NA')
            prices.append('NA')
            material_lists.append('NA')
            continue
        #name
        name = soup.find('h1')
        if not name:
            names.append('NA')
            prices.append('NA')
            material_lists.append('NA')
            continue
        nameTEXT = name.text
        
        #price
        price_div = soup.find('div', class_='price parbase')
        if not price_div:
            names.append('NA')
            prices.append('NA')
            material_lists.append('NA')
            continue
        price_span = price_div.find('span')
        price_value = price_span.text.strip()
        
        # materials
        h3 = soup.find(lambda tag: tag.name == 'h3' and "Explications relatives " in tag.text) #  
        parent_tag = h3.find_next_sibling()

        # its under dt 
        dt_tags = parent_tag.find_all('dt')
        materials = []

        
        # get the text from the dt tags
        for dt in dt_tags:
            materials.append(dt.text)

        names.append(nameTEXT)
        prices.append(price_value)
        material_lists.append(materials)
    return names, prices, material_lists

def run_selenium(unique_links):

    # Initialize a WebDriver (assuming you have chromedriver installed)
    driver = webdriver.Chrome()
    informations = []
    # Navigate to the webpage
    #url = 'https://www2.hm.com/fr_fr/productpage.1149098003.html'
    for url in unique_links:
        driver.get(url)
        try:
            materials_button =  WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID,"toggle-materialsAndSuppliersAccordion")))
            materials_button.click()
            #popup_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Informations sur le fournisseur')]")))
            popup_button = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.CLASS_NAME, "bbcd86")))
            popup_button.click()

            popup_elements = WebDriverWait(driver, 4).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "dd5fe7")))
            popup_contents = [element.text.strip() for element in popup_elements]
        except:
            popup_contents = []
            informations.append(popup_contents)
            continue
        informations.append(popup_contents)
    # Close the browser window
    driver.quit()
    return informations

main_url = 'https://www2.hm.com/fr_fr/femme/catalogue-par-produit/sweatshirts.html'
max_page = 5
links = scrape_items(main_url,max_page)

unique_links = list(set(links))
print((len(unique_links),len(links)))

names,prices,material_lists = scrape_details(unique_links)
informations = run_selenium(unique_links)

fixed_material_lists = [[s.encode('utf-8').decode('unicode_escape') for s in sublist] for sublist in material_lists]

print(fixed_material_lists)
import pandas as pd
print(len(names), len(prices), len(fixed_material_lists), len(unique_links))
data = {
    'Product Type': ['Sweatshirt']*len(names),
    'Product Name': names,
    'Price': prices,
    'Material': fixed_material_lists,
    'Link': unique_links[:len(names)],
    'Informations': informations[:len(names)]
}

# Create the dataframe
df = pd.DataFrame(data)

# Print the dataframe
df.to_csv('hmSWEATSHIRTS.csv', index=False)