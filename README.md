# Housing market in Denmark - dashboard

▶ See [live dashboard](https://public.tableau.com/app/profile/audrey.dogbeh/viz/Apartmentsm2-priceinDenmarkaggregatedbypostalcode/HousingmarketinDenmarkapartments) on Tableau Public. No account required.

## What?
I created a Tableau dashboard showing the state of real estate property sales in Denmark since January 2020. The dashboard makes it possible to dig into data at postal code level.

## Why?
The aim of this visualisation is to provide users with an overview of the market in a granular way that common listings websites don't provide (at the time I started the project at least).

I was looking to buy an apartment in 2020 and trying to get an overview of square meter prices by neighbourhood in Copenhagen. However, I could mostly find average prices at communal level. Copenhagen commune, as an example, is big (for Denmark) and prices vary a lot depending on neighbourhoods. Getting an average price per square meter for the Copenhagen commune is not useful for a prospective buyer - square meter prices can vary by 30-40.000 DKK for neighbourhoods barely 5 km from one another. 

## How?
The project has 3 main parts:
- Web scraping of housing listings on boliga.dk, using Python, Pandas and the BeautifulSoup library
- Automation using Windows Task Scheduler
- Data visualisation and dashboard in Tableau

## Caveats
- As of February 2023, data is only related to apartments ("lejlighed" and "villalejlighed"). Boliga.dk does not use weighted area (defined by Finanstilsynet) when calculated the square meter price of a house, which makes it impossible to compare two houses together. I chose therefore not to include houses data in the dataset.
- Data is not representative of the full housing sales picture in Denmark. Since data is scraped from a housing sales website, it only includes listings that are made public. A lot of properties are indeed sold without having been made public.
- There can be small discrepancies in the date a property is put on sale or sold/removed from the website, which are dependant on how quickly the website publishes listings.
- Automation via Windows Task Scheduler is practical but not ideal. I would like to
avoid having to leave my computer on sleep mode for it to work. I am looking into ways to take the automation online.

