from bs4 import BeautifulSoup
import requests as req
import re

"""
Get all disease detail link from a Category, categories from A - Z
"""

links = []
prefix = "https://www.drugs.com"

for code in range(ord('a'), ord('z') + 1):
    letter = chr(code)

    resp = req.get("https://www.drugs.com/alpha/{}.html".format(letter))
    soup = BeautifulSoup(resp.text, 'html.parser')
    contents = soup.body.find_all("ul", {"class": "ddc-list-column-2"})[0].find_all("a")

    for link in contents:
        href = link.get('href')
        links.append(prefix + href )

links_formated = '\n'.join(links)
with open("drugs_links.txt", "w") as f:
    f.write(links_formated)


