import json
import time
import socks
import socket
from django.utils import timezone
import requests as req
from bs4 import BeautifulSoup
from datetime import date, datetime
from .models import Patterns, Links, Galleries, CurrentPattern
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException

def getPageContent(URL): 
    # Configure the proxy settings for Tor
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.socks_proxy = 'localhost:9050'
    proxy.socks_version = 5

    capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    capabilities.update(proxy.to_capabilities())

    # Setup Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')   # Optional: Run in headless mode
    firefox_options.proxy = proxy

    # Path to GeckoDriver
    gecko_driver_path = '/usr/local/bin/geckodriver'  # Update with your path
    service = Service(gecko_driver_path)

    # Initialize the WebDriver for Firefox
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Navigate to the page
        driver.get(URL)

        try:
            continue_button = driver.find_element(By.XPATH, '//a[contains(text(), "Continue to your image")]')
            continue_button.click()
            print("Button clicked.")
        except NoSuchElementException:
            print("Button not found.")

        # Get the final page source
        page_source = driver.page_source

        # Save or print the page source
        with open('imagebam_page.html', 'w', encoding='utf-8') as file:
            file.write(page_source)

    finally:
        driver.quit()
        return page_source

def increment_pattern(current_pattern):
  current_pattern.current = current_pattern.current + 1
  current_pattern.save()
  current_pattern = CurrentPattern.objects.get(id=1)
  pattern = Patterns.objects.get(id=current_pattern.current).pattern
  print("INCRESED PATTERN:", pattern)
  print("            ")


def check_links():
  begin_time = datetime.now()
  current_pattern = CurrentPattern.objects.get(id=1)
  pattern = Patterns.objects.get(id=current_pattern.current).pattern

  while pattern != "ZZZZ":
    time_now = timezone.localtime(timezone.now()).strftime("%d-%m-%Y %H:%M:%S")
    URL = "https://www.imagebam.com/view/AA{}".format(pattern)
    print("PATTERN NOW:", pattern)

    ip_address = req.get("https://api.ipify.org/?format=json").json()['ip']
    print("IP:", ip_address)

    link_checker(pattern, URL, current_pattern)

    current_pattern = CurrentPattern.objects.get(id=1)
    pattern = Patterns.objects.get(id=current_pattern.current).pattern

    # print("                   ")
    print("TIME {}".format(time_now))
    print("DURATION OF EXECUTION:", datetime.now() - begin_time)
    # print("URL {}".format(URL))

def link_checker(pattern, URL, current_pattern):
  status_req = req.get(URL).status_code
  # print("REQUEST STATUS {}".format(status_req))

  if status_req == 200:
    resp = getPageContent(URL)

    soup = BeautifulSoup(resp, 'html.parser')
    soup_tag = BeautifulSoup(resp, 'html.parser')
    soup_gal_id = BeautifulSoup(resp, 'html.parser')
    links = soup_gal_id.find_all("a", class_="text-decoration-none")
    gal_link = "https://www.example.com/nonexistentpage12345"
    for link in links:
        href = link.get('href')
        if href and 'GA' in href:
            gal_link = link.get("href")
            break
    
    soup = soup.body.div.main
    soup = soup.find_all(attrs={"class": "fas fa-ellipsis-h"})

    # print("GETING IMAGE TAG")
    image_tag = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('src') 
    image_tag = str(image_tag)
    print("IMAGE TAG: {}".format(image_tag))
    # print("SOUPPPP", len(soup), soup, soup_tag)

    tag_alt = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('alt')
    tag_alt = str(tag_alt)

    if gal_link != "https://www.example.com/nonexistentpage12345":
        # links = soup_gal_id.find_all("a", class_="text-decoration-none")
        print("GALLERY LINK {}".format(gal_link))

        resp_gal = req.get(gal_link)
        status_req_gal = resp_gal.status_code
        if status_req_gal == 200:
          if image_tag:
            gal_name = tag_alt

            print("GAL NAME {}".format(gal_name))
          else:
           gal_name = "none"

        # print("Picture belongs to a Gallery {}".format(gal_link))

        # print("CHECK IF GALLERY LINK ALREADY IN THE DB")
        print("GAL LINK", gal_link)
        existing = Galleries.objects.filter(gallery_link=gal_link).first()
        # print("EXISTING {}".format(existing))
        if existing == None:
            # print("GALLERY LINK NOT PRESENT, ADDING...")

            gal = Galleries()
            gal.gallery_link = gal_link
            gal.link = URL
            gal.img_tag = image_tag
            gal.status = status_req
            gal.name = gal_name
            gal.save()

            print("NEW GAL")
            increment_pattern(current_pattern)
            # current_pattern.current = current_pattern.current + 1
            # current_pattern.save()

        else:
            print("GAL IN DB")
            # print("INCREMENT CURRENT PATTERN")
            increment_pattern(current_pattern)
            # current_pattern.current = current_pattern.current + 1
            # current_pattern.save()
    else:
        # print("Picture does not belong to a gallery, URL will be stored in Links database {}".format(URL))
        existing_img = Links.objects.filter(img_tag=image_tag).first()

        if existing_img == None:

          link = Links()
          link.link = URL
          link.img_tag = image_tag
          link.status = status_req
          link.name = tag_alt
          link.save()

          print("NEW IMG")
          increment_pattern(current_pattern)
        else:
          print("IMG IN DB")
          increment_pattern(current_pattern)

        # current_pattern.current = current_pattern.current + 1
        # current_pattern.save()
  else:
    # print("URL request STATUS is {}".format(status_req))
    print("URL 404")
    # print("INCREMENT CURRENT PATTERN")
    increment_pattern(current_pattern)
    # current_pattern.current = current_pattern.current + 1
    # current_pattern.save()
