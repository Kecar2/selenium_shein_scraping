#!/usr/bin/env python
# coding: utf-8

# In[49]:


import selenium
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# In[50]:


# Generating url for product

def get_url(product):
    product = product.replace(' ','%20')
    template = 'https://es.shein.com/pdsearch/{}'
    url = template.format(product)
    return url


# In[52]:


# Create a function which will fetch the product information

def get_all_products(card):
    pImg = card.find('img','falcon-lazyload')
    try:
        product_image = pImg['src']
    except TypeError:
        product_image = ''
    product_name = card.find('div','S-product-item__name').text.strip()
    product_price = card.find('div','S-product-item__price').text.strip()
    anchor_tag = card.a.get('href')
    product_buy_link = 'https://es.shein.com'+anchor_tag
    
    product_info = (product_image , product_name , product_price , product_buy_link)
    
    return product_info

def main(product):
    records = []
    url = get_url(product)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    product_cards = soup.find_all('section', 'S-product-item')
    
    
    for everyProduct in product_cards:
        productDetails = get_all_products(everyProduct)
        records.append(productDetails)
        
# Here We Are Using Pandas Data Frame To Save Products Information In A CSV File

    col = ['Product_Image','Product_Name','Product_Price','Product_Buy_Link']
    
    shein_data = pd.DataFrame(records, columns=col)
    
    shein_data.to_csv('C:\\Users\\kendr\\OneDrive\\Escritorio\\ProyectosPython\\SheinData.csv')
    


# In[53]:


product = input('Enter Product You Are Looking For : ')
main(product)

