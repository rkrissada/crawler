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
target_url = 'https://www.tripadvisor.com/Hotel_Review-g293916-d3183208-Reviews-Klassique_Sukhumvit-Bangkok.html' 
driver = webdriver.Chrome('/usr/local/bin/chromedriver/', chrome_options=options)
driver.get(target_url)
driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'html.parser')
domain = 'https://www.tripadvisor.com'

# scrape page
next_page = '//*[@id="taplc_hr_community_content_0"]/div/div/div/span/a'
check_last_page = soup.find('div',{'class' : "pageNumbers"}).find_all("a")[-1].get_text()
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
page_list =  range(int(check_last_page))
print("Total number of page: {}".format(len(page_list)))



with open('./data/review_parser.csv', 'a') as csvfile:
    fieldnames = ['user', 'stay_date', 'rate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    

    for p in page_list:
        print('the number of page = {0}/{1}'.format(p+1, len(page_list)))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_blocks = soup.find_all('div', {"class": "hotels-review-list-parts-SingleReview__reviewContainer--d54T4"})
        
        index = 0

        for element in review_blocks:
            index += 1
            
            user = element.find('a', {"class": "ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC"}).text
            
            stay_date_group = element.find('div', {"class": "hotels-review-list-parts-EventDate__event_date--CRXs4"})
            stay_date = stay_date_group.find('span', {"class": ""}).text.replace("Date of stay: ","")
            
            rate = element.find('div', {"class": "hotels-review-list-parts-RatingLine__bubbles--1oCI4"})
            rate = str(rate.find('span'))[37:-9]
            
            writer.writerow(
                            {
                                'user':user,
                                'stay_date':stay_date,
                                'rate':rate
                            }
                           )

        try:
            driver.execute_script(page_down)
            time.sleep(5)
            driver.find_element_by_css_selector(".ui_button.nav.next.primary").click()
            time.sleep(8)
        except:
            print('>>>>>>>in the end<<<<<<<')
            break

driver.quit()