# A Football stats scraper

This command-line tool can retrieve football stats from the flashcore website. It uses the python scraping package, selenium.

## Stats recuperated


We get the statistics on this type of page :

<p align="center">
  <img src="https://github.com/amaurylekens/FootballStatsScraper/blob/master/images/page.png" style="width: 10%; height: 10%"/>
</p>

The statistics recovered are as follows: Goals, Ball Possession, Goal Attempts, Shots on Goal, Shots off Goal, Blocked Shots, Free Kicks, Corner Kicks, Offsides, Goalkeeper Saves, Fouls, Total Passes (for the two teams). So we recovered 24 stats.

All the stats are stored in a csv file.

## Getting started 

### Dependencies

* The chromedriver (download [here](https://chromedriver.chromium.org/downloads))
* Python librairies : csv, argprse, tqdm, selenium

### Configuration

The repo is organized like this :


```bash
├── scraper.py
├── url.txt
├── images
└── .gitignore
``` 

The *url.txt* file contains the urls that the program will scrape.

### Launch

* Normal mode

```bash
python3 scraper.py [url file path] [csv file] 
``` 

* Verbose mode

```bash
python3 scraper.py [url file path] [csv file] -v
```
