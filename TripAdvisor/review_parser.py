# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv
import re


domain = 'https://www.tripadvisor.com'
df = pd.read_csv('./data/url_parser.csv')
total_hotels = len(df)
debug = False
if debug:
    limit = 3
else:
    limit = None

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver/', chrome_options=options)

#next_page = '//*[@id="taplc_hr_community_content_0"]/div/div/div/span/a'
#page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"

with open('./data/review_parser.csv', 'a') as csvfile:
    fieldnames = ['hotel_id', 'user', 'home_town', 'stay_date', 'rate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for index, u in enumerate(df['url'][:limit]):
        hotel_id = df['hotel_id'][index]
        print('process = {}/{}'.format(index+1, total_hotels))
        driver.get(u)
        driver.maximize_window()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # scrape page
        check_last_page = soup.find('div',{'class' : "pageNumbers"}).find_all("a")[-1].get_text()
        page_list =  range(int(check_last_page))
        page_list_tot = len(page_list)
        print("Total number of page: {}".format(page_list_tot))        

        for p in page_list[:limit]:
            print("Crawling review page [{}]/[{}]".format(p+1,page_list_tot), end='\r', flush=True)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_blocks = soup.find_all('div', {"class": "hotels-review-list-parts-SingleReview__reviewContainer--d54T4"})
            
            index = 0

            for element in review_blocks:
                index += 1
                
                user = element.find('a', {"class": "ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC"}).text

                try:
                    home_town = element.find('span', {"class": "default social-member-common-MemberHometown__hometown--3kM9S small"}).text
                except:
                    home_town = ""
                
                stay_date_group = element.find('div', {"class": "hotels-review-list-parts-EventDate__event_date--CRXs4"})
                stay_date = stay_date_group.find('span', {"class": ""}).text.replace("Date of stay: ","")
                
                rate = element.find('div', {"class": "hotels-review-list-parts-RatingLine__bubbles--1oCI4"})
                rate = int(str(rate.find('span'))[37:-9])/10

                writer.writerow(
                                {
                                    'hotel_id':hotel_id,
                                    'user':user,
                                    'home_town':home_town,
                                    'stay_date':stay_date,
                                    'rate':rate
                                }
                            )
                csvfile.flush()
                
            try:
                #driver.execute_script(page_down)
                #time.sleep(5)
                driver.find_element_by_css_selector(".ui_button.nav.next.primary").click()
                time.sleep(10)
            except:
                print('>>>>>>>in the end<<<<<<<')
                break


driver.quit()