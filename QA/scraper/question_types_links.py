from bs4 import BeautifulSoup
import requests as req
import re

"""
Get all Question Types
"""

links = []
prefix = "https://www.webmd.com"

resp = req.get("https://www.webmd.com/a-to-z-guides/qa")
soup = BeautifulSoup(resp.text, 'html.parser')
contents = soup.body.find_all("ul", {"class": "channel-list"})[0].find_all("a")
contents = contents[1:]
for link in contents:
    href = link.get('href')
    links.append(prefix + href )

links_formated = '\n'.join(links)
with open("question_type_links.txt", "w") as f:
    f.write(links_formated)


