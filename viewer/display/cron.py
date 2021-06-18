import json
import time
from django.utils import timezone
import requests as req
from bs4 import BeautifulSoup
from datetime import date, datetime
from .models import Patterns, Links, Galleries, CurrentPattern

time_now = timezone.localtime(timezone.now()).strftime("%d-%m-%Y %H:%M:%S")
current_pattern = CurrentPattern.objects.get(id=1)
pattern = Patterns.objects.get(id=current_pattern.current).pattern
URL = "https://www.imagebam.com/view/{}".format(pattern)

print("                   ")
print("TIME {}".format(time_now))
print("URL {}".format(URL))

def link_checker():
  resp = req.get(URL)
  status_req = resp.status_code
  print("REQUEST STATUS {}".format(status_req))

  if status_req == 200:
    
    soup = BeautifulSoup(resp.content, 'html.parser')
    soup_tag = BeautifulSoup(resp.content, 'html.parser')
    tag_alt = BeautifulSoup(resp.content, 'html.parser')

    soup = soup.body.div.main
    soup = soup.find_all(attrs={"class": "fas fa-ellipsis-h"})

    print("GETING IMAGE TAG")
    image_tag = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('src') 
    image_tag = str(image_tag)

    tag_alt = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('alt')
    tag_alt = str(tag_alt)

    if len(soup) > 0:
        soup = soup[0]
        gal_link = soup.find_previous("a")["href"]
        print("GALLERY LINK {}".format(gal_link))

        resp_gal = req.get(gal_link)
        status_req_gal = resp_gal.status_code
        if status_req_gal == 200:

          soup_gal_id = BeautifulSoup(resp_gal.content, 'html.parser')
          gal_name = soup_gal_id.find("a", {"id": "gallery-name"}).getText()
          print("GAL NAME {}".format(gal_name))
        else:
          gal_name = "none"

        print("Picture belongs to a Gallery {}".format(gal_link))

        print("CHECK IF GALLERY LINK ALREADY IN THE DB")
        existing = Galleries.objects.filter(gallery_link=gal_link).first()
        print("EXISTING {}".format(existing))
        if existing == None:
            print("GALLERY LINK NOT PRESENT, ADDING...")

            gal = Galleries()
            gal.gallery_link = gal_link
            gal.link = URL
            gal.img_tag = image_tag
            gal.status = status_req
            gal.name = gal_name
            gal.save()

            print("INCREMENT CURRENT PATTERN")
            current_pattern.current = current_pattern.current + 1
            current_pattern.save()

        else:
            print("GALLERY LINK PRESENT IN DB")
            print("INCREMENT CURRENT PATTERN")
            current_pattern.current = current_pattern.current + 1
            current_pattern.save()
    else:
        print("Picture does not belong to a gallery, URL will be stored in Links database {}".format(URL))
        link = Links()
        link.link = URL
        link.img_tag = image_tag
        link.status = status_req
        link.name = tag_alt
        link.save()

        print("INCREMENT CURRENT PATTERN")
        current_pattern.current = current_pattern.current + 1
        current_pattern.save()
  else:
    print("URL request STATUS is {}".format(status_req))

    print("INCREMENT CURRENT PATTERN")
    current_pattern.current = current_pattern.current + 1
    current_pattern.save()