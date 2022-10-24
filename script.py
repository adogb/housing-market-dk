import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import wrangling as w # project module
import pandas as pd
# import requests
# from bs4 import BeautifulSoup, Comment
# import re
import datetime as dt
import shutil
import pathlib

# Archiving existing CSV file
modified_timestamp = pathlib.Path("listings.csv").stat().st_mtime
modified_date = dt.date.fromtimestamp(modified_timestamp)
archive_path = "csv_archive/" + modified_date.strftime(("%Y%m%d")) + "_listings.csv"
shutil.copy("listings.csv", archive_path)

# Extracting new data
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

# Read existing listings.csv in a dataframe
df_old = pd.read_csv("listings.csv", parse_dates=["date_added","retrieved"])

# Update still online listings' price reductions
df = df.set_index("id")
df_old = df_old.set_index("id")
df_old["price_diff%"].update(df["price_diff%"]) # update where index (id) match
df_old = df_old.reset_index()
df = df.reset_index()

# Treat removed listings
df_old.loc[~df_old["id"].isin(df["id"]),"status"] = "removed"

# Treat new listings
latest_retrieved_date = df_old["date_added"].max()
new_listings = df[df["date_added"]>latest_retrieved_date]
df_new = pd.concat([df_old, new_listings], ignore_index=True, copy=False)

# Write to CSV
df_new.to_csv("listings.csv", index=False)