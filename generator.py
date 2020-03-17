from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import random
import subprocess
import sys
import os.path
from requests import get

def print_help():
    print("This script will help you find random images on the web using" + 
        " default random search terms or provided in file")
    print("Running the script:")
    print("python generator.py <args> / python3 generator.py <args>")
    print("Command line arguments:")
    print("-f/--file <filename> - the script will try to load search terms" + 
        " from the provided file (see default.terms for example of file)")
    print("-t/--time <number> - time of displaying a single image (in minutes)")
    print("-h/--help - display this help")
    print("Note: wrong arguments will result in displaying help")
    print("Defaults:")
    print("--file default.terms")
    print("--time 5")

def get_cmd_args():
    if len(sys.argv) == 3 or len(sys.argv) == 5:
        if sys.argv[1] == "--file" or sys.argv[1] == "-f":
            # check file
            pass
        elif sys.argv[1] == "--time" or sys.argv[1] == "-t":
            # check time
            pass
        else:
            print("Wrong number of arguments, see usage below")
            print_help()
    elif len(sys.argv) == 1:
        print("Running using the default arguments")
    else:
        print("Wrong number of arguments, see usage below:\n")
        print_help()

# reads the provided file and returns a list of terms
def get_terms_from_file(filename = "default.terms"):
    pass

def download_from_url(url, filename):
    pass

def download_image():
    pass

def open_image(filename):
    pass

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
    "british cat",
    "cat stock photos"
]

while True:
    wd = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    wd.maximize_window()
    wd.get('http://images.google.com/')

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
