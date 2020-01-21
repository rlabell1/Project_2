import numpy as np

import requests
import json
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import flask
from flask import request, jsonify
import bs4
import urllib.parse
from splinter import Browser

from flask import Flask, jsonify

#################################################
# Web Scraping for Georgia Income Data
#################################################
executable_path={'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit('http://datausa.io/api/data?Geography=04000US13:children&measure=Household Income by Race,Household Income by Race Moe&drilldowns=Race')

GA_Income_Data = json.loads((browser.find_by_tag('body').first.text))
browser.quit()

#################################################
# EV Station Data API - Acquisiton
#################################################
url ='https://developer.nrel.gov/api/alt-fuel-stations/v1.json?fuel_type=ELEC,ELEC&state=GA&limit=all&api_key=FHhxl7HnTsc9tm4X9CwUBVDNmbQFFu4uZXKJeO59&format=JSON'
response = requests.get(url).json()
#print((json.dumps(response, indent = 4, sort_keys =True)))
response_string=(json.dumps(response ['fuel_stations'], indent = 4, sort_keys =True))
#############################
#creationg dataframe from ev response
ev_df = pd.read_json(response_string)
##########################
#selecting relevent data
ev_df.head()
ev_data = ev_df[["access_code", "city","facility_type", "latitude", "longitude", "street_address", "zip", "owner_type_code", "ev_pricing"]]
ev_data.head()

#################################################
# Database Setup
#################################################
#connecting to Mongo db
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
#############################
# loading to GA Income Data Mongodb
db = client.ev_data
collection = db.Income
collection.insert_one(GA_Income_Data)

# loading EV Station Data to Mongodb
db = client.ev_data
collection = db.Stations
collection.insert_many(ev_data.to_dict('records'))