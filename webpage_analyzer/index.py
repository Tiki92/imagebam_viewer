import json
import requests as req
from bs4 import BeautifulSoup

URL = "https://www.imagebam.com/view/GA62J"
resp = req.get(URL)
status_req = resp.status_code
if status_req == 200:

    soup = BeautifulSoup(resp.content, 'html.parser')
    soup_tag = BeautifulSoup(resp.content, 'html.parser')
    soup_gal_id = BeautifulSoup(resp.content, 'html.parser')
    soup = soup.body.div.main
    soup = soup.find_all(attrs={"class": "fas fa-ellipsis-h"})

    print("GETING IMAGE TAG")
    # image_tag = soup_tag.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"}).get('alt')   
    # image_tag = str(image_tag)
    # print("IMG TAG {}".format(image_tag))

    gal_name = soup_gal_id.find("a", {"id": "gallery-name"}).getText()

    print("GAL NAME {}".format(gal_name))

    # soup = BeautifulSoup(resp.content, 'html.parser')
    # soup = soup.body.div.main.find("div", {"class": "view-image"}).a.find("img",{"class": "main-image"})
    # # soup = soup.nextSibling
    # print(soup)
#     soup = soup.find_all(attrs={"class": "fas fa-ellipsis-h"})
#     # soup = soup.find_previous("a")["href"]
#     # soup = str(soup)
#     if len(soup) > 0:
#         soup = soup[0]
#         soup = soup.find_previous("a")["href"]

#         print("Picture belongs to a Gallery {}".format(soup))
#     else:
#         print("Picture does not belong to a gallery, URL will be stored in Links database {}".format(URL))
# else:
#     print("URL request STATUS is {}".format(status_req))