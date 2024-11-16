# Polish unemployment - county map 
A small project which aim is to present on an interactive map of polish unemployemnt rate (broken down by county)

## Interctive map
https://unemployment-2d84.onrender.com/

## Data sources
1. [The Central Statistical Office unemployment data for April 2021](https://stat.gov.pl/obszary-tematyczne/rynek-pracy/bezrobocie-rejestrowane/bezrobotni-zarejestrowani-i-stopa-bezrobocia-stan-w-koncu-kwietnia-2021-r-,2,105.html)
2. [The Main Office of Geodesy and Cartography regional division of the country into counties (shapefile)](http://www.gugik.gov.pl/pzgik/dane-bez-oplat/dane-z-panstwowego-rejestru-granic-i-powierzchni-jednostek-podzialow-terytorialnych-kraju-prg)

## Inspiration articles:
1. [Folium map tutorial](https://python-visualization.github.io/folium/installing.html)
2. [Deployment of map on Heroku](https://towardsdatascience.com/your-cool-folium-maps-on-the-web-313f9d1a6bcd)

## Authors
Sebastian Konicz - sebastian.konicz@gmail.com

## Project Organization

------------

    ├── data                            <- place whre the data is stored
    │   │
    │   ├── final                           <- final maps created by script
	│   │
    │   ├── geo                             <- geospatial data
    │   │
    │   ├── interim                         <- intermediate data that has been transformed.
    │   │
    │   └── raw                             <- the original, immutable data dump.
    │
    ├── src                             <- source code for use in this project.
    │   │
    │   ├── 01_data_load.py                 <- transforms oficial unemployment data to datafram
    │   │
    │   └── 02_map.py                       <- crates map besed on unemplyment and geospacial data
	│
    ├── templates                       <- folder with template sites for flask
	│
    ├── app.py                          <- app for running flask
	│
    ├── Procfile                        <- file for flask
	│
    ├── README.md                       <- the top-level README for developers using this project.
	│
    ├── requirements.txt                <- requirements for the project
	│
    └── runtime.txt                     <- python version fo deployemnt

------------
