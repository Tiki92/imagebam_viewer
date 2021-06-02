import requests as req

resp = req.get("https://www.imagebam.com/view/GAKC")
# print(resp.text)
print(resp.status_code)