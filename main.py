# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import re
import datetime

# %% GATHERING DATA
## Fetch current HTML content from website (day 1) using Requests module
url = 'https://www.boliga.dk/resultat?zipCodes=2720'
r = requests.get(url)
content = r.content
soup = BeautifulSoup(content, "lxml")

## Creating timestamp
now = datetime.datetime.now()
retrieved = now.strftime(("%Y-%m-%d %H:%M:%S"))

# %% Remove comments
comments = soup.find_all(string=lambda x: isinstance(x, Comment))
for comment in comments:
  comment.extract()

# %% Extract (scrape) relevant data from each listing with BeautifulSoup
def is_relevant_listing(tag): 
  # find names of tag parents by mapping
  parentsNames = list(map((lambda x: x.name), tag.parents))
  is_not_public = tag.find("app-listing-information-hidden")

  return (tag.name == "app-housing-list-item") and not ("ngb-carousel" in parentsNames) and not ("swiper" in parentsNames) and not is_not_public

tag_list=soup.find_all(is_relevant_listing)

# %% Making list of dictionaries to name data, and to later make a dataframe
data_list = []
for tag in tag_list:     
  # structuring for code readability
  top_info = tag.find("app-listing-information-lg").div.div
  middle_info = top_info.next_sibling.next_sibling.div.div
  bottom_info = tag.find(class_="house-details-blocks")
  
  link = tag.a['href']
  address=top_info.div.div.span.string
  #print(address)
  city=address.parent.next_sibling.string
  #print(city)
  price=top_info.div.next_sibling.div.contents[1]
  #print(price)
  price_per_m2=price.parent.next_sibling.string
  #print(price_m2)
  housing_type = middle_info.find("app-property-label").find("span", class_="text").string
  date_added = middle_info.p.string
  rooms = bottom_info.contents[0].span.string
  area = bottom_info.contents[1].span.string
  energy_label = bottom_info.contents[2].span.string
  year_built = bottom_info.contents[3].span.string
  ground_area = bottom_info.contents[4].span.string
  monthly_cost = bottom_info.contents[5].span.string
  
  # appending data dictionnary to data_list. BeautifulSoup converts HTML non-breaking spaces (&nbsp) to \xa0 (unicode),
  # so we need to remove them.
  data_list.append({
      "link": link,
      "address": str(address).replace(u'\xa0', u' '),
      "city": city,
      "housing_type": housing_type,
      "price": str(price).replace(u'\xa0', u' '),
      "price_per_m2": str(price_per_m2).replace(u'\xa0', u' '),
      "area": area,
      "rooms": rooms,
      "ground_area": ground_area,
      "energy_label": energy_label,
      "year_built": year_built,
      "monthly_cost": monthly_cost,
      "date_added": date_added,
      "retrieved": retrieved
  })

# %% CLEANING DATA
df_original = pd.DataFrame(data_list)
df = df_original.copy()

# %%
df["id"] = df["link"].str.split("/").str[2]

# %% remove comma and space at the end of address values
df.address = df.address.str.rstrip(", ")

# %% extract numbers from strings for relevant columns
df.price = df.price.str.strip().str.rstrip(" kr.").str.replace(".","").astype(int)

df.price_per_m2 = df.price_per_m2.str.strip().str.rstrip(" kr. / m²").str.replace(".","").astype(int)

df.area = df.area.str.strip().str.rstrip(" m²").astype(int)

df.monthly_cost = df.monthly_cost.str.strip().str.rstrip(" kr. / md.")\
                                .str.lstrip("Ejerudgift: ").str.replace(".","").astype(int)

df.rooms = df.rooms.str.strip().str.lstrip("Værelser: ").str.rstrip(" værelse").astype("int")

df.ground_area = df.ground_area.str.strip().str.rstrip(" m²").str.replace(".","").astype(int)


# %%
# print(df.ground_area)
# Create a database MySQL / or CSV file?
# Each day
#   Fetch new offers on the website
#   Extract relevant data from each listing and put in database
#   Categorise all housing to sold/for sale
#     Compare list to sold housing page? Or Look for listings that are not there
#     anymore?
# %%
