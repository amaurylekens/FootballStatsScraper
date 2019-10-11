import os
import re
import sys
import time
import csv
import argparse
import yaml

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_match_ids_by_url(url, driver, wait_time):

    """Recuperate the ids of the matchs in the page

        :param url: url of the page
        :param driver: chromedriver object
        :param wait_time: time to wait for some event (js loading, ...)
        :return: tupple with a list of the ids and the title of the page"""

    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sportName")))
    title = driver.title
    word = re.search(r'\b(Results)\b', title)
    title = title[0:word.start()]

    # click on more button until all the matchs are displayed
    while True:
        more_link = driver.find_elements_by_class_name("event__more--static")
        if more_link == []:
            break
        driver.execute_script("arguments[0].click();", more_link[0])
        time.sleep(wait_time)

    # recuperate match_ids
    match_ids = [match.get_attribute("id")[4:] for
                 match in driver.find_elements_by_class_name(
                    "event__match--static")]

    return (match_ids, title)


def get_stats_by_match_id(match_id, driver, selected_stats):

    """Recuperate the stats of a match by his id

        :param match_id: the id of the match
        :param driver: chromedriver object
        :param selected_stats: list of stats to recuperate
        :return: a list with the stats of a None object (if invalid)"""

    valid = False
    while not valid:
        match_path = "{}/#match-statistics;0".format(match_id)
        match_path = "https://www.flashscore.com/match/{}".format(match_path)
        driver.get(match_path)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.ID, "tab-statistics-0-statistic")))

        # list to store the stats of the match
        row = []

        # recuperate the numbers of goals and store it
        goals = driver.find_elements_by_class_name("scoreboard")
        if goals[0].text != "":
            row.append(int(goals[0].text))
        else:
            row.append(goals[0].text)
        if goals[1].text != "":
            row.append(int(goals[1].text))
        else:
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
        for stat_title, home_stat, away_stat in zip(stat_titles,
                                                    home_stats,
                                                    away_stats):

            if stat_title in selected_stats:
                if home_stat.replace("%", "") != "":
                    row.append(int(home_stat.replace("%", "")))
                else:
                    row.append(home_stat.replace("%", ""))
                if away_stat.replace("%", "") != "":
                    row.append(int(away_stat.replace("%", "")))
                else:
                    row.append(away_stat.replace("%", ""))
                n += 1

        valid = not("" in row)

    # check that we have all the good stats
    if n == len(selected_stats):
        return row
    else:
        return None


def main():

    # manage args
    parser = argparse.ArgumentParser(prog='scraper')
    parser.add_argument('csv_file', help="path of the csv file")
    parser.add_argument('url_file', help="path of the urls file")
    parser.add_argument('-t', '--time', help="time (s) to load js", default=10)
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    # manage chrome driver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver_osx"),
                              options=chrome_options)

    with open(args.url_file) as f_params:
        data = yaml.load(f_params, Loader=yaml.FullLoader)
        urls = data['urls']
        selected_stats = data['stats']

    count = 0
    with open(args.csv_file, mode='w') as f:
        f_writer = csv.writer(f, 
                              delimiter=',', 
                              quotechar='"',
                              quoting=csv.QUOTE_MINIMAL)

        for url in urls:
            match_ids, title = get_match_ids_by_url(url, driver, args.time)

            # recuperate statistics for each matchs and write in csv file
            for match_id, i in zip(match_ids,
                                   tqdm(range(0, len(match_ids)), desc=title)):

                row = get_stats_by_match_id(match_id, driver, selected_stats)
                if row is not None:
                    f_writer.writerow(row)
                    count += 1


if __name__ == '__main__':
    main()
