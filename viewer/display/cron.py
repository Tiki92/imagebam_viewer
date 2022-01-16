import json
import time
import socks
import socket
from django.utils import timezone
import requests as req
from bs4 import BeautifulSoup
from datetime import date, datetime
from .models import Patterns, Links, Galleries, CurrentPattern
from stem import Signal
from stem.control import Controller

controller = Controller.from_port(port=9051)

def increment_pattern(current_pattern):
  current_pattern.current = current_pattern.current + 1
  current_pattern.save()
  current_pattern = CurrentPattern.objects.get(id=1)
  pattern = Patterns.objects.get(id=current_pattern.current).pattern
  print("INCRESED PATTERN:", pattern)
  print("            ")


def renew_tor_ip():
  controller.authenticate(password="MyStr0n9P#D")
  controller.signal(Signal.NEWNYM)
  # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050, True)
  # socket.socket = socks.socksocket
  
  time.sleep(10)
  # with Controller.from_port(port = 9051) as controller:
  #     controller.authenticate(password="MyStr0n9P#D")
  #     controller.signal(Signal.NEWNYM)
  #     time.sleep(5)

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket

connectTor()
print("CONECTED TO TOR")

def check_links():
  begin_time = datetime.now()
  current_pattern = CurrentPattern.objects.get(id=1)
  pattern = Patterns.objects.get(id=current_pattern.current).pattern

  while pattern != "ZZZ9":
    time_now = timezone.localtime(timezone.now()).strftime("%d-%m-%Y %H:%M:%S")
    URL = "https://www.imagebam.com/view/AA{}".format(pattern)
    print("PATTERN NOW:", pattern)

    session = req.session()
    

    # TO Request URL with SOCKS over TOR
    # session.proxies = {}
    # session.proxies['http']='socks5h://localhost:9050'
    # session.proxies['https']='socks5h://localhost:9050'
    # r = session.get('http://httpbin.org/ip')
    ip_address = req.get("https://api.ipify.org/?format=json").json()['ip']
    print("IP:", ip_address)

    resp = session.get(URL)
    # print("CONTENT:", resp.content)

    link_checker(pattern, resp, URL, current_pattern)

    current_pattern = CurrentPattern.objects.get(id=1)
    pattern = Patterns.objects.get(id=current_pattern.current).pattern

    # print("                   ")
    print("TIME {}".format(time_now))
  print("DURATION OF EXECUTION:", datetime.now() - begin_time)
    # print("URL {}".format(URL))

def link_checker(pattern, resp, URL, current_pattern):
  status_req = resp.status_code
  # print("REQUEST STATUS {}".format(status_req))

  if status_req == 200:
    
    soup = BeautifulSoup(resp.content, 'html.parser')
    soup_tag = BeautifulSoup(resp.content, 'html.parser')
    tag_alt = BeautifulSoup(resp.content, 'html.parser')
    banned_ip = soup_tag.body.main.div.find("div", {"class": "message"}) # .p.contents (get the specific content of the mesasge)

    if banned_ip != None:
      print("BANNED IP:", banned_ip)
      renew_tor_ip()
      check_links()

    soup = soup.body.div.main
    soup = soup.find_all(attrs={"class": "fas fa-ellipsis-h"})

    # print("GETING IMAGE TAG")
    image_tag = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('src') 
    image_tag = str(image_tag)
    print("IMAGE TAG: {}".format(image_tag))

    tag_alt = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('alt')
    tag_alt = str(tag_alt)

    if len(soup) > 0:
        soup = soup[0]
        gal_link = soup.find_previous("a")["href"]
        # print("GALLERY LINK {}".format(gal_link))

        resp_gal = req.get(gal_link)
        status_req_gal = resp_gal.status_code
        if status_req_gal == 200:

          soup_gal_id = BeautifulSoup(resp_gal.content, 'html.parser')
          gal_name = soup_gal_id.find("a", {"id": "gallery-name"}).getText()
          # print("GAL NAME {}".format(gal_name))
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
