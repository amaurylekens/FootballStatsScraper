[![Build Status](https://travis-ci.org/amaurylekens/FootballStatsScraper.svg?branch=master)](https://travis-ci.org/amaurylekens/FootballStatsScraper)
[![codecov](https://codecov.io/gh/amaurylekens/FootballStatsScraper/branch/master/graph/badge.svg)](https://codecov.io/gh/amaurylekens/FootballStatsScraper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# A Football stats scraper

This command-line tool can retrieve football stats from the flashcore website. It uses the python scraping package, selenium.

## Stats recuperated


We get the statistics on this type of page :

<p align="center">
  <img src="https://github.com/amaurylekens/FootballStatsScraper/blob/master/images/page.png" style="width: 10%; height: 10%"/>
</p>

You can retrieve all types of stats that are offered on these pages by modifying the *params.yml* file.

All the stats are stored in a csv file.

## Getting started 

### Dependencies

* The chromedriver (download [here](https://chromedriver.chromium.org/downloads))
* Python librairies : csv, argprse, tqdm, selenium, pyyaml

### Configuration

The repo is organized like this :


```bash
├── scraper
│   ├── scraper.py
│   └── ...
├── params.yml
├── images
└── ...
``` 

The *params.yml* file contains the urls and the stats that the program will scrape :

* Valid params *stats* are the titles of the stats found on the flashscore pages.
* Valid *url* params are flashscore urls that end with */results* (ex: https://www.flashscore.com/football/italy/series-a-2018-2019/results/)

### Launch

* Normal mode

```bash
python3 scraper.py [url file path] [csv file] 
``` 

* Verbose mode

```bash
python3 scraper.py [url file path] [csv file] -v
```
