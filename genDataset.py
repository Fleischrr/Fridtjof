import os
import time
import urllib
from duckduckgo_search import ddg_images
from fastcore.all import *

# Søker etter bilder via DuckDuckGo
def search_images(term, max_images=30):
    print(f"Searching for '{term}'")
    return L(ddg_images(term, max_results=max_images)).itemgot('image')        

# Laster ned bilder fra URLs og lagrer de til disk
def download_image(url, file_path):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded image: {url}")
    except Exception as e:
        print(f"Error downloading image '{url}': {e}")

# Definere mappe for alle bilder
IMAGES_DIR = "images"
CAR_IMAGES_DIR = os.path.join(IMAGES_DIR, "car")
NO_CAR_IMAGES_DIR = os.path.join(IMAGES_DIR, "no_car")
                    
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)               # Lage mappe for bilder 
if not os.path.exists(CAR_IMAGES_DIR):
    os.makedirs(CAR_IMAGES_DIR)           # Lage mappe for bilder med biler
if not os.path.exists(NO_CAR_IMAGES_DIR):
    os.makedirs(NO_CAR_IMAGES_DIR)        # Lage mappe for bilder uten biler      

queryYes = "cars on the road"
queryNo = "empty roads"
num_images = 200
min_req_images = 300

# Sjekker om det er allerede minst 150 bilder lagret i mappene
if len(os.listdir(CAR_IMAGES_DIR)) + len(os.listdir(NO_CAR_IMAGES_DIR)) >= min_req_images:
    print("Already downloaded 150 images or more, exiting...")
else:
    # Søk etter bilder av biler
    urls = search_images(queryYes, num_images)

    # Last ned bilder fra URLs
    for i, url in enumerate(urls):
        file_name = f"car_{i+1}.jpg"
        file_path = os.path.join(CAR_IMAGES_DIR, file_name)
        download_image(url, file_path)
        time.sleep(1)

    # Søk etter bilder av ikke noen biler
    urls = search_images(queryNo, num_images)

    # Last ned bilder fra URLs
    for i, url in enumerate(urls):
        file_name = f"no_car_{i+1}.jpg"
        file_path = os.path.join(NO_CAR_IMAGES_DIR, file_name)
        download_image(url, file_path)
        time.sleep(1)

# Tell antall bilder i hver mappe og totale bilder
num_car_images = len(os.listdir(CAR_IMAGES_DIR))
num_no_car_images = len(os.listdir(NO_CAR_IMAGES_DIR))
total_images = num_car_images + num_no_car_images

print(f"Number of car images: {num_car_images}")
print(f"Number of no car images: {num_no_car_images}")
print(f"Total number of images: {total_images}")    

