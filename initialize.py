import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import wrangling as w # project module

# GATHERING DATA
dict_list = []
page_num = 1
pages_count = 1

# Collecting appartments previously on sale since January 2020
while page_num <= pages_count:
  url= 'https://www.boliga.dk/resultat?propertyType=3,9&hideForclosure=true&'\
    'searchArchive=true&pubdateMin=2020-01-01&page={num}'\
    .format(num=page_num)
  soup, retrieved = w.scrape_page(url)
  w.remove_comments(soup)
  tag_list=soup.find("app-housing-list-results").find_all(w.is_relevant_listing)
  w.append_to_dictlist(tag_list, dict_list, retrieved, "removed")
  if page_num == 1:
    pages_count = int(soup.find("app-housing-list-results").find("app-pagination")\
                      .find("div", class_="nav-right").a.string)
  #print(page_num, " done")
  page_num+=1

page_num = 1
pages_count = 1


# Collecting appartments currently on sale
while page_num <= pages_count:
  url= 'https://www.boliga.dk/resultat?propertyType=3,9&hideForclosure=true&page={num}'\
    .format(num=page_num)
  soup, retrieved = w.scrape_page(url)
  w.remove_comments(soup)
  tag_list=soup.find("app-housing-list-results").find_all(w.is_relevant_listing)
  w.append_to_dictlist(tag_list, dict_list, retrieved, "online")
  if page_num == 1:
    pages_count = int(soup.find("app-housing-list-results").find("app-pagination")\
                      .find("div", class_="nav-right").a.string)
  #print(page_num, " done")
  page_num+=1

# CLEANING DATA AND CREATING DATAFRAME
df = w.create_dataframe(dict_list)
df.set_index("id", inplace=True)
df.sort_index(inplace=True)

# CREATING CSV FILE
df.to_csv("listings.csv")