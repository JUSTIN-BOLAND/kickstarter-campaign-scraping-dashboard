#!/usr/bin/env python
# coding: utf-8

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup as bs
import requests
from lxml import html
import re
import datetime
import pytz

## Google Apps Api
# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/jeremie/environment_directory/slicecharge/client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("kickstarter").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()


## Scrape Kickstarter
url = 'https://www.kickstarter.com/projects/2127998328/slicecharge-pro-worlds-1st-6-coils-wireless-chargi'
r = requests.get(url).content
soup = bs(r,'lxml')

pledge = soup.find("span", {"class": "ksr-green-700"}).get_text()
pledge = pledge.split()[1]
pledge = pledge.replace(",", "")

goal = soup.find("span", {"class": "money"}).get_text()
goal = goal.split()[1]
goal = goal.replace(",", "")

currency = soup.find("span", {"class": "ksr-green-700"}).get_text()
currency = currency.split()[0]

backers = soup.find("div", {"class": "block type-16 type-24-md medium soft-black"}).get_text()
backers = backers.replace(",","")

days = soup.find("span", {"class": "block type-16 type-24-md medium soft-black"}).get_text()

# Select Hong Kong time-zone
tz = pytz.timezone('Asia/Hong_Kong')
ct = datetime.datetime.now(tz=tz)

# Export the values to google sheets
row = [str(ct.isoformat()),str(ct.strftime('%Y/%m/%d %H:%M:%S')),str(ct.strftime('%Y/%m/%d-%H:%M:%S')),str(url),int(pledge),int(goal),str(currency),int(backers),int(days)]
index = int(sheet.row_count)
sheet.insert_row(row, index)
