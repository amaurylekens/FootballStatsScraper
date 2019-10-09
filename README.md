# A Football stats scraper

This command-line tool can retrieve football stats from the flashcore website. It uses the python scraping package, selenium.

## Stats recuperated


We get the statistics on this type of page.

![page](https://github.com/amaurylekens/FootballStatsScraper/blob/master/images/page.png)

The statistics recovered are as follows: Goals, Ball Possession, Goal Attempts, Shots on Goal, Shots off Goal, Blocked Shots, Free Kicks, Corner Kicks, Offsides, Goalkeeper Saves, Fouls, Total Passes (for the two teams). So we recovered 24 stats.

## Getting started 

### Dependencies

* The chromedriver (download [heer](https://chromedriver.chromium.org/downloads))
* Python librairies : csv, argprse, tqdm, selenium

### Configuration

The repo is organized like this :


```bash
├── scraper.py
├── url.txt
├── images
└── .gitignore
``` 

The "url.txt" file contains the urls that the program will scrape.

### Launch

