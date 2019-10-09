import os
import re
import sys
import time
import csv
import argparse

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# manage args
parser = argparse.ArgumentParser(prog='scraper')
parser.add_argument('csv_file', help="path of the csv file")
parser.add_argument('url_file', help="path of the urls file")
parser.add_argument('-t', '--time', help="time (s) to load js", default=5)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

# manage chrome driver options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),
                          chrome_options=chrome_options)

# recuperate the paths in the file
paths = [line.rstrip('\n') for line in open(args.url_file)]

# define selected stats
selected_stats = ["Ball Possession", "Goal Attempts", "Shots on Goal",
                  "Shots off Goal", "Blocked Shots", "Free Kicks",
                  "Corner Kicks", "Offsides", "Goalkeeper Saves",
                  "Fouls", "Total Passes"]

count = 0
with open(args.csv_file, mode='w') as f:
    f_writer = csv.writer(f, delimiter=',', quotechar='"',
                          quoting=csv.QUOTE_MINIMAL)

    for path in paths:
        driver.get(path)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sportName")))
        title = driver.title
        word = re.search(r'\b(Results)\b', title)
        title = title[0:word.start()]

        # click on more button until all the matchs are displayed
        while True:
            more_button = driver.find_elements_by_class_name(
                "event__more--static")
            if more_button == []:
                break
            driver.execute_script("arguments[0].click();", more_button[0])
            time.sleep(args.time)

        # recuperate match_ids
        match_ids = [match.get_attribute("id")[4:] for
                     match in driver.find_elements_by_class_name(
                        "event__match--static")]

        # recuperate statistics for each matchs and write in csv file
        for match_id, i in
        zip(match_ids, tqdm(range(0, len(match_ids)), desc=title)):

            # variable to check if there isn't empty value
            valid = False
            while not valid:
                match_path = "https://www.flashscore.com/match/{}\
                /#match-statistics;0".format(match_id)
                driver.get(match_path)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                    (By.ID, "tab-statistics-0-statistic")))

                # list to store the stats of the match
                row = []

                # recuperate the numbers of goals and store it
                goals = driver.find_elements_by_class_name("scoreboard")
                row.append(goals[0].text)
                row.append(goals[1].text)

                # recuperate the name of the stats and the values
                stat_titles = [stat.text for stat in
                               driver.find_elements_by_class_name(
                                   "statText--titleValue")]
                home_stats = [home_stat.text for home_stat in
                              driver.find_elements_by_class_name(
                                  "statText--homeValue")]
                away_stats = [away_stat.text for away_stat in
                              driver.find_elements_by_class_name(
                                  "statText--awayValue")]

                # store the stats which are desired
                n = 0
                for stat_title, home_stat, away_stat in
                zip(stat_titles, home_stats, away_stats):

                    if stat_title in selected_stats:
                        row.append(home_stat.replace("%", ""))
                        row.append(away_stat.replace("%", ""))
                        n += 1

                valid = not("" in row)

            # check if all the desired stats are recupered and write in the csv
            if n == len(selected_stats):
                f_writer.writerow(row)
                count += 1
                if args.verbose:
                    sys.stdout.write('\r' + str(row))
