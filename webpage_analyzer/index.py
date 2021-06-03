import json
import requests as req
from bs4 import BeautifulSoup

URL = "https://www.imagebam.com/view/MEMYAQ"
resp = req.get(URL)
status_req = resp.status_code
if status_req == 200:

    soup = BeautifulSoup(resp.content, 'html.parser')
    soup = soup.body.div.main
    soup = soup.find_all(attrs={"class": "fas fa-ellipsis-h"})
    # soup = soup.find_previous("a")["href"]
    # soup = str(soup)
    if len(soup) > 0:
        soup = soup[0]
        soup = soup.find_previous("a")["href"]

        print("Picture belongs to a Gallery {}".format(soup))
    else:
        print("Picture does not belong to a gallery, URL will be stored in Links database {}".format(URL))
else:
    print("URL request STATUS is {}".format(status_req))