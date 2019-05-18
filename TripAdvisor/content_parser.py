# -*- coding: utf-8 -*-
import pandas as pd
import csv
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re

domain = 'https://www.tripadvisor.com'
df = pd.read_csv('./data/url_parser.csv')
total_hotels = len(df)
debug = False
if debug:
    limit = 3
else:
    limit = None

with open('./data/content_parser.csv', 'a') as csvfile:
    fieldnames = [
                    'hotel_id', 'address', 'rank', 'phone',
                    'n_Excellent', 'n_VeryGood', 'n_Average', 'n_Poor', 'n_Terrible', 'amenities','hotel_class'
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for index, u in enumerate(df['url'][:limit]):
        hotel_id = df['hotel_id'][index]
        print("Crawling hotel page [{}]/[{}]".format(index+1,total_hotels), end='\r', flush=True)
        r = requests.get(u)
        soup = BeautifulSoup(r.text, 'html.parser')
        # info_block
        info_block = soup.find('div', {'id':"atf_header"})
        
        try:
            street = info_block.find('span', {'class':"street-address"}).text
        except AttributeError:
            street = None

        try:
            extended = info_block.find('span', {'class':"extended-address"}).text
        except AttributeError:
            extended = None

        try:
            locality = info_block.find('span', {'class':"locality"}).text
        except AttributeError:
            locality = None

        try:
            country = info_block.find('span', {'class':"country-name"}).text
        except AttributeError:
            country = None

        address = str(street) + ', ' + str(extended) + ', ' + str(locality) + str(country)

        try:
            phone = info_block.find('span', {'class':"detail ui_link level_4 is-hidden-mobile"}).text
        except AttributeError:
            phone = None

        try:
            rank = info_block.find('b', {'class':"rank"}).text
        except AttributeError:
            rank = None

        rating_chart = soup.find('div', {'class':"ui_column is-5 is-12-mobile"})
        rating_dict = {'Excellent':None,'VeryGood':None,'Average':None,'Poor':None,'Terrible':None}
        for i, col in enumerate(rating_dict):
            try:
                tmp = rating_chart.find_all('span', {'class':"hotels-review-list-parts-ReviewRatingFilter__row_num--gIW_f"})[i].text
                tmp = int(re.sub('[^0-9,]', "", tmp).replace(',',''))
                rating_dict[col] = tmp
            except:
                rating_dict[col] = None

        amenities = " | ".join([a.text for a in soup.find_all('span', {'class': "hotels-hotel-review-about-with-photos-Amenity__name--2IUMR"})])
        hotel_class = str(soup.find_all('div', {'class': "hotels-hotel-review-about-with-photos-layout-TextItem__textitem--3kv6J"})[-1:])[118:120]    
        writer.writerow(
                         {
                            'hotel_id':hotel_id,
                            'address':address,
                            'rank':rank,#.encode('utf-8'),
                            'phone':phone,
                            'n_Excellent':rating_dict["Excellent"], 
                            'n_VeryGood':rating_dict["VeryGood"], 
                            'n_Average':rating_dict["Average"],
                            'n_Poor':rating_dict["Poor"],
                            'n_Terrible':rating_dict["Terrible"],
                            'amenities':amenities,
                            'hotel_class':hotel_class
                         }
                        )
        csvfile.flush()
    print("")