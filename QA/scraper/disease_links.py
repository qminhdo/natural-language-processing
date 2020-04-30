from bs4 import BeautifulSoup
import requests as req
import re

"""
Get all disease detail link from a Category, categories from A - Z
"""

links = []
prefix = "https://www.mayoclinic.org"

for code in range(ord('A'), ord('Z') + 1):
    letter = chr(code)

    resp = req.get("https://www.mayoclinic.org/diseases-conditions/index?letter={}".format(letter))
    soup = BeautifulSoup(resp.text, 'html.parser')
    contents = soup.body.find_all("div", {"class": "content-within"})[0].find_all("a")

    for link in contents:

        pattern = r'^/diseases.*'
        href = link.get('href')
        r = re.compile(pattern)
        match = r.search(href)
        if match:
            links.append(prefix + href )

# print(links)
links_formated = '\n'.join(links)
with open("disease_links.txt", "w") as f:
    f.write(links_formated)


