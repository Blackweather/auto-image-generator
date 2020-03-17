from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import random
import subprocess
from requests import get

while True:
    wd = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    wd.maximize_window()
    wd.get('http://images.google.com/')
    search_terms = [ 
        "kotki",
        "kot",
        "petite cats",
        "young cats",
        "old cats",
        "hairy cats",
        "cute cats",
        "slodkie kotki",
        "kiciusie",
        "kocieta",
        "small cats",
        "little cats",
        "fat cats",
        "homeless cats",
        "norwegian cat",
        "white cat",
        "kociaki",
        "persian cat",
        "shorthair cat",
        "british cat"
    ]

    MAX_IMAGES = 11

    search_bar = wd.find_elements_by_css_selector("input.gLFyf")[0]

    search_term = random.choice(search_terms)

    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.ENTER)

    images = wd.find_elements_by_css_selector("img.Q4LuWd")
    chosen_image = images[random.randrange(0, MAX_IMAGES - 1)]
    try:
        chosen_image.click()
    except Exception:
        wd.quit()
        continue

    download_search = wd.find_elements_by_css_selector("img.n3VNCb")

    images_queried = [link for link in download_search if 'http' in link.get_attribute('src')]
    if len(images_queried) == 0:
        wd.quit()
        continue

    image_to_download = images_queried[0]


    image_url = image_to_download.get_attribute('src')

    wd.get(image_url)

    time.sleep(5)
    wd.quit()


    file_name = "kotki." + image_url.split('.')[-1]
    # download cat image
    with open(file_name, "wb") as opened_file:
        response = get(image_url)
        opened_file.write(response.content)

    # display image
    displayed_image = subprocess.Popen(["feh", "--hide-pointer", "-Z", "-F", "-x", "-q", "-B", "black", file_name])

    time.sleep(300)

    displayed_image.kill()
