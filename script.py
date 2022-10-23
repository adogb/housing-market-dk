import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import wrangling as w # project module
import pandas as pd
# import requests
# from bs4 import BeautifulSoup, Comment
# import re
# import datetime

dict_list = []
page_num = 1
pages_count = 1

while page_num <= pages_count:
  url= 'https://www.boliga.dk/resultat?zipCodes=2720&sort=daysForSale-d&page={num}'\
    .format(num=page_num)
  soup, retrieved = w.scrape_page(url)
  w.remove_comments(soup)
  tag_list=soup.find_all(w.is_relevant_listing)
  w.append_to_dictlist(tag_list, dict_list, retrieved)
  if page_num == 1:
    pages_count = int(soup.find("app-housing-list-results").find("app-pagination")\
                      .find("div", class_="nav-right").a.string)
  page_num+=1

df = w.create_dataframe(dict_list)

# read listings.csv in dataframe master
df_master = pd.read_csv("listings.csv")
df_master["date_added"] = df_master["date_added"].astype("datetime64[ns]")
df_master["retrieved"] = df_master["retrieved"].astype("datetime64[ns]")

# Treat new listings
# Treat existing listings
# Treat removed listings
