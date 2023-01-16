import wrangling as w # project module
import datetime as dt
import pandas as pd

dict_list = []
page_num = 1
date_update_from = dt.date(2023, 1, 10) # INPUT DESIRED DATE
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


