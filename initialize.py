import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import wrangling as w # project module
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup, Comment
# import re
# import datetime

# GATHERING DATA
dict_list = []
page_num = 1
pages_count = 1

while page_num <= pages_count:
  url= 'https://www.boliga.dk/resultat?zipCodes=2720&sort=daysForSale-a&page={num}'\
    .format(num=page_num)
  soup, retrieved = w.scrape_page(url)
  w.remove_comments(soup)
  tag_list=soup.find_all(w.is_relevant_listing)
  w.append_to_dictlist(tag_list, dict_list, retrieved)
  if page_num == 1:
    pages_count = int(soup.find("app-housing-list-results").find("app-pagination")\
                      .find("div", class_="nav-right").a.string)
  page_num+=1

# CLEANING DATA AND CREATING DATAFRAME
df = w.create_dataframe(dict_list)

# CREATING CSV FILE
df.to_csv("listings.csv", index=False)