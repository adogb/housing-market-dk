# Housing market in Denmark - dashboard

## What?
The project's goal is the creation of an interactive dashboard visualising the current housing market in Denmark. The scope is to create a dashboard updated daily, giving information on listings price evolution.

## Why?
The aim is to provide users with an overview of the market in a tailored way that common listings websites don't provide. An example of this is that average prices or other information are usually presented at commununal level. Copenhagen commune, as an example, is big (for Denmark) and prices vary a lot depending on neighbourhoods. Getting an average price per square meter for the Copenhagen commune is not useful for a prospective buyer - you could expect to pay 20.000 DKK (~$3200) more or less per square meter for neighbourhoods barely 5 km from one another.

## How?
The project has two main parts:
- web scraping of housing listings on boliga.dk, using Python and the BeautifulSoup library
- data visualisation and dashboard: the dashboard is available to see on [Tableau Public](https://public.tableau.com/app/profile/audrey.dogbeh/viz/HousingmarketinDenmark/HousingmarketinDenmarkapartments)

## Caveats
- As of February 2023, data is only related to apartments ("lejlighed" and "villalejlighed"). Boliga.dk does not use weighted area (defined by Finanstilsynet) when calculated the square meter price of a house, which makes it impossible to compare two houses together. I chose therefore not to include houses data in the dataset.
- Data is not representative of the full housing sales picture in Denmark. Since data is scraped from a housing sales website, it only includes properties that are made public. A lot of properties are indeed sold having never been made public.
- There can be small discrepancies in the date a property is put on sale or sold/removed from the website, which are dependant on how quickly the website publishes listings.

