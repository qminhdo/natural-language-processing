from bs4 import BeautifulSoup
import requests as req
from requests_html import HTMLSession
import re
import time

"""
Get the disease contents from all links
Include symtoms and casues
diagnosis and treatment

Sample:
prefix = https://www.drugs.com/


"""


def get_content(link):
    contents = ""
    resp = req.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.body.find_all("div", {"class": "contentBox"})[0]
    text_arr = content.find_all(text=True)


    for text in text_arr:
        if len(text) > 2:
            contents += text

    return contents

prefix = "https://www.mayoclinic.org"

index = 0
# loop over all links in file
with open("./drugs_links.txt", 'r', encoding='utf-8') as f:
    # line = "https://www.drugs.com/mtm/anastrozole.html"
    for line in f:
        contents = ""
        link = line.strip()
        print(link)

        try:
            contents += get_content(link)
        except Exception as e:
            print("Unable to process", link)

        if contents:
            r = re.compile(r'.*\/(?P<name>.*)\.html$', re.IGNORECASE)
            match = r.search(link)
            if match:
                filename = match.groupdict().get('name')
                with (open("../data/assorted/{}-drugs-{}.txt".format(index,filename), 'w', encoding='utf-8')) as f:
                    f.write(contents)

            index += 1
