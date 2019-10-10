import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper import get_stats_by_match_id


tests_values = [("Mi67N5em", [0, 2, 76, 24, 18, 7, 2, 2, 6, 3, 10, 2,
                              16, 12, 9, 1, 1, 2, 0, 2, 11, 14, 712, 228]),
                ("CtaKK3u6", [1, 4, 44, 56, 10, 13, 3, 7, 6, 4, 1, 2, 15,
                	          9, 3, 4, 1, 0, 3, 2, 8, 15, 404, 521]),
                ("nch9U8kc", None),
                ("QmiDTS43", None)]

@pytest.mark.parametrize('id, expected', tests_values)
def test_get_stats_by_match_id(id, expected):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),
    	                      options=chrome_options)

    selected_stats = ["Ball Possession", "Goal Attempts", "Shots on Goal", 
                      "Shots off Goal", "Blocked Shots", "Free Kicks", 
                      "Corner Kicks", "Offsides", "Goalkeeper Saves", 
                      "Fouls", "Total Passes"]

    assert get_stats_by_match_id(id, driver, selected_stats) == expected

    [0, 2, 76, 24, 18, 7, 2, 2, 6, 3, 10, 2,
    16, 12, 9, 1, 1, 2, 0, 2, 11, 14, 712, 228]

