# To update a CSV file that has not been updated for a while for example
# and where the date_removed is thus wrong by a number of days. Run script.py first to retrieve all newest listings. This uses the archive
# so only valid for listings that have been removed. To update all the other listings, use
# script.py.

import wrangling as w # project module
import datetime as dt
import pandas as pd

dict_list = []
page_num = 1
date_update_from = dt.date(2023, 5, 20) # INPUT DESIRED DATE, corresponds to "last seen" date on Boliga
page_last_removal_date = dt.date.today()

while page_last_removal_date >= date_update_from:
  url= 'https://www.boliga.dk/resultat?propertyType=3,9&hideForclosure=true&'\
    'searchArchive=true&pubdateMin=2020-01-01&sort=lastchange-d&page={num}'\
    .format(num=page_num)
  soup, retrieved = w.scrape_page(url)
  w.remove_comments(soup)
  tag_list=soup.find("app-housing-list-results").find_all(w.is_relevant_listing)
  w.append_to_dictlist(tag_list, dict_list, retrieved, "removed")

  page_last_removal_datestring = dict_list[-1]["date_removed"].strip()\
    .replace("Ikke længere til salg - sidst set ", "")
  page_last_removal_date = dt.datetime.strptime(page_last_removal_datestring, "%d-%m-%Y").date()
  page_num+=1

df_archive = w.create_dataframe(dict_list)
df_archive.set_index("id", inplace=True)

df = pd.read_csv("listings.csv", index_col="id", parse_dates=["date_added",\
  "retrieved", "date_removed", "year_built"])

df["date_removed"].update(df_archive["date_removed"])
df["status"].update(df_archive["status"])
df["price_diff%"].update(df_archive["price_diff%"])
df["price"].update(df_archive["price"])
df["price_per_m2"].update(df_archive["price_per_m2"])
df["days_on_sale"].update(df_archive["days_on_sale"])

df.to_csv("listings.csv")
