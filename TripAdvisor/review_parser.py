# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv
import re

options = webdriver.ChromeOptions()
options.add_argument('headless')
#target_url = 'https://www.tripadvisor.com.tw/Hotels-g294225-Indonesia-Hotels.html'
target_url = 'https://www.tripadvisor.com/Hotel_Review-g293916-d3183208-Reviews-Klassique_Sukhumvit-Bangkok.html' 
#target_url = 'https://www.tripadvisor.com/Hotels-g293916-Bangkok-Hotels.html'
driver = webdriver.Chrome('/usr/local/bin/chromedriver/', chrome_options=options)
driver.get(target_url)
driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'html.parser')
domain = 'https://www.tripadvisor.com'

# scrape page
next_page = '//a[@class="ui_button nav next primary "]'
check_last_page = soup.find('div',{'class' : "pageNumbers"}).find_all("a")[-1].get_text()
#print(check_last_page)
#print(pages_list.find_all("a")[-1].get_text())
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
page_list =  range(int(check_last_page))
print("Total number of page: {}".format(len(page_list)))



with open('./data/review_parser.csv', 'a') as csvfile:
    fieldnames = ['hotel_id', 'hotel_name', 'n_comment', 'rank_in_country', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    index = 0

    for p in page_list:
        print('the number of page = {0}/{1}'.format(p+1, len(page_list)))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_blocks = soup.find_all('div', {"class": "hotels-community-tab-common-Card__ui_card--mBW-w hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"})
        #print(len(review_blocks))
        
        for element in review_blocks:
            #print(element)
            index += 1
            try:
                user = element.find('a', {"class": "ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC"}).text
            except:
                user = None
            print(user)
            """
            writer.writerow(
                            {
                                'hotel_id':index,
                                'hotel_name':hotel_name.encode("utf-8"),
                                'n_comment':n_comment,
                                'rank_in_country':rank_in_country.encode("utf-8"),
                                'url':url
                            }
                           )
            """
        try:
            driver.execute_script(page_down)
            time.sleep(5)
            #driver.find_element_by_xpath(next_page).click()
            try:
                next = driver.find_element_by_class_name('ui_button nav next primary')#.click()
            except:
                print("not found")
            #driver.execute_script('next = document.querySelector(".ui_button nav next primary "); next.click();')
           
        except:
            print('in the end')


driver.quit()