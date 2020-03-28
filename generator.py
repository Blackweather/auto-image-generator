from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import random
import subprocess
import sys
import os.path
from requests import get

# global variables
# TODO: change the terms to be parsed from file
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

# make sure chrome doesn't need to be scrolled
MAX_IMAGES = 11

# in seconds
image_display_time = 5 * 60

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

# reads the provided file and returns a list of terms
def get_terms_from_file(filename = "default.terms"):
    pass

def get_cmd_args():
    if len(sys.argv) == 3 or len(sys.argv) == 5:
        if sys.argv[1] == "--file" or sys.argv[1] == "-f":
            # check file os.path.isfile()
            # this should be if sys.argv[2] is filepath
            if True:
                # check if argv[2] is file
                # if it is open and parse
                # if parsed check for more args
                pass
            pass
        elif sys.argv[1] == "--time" or sys.argv[1] == "-t":
            # check time
            if sys.argv[2].isnumeric():
                image_display_time = int(sys.argv[2] * 60)
                if len(sys.argv) > 3:
                    if len(sys.argv) == 5:
                        if sys.argv[3] == "--file" or sys.argv[3] == "-f":
                            # check file
                            pass
                        else:
                            print("Wrong number of arguments, see usage below:\n")
                            print_help()
                    else:
                        print("Wrong number of arguments, see usage below:\n")
                        print_help()
            else:
                print("Wrong argument format, see usage below:\n")
                print_help()
        else:
            print("Wrong number of arguments, see usage below:\n")
            print_help()
    elif len(sys.argv) == 1:
        print("Running using the default arguments")
        get_terms_from_file()
    else:
        print("Wrong number of arguments, see usage below:\n")
        print_help()
    pass

def download_image():
    pass

def open_image(filename):
    pass


def main():
    while True:
        # initialize webdriver
        wd = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        wd.maximize_window()
        wd.get('http://images.google.com/')

        # search for one of the terms provided in file
        search_bar = wd.find_elements_by_css_selector("input.gLFyf")[0]
        search_term = random.choice(search_terms)
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.ENTER)

        # click on a random found image thumbnail
        images = wd.find_elements_by_css_selector("img.Q4LuWd")
        chosen_image = images[random.randrange(0, MAX_IMAGES - 1)]
        try:
            chosen_image.click()
        except Exception:
            wd.quit()
            continue

        # get URL from the enlarged image thumbnail
        download_search = wd.find_elements_by_css_selector("img.n3VNCb")
        images_queried = [link for link in download_search if 'http' in link.get_attribute('src')]
        if len(images_queried) == 0:
            wd.quit()
            continue

        image_to_download = images_queried[0]
        image_url = image_to_download.get_attribute('src')
        wd.get(image_url)

        # quit webdriver
        time.sleep(5)
        wd.quit()

        # get filename using the extension from image url
        file_name = "image." + image_url.split('.')[-1]
        # check if the file name contains supported format
        # supported formats - jpg, jpeg, png
        # download picked image
        with open(file_name, "wb") as opened_file:
            response = get(image_url)
            opened_file.write(response.content)

        # display image using feh
        displayed_image = subprocess.Popen(["feh", "--hide-pointer", "-Z", "-F", "-x", "-q", "-B", "black", file_name])

        # let the image be displayed for specified time
        time.sleep(image_display_time)

        # close the image display
        displayed_image.kill()

if __name__ == "__main__":
    main()
