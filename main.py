from operator import is_
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime

# GATHERING DATA

url = 'https://www.boliga.dk/resultat?zipCodes=2720'
r = requests.get(url)
content = r.content
soup = BeautifulSoup(content, "lxml")

def is_relevant_listing(tag):
  # find names of tag parents by mapping
  parentsNames = list(map((lambda x: x.name), tag.parents))
  return tag.name == "app-housing-list-item" and not "ngb-carousel" in parentsNames
#tag_list=soup.find("app-housing-list-results").div.div.next_sibling.find_all("app-housing-list-item")
tag_list=soup.find_all(is_relevant_listing)
print(tag.a for tag in tag_list)

# Fetch current HTML content from website (day 1) using Requests module
# Extract (scrape) relevant data from each listing with BeautifulSoup and put in a dataframe
# Clean the data
# Create a database MySQL / or CSV file?
# Each day
#   Fetch new offers on the website
#   Extract relevant data from each listing and put in database
#   Categorise all housing to sold/for sale
#     Compare list to sold housing page? Or Look for listings that are not there
#     anymore?

