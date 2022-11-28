import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import datetime
import re

def scrape_page(url):
  r = requests.get(url)
  time_retrieved = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
  return BeautifulSoup(r.content, "lxml"), time_retrieved

def remove_comments(soup):
  comments = soup.find_all(string=lambda x: isinstance(x, Comment))
  for comment in comments:
    comment.extract()

def is_relevant_listing(tag): 
  # find names of tag parents by mapping
  if tag.name == "app-housing-list-item":
    parentsNames = list(map((lambda x: x.name), tag.parents))
    is_not_public = tag.find("app-listing-information-hidden")

    return not ("ngb-carousel" in parentsNames) and not ("swiper" in parentsNames) \
      and not is_not_public
  else:
    return False

def append_to_dictlist(tag_list, dict_list, time_retrieved, status):
  for tag in tag_list:     
    # structuring for code readability
    top_info = tag.find("app-listing-information-lg").div.div
    middle_info = tag.find("app-listing-information-lg").find("app-property-label").parent
    bottom_info = tag.find(class_="house-details-blocks")
    
    link = tag.a['href']
    address=top_info.div.div.span.string
    city=address.parent.next_sibling.string
    price=top_info.div.next_sibling.div.contents[1]
    price_per_m2=price.parent.next_sibling.string
    price_diff_tag=top_info.div.next_sibling.div.find("span", class_="badge")
    price_diff = price_diff_tag.string if price_diff_tag else "0"
    housing_type = middle_info.find("app-property-label").find("span", class_="text").string
    date_added = middle_info.p.string
    rooms = bottom_info.contents[0].span.string
    area = bottom_info.contents[1].span.string
    energy_label = bottom_info.contents[2].span.string
    year_built = bottom_info.contents[3].span.string
    ground_area = bottom_info.contents[4].span.string
    monthly_cost = bottom_info.contents[5].span.string
    date_removed = tag.find("app-listing-information-lg").find("span", class_="badge-warning").string if status == "removed" else ""
    
    # appending data dictionnary to dict_list. BeautifulSoup converts HTML non-breaking spaces (&nbsp) to \xa0 (unicode), so we need to remove them.
    dict_list.append({
        "link": link,
        "address": str(address).replace(u'\xa0', u' '),
        "city": city,
        "housing_type": housing_type,
        "price": str(price).replace(u'\xa0', u' '),
        "price_per_m2": str(price_per_m2).replace(u'\xa0', u' '),
        "price_diff%": price_diff,
        "area": area,
        "rooms": rooms,
        "ground_area": ground_area,
        "energy_label": energy_label,
        "year_built": year_built,
        "monthly_cost": monthly_cost,
        "date_added": date_added,
        "retrieved": time_retrieved,
        "date_removed": date_removed,
        "status": status
    })

def create_dataframe(dict_list):
  df = pd.DataFrame(dict_list)

  df.id = df.link.str.split("/").str[2]

  df = df.apply(lambda col: col.str.strip())

  df.address = df.address.str.rstrip(",")
  df.energy_label = df.energy_label.str.replace("Energimærke: ", "")

  df.price = df.price.str.replace(" kr\.","").str.replace("\.","")
  df.price_per_m2 = df.price_per_m2.str.replace(" kr\. \/ m²","")\
                                    .str.replace("\.","")
  df["price_diff%"] = df["price_diff%"].str.replace("%","")
  df.area = df.area.str.replace(" m²","")
  df.monthly_cost = df.monthly_cost.str.replace(" kr\. \/ md\.","")\
                                  .str.replace("Ejerudgift: ","")\
                                  .str.replace("Boligydelse: ","")\
                                  .str.replace("\.","")
  df.rooms = df.rooms.str.replace("Værelser: ","").str.replace(" værelse","")
  df.ground_area = df.ground_area.str.replace(" m²","").str.replace("\.","")

  numeric_columns = ["id", "price","price_per_m2", "area","rooms",
  "ground_area", "monthly_cost"]
  df[numeric_columns] = df[numeric_columns]\
    .apply(lambda col: pd.to_numeric(col, errors="coerce").astype(int)) 
    # to replace the non-numbers/missing info with NaN
  df["price_diff%"] = pd.to_numeric(df["price_diff%"], errors="coerce").fillna(0).astype(int)
  df["price_diff%"] = df["price_diff%"]/100
  # to replace the non-numbers/missing info with 0

  def convert_to_date_string(str):
    arr = str.replace("Oprettet ","").replace(".","").split(" ")
    if (len(arr[0])==1): 
      arr[0] = "0" + arr[0] # adding a 0 to numbers from 1 to 9
    
    months_conversion = {"jan": "01", "feb": "02", "mar": "03", "apr": "04",
      "maj": "05", "jun": "06", "jul": "07", "aug": "08", "sep":"09", "okt": "10",
      "nov": "11", "dec": "12"}
    date = arr[2]+ "-" + months_conversion[arr[1]] + "-" + arr[0]
    return date

  df.date_added = df.date_added.apply(convert_to_date_string)
  df.date_added = df.date_added.astype("datetime64[ns]")

  df.retrieved = df.retrieved.astype("datetime64[ns]")

  df.date_removed = df.date_removed\
    .str.replace("Ikke længere til salg - sidst set ", "")
  df.date_removed = pd.to_datetime(df.date_removed, format="%d-%m-%Y", errors="coerce")

  df.loc[df.status=="online", "days_on_sale"] = (df.retrieved-df.date_added).dt.days
  df.loc[df.status=="removed", "days_on_sale"] = (df.date_removed-df.date_added).dt.days

  df.year_built = pd.to_datetime(df.year_built, format="%Y", errors="coerce")

  df = df[["id", "address", "city", "housing_type", "price", "price_per_m2", "price_diff%",\
    "area", "ground_area", "rooms", "year_built", "energy_label", "monthly_cost",\
    "date_added", "date_removed", "days_on_sale", "status", "retrieved", "link"]]

  return df