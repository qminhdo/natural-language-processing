from bs4 import BeautifulSoup
import requests as req
import re

"""
Get all questions
"""

questions = []
prefix = "https://www.drugs.com"

with open("./question_type_links.txt", 'r', encoding='utf8') as f:
    for line in f:
        link = line.strip()
        print("Link", link)
        for i in range(1,30):
            page = "{}?pg={}".format(link,i)
            # print("page", page)
            page = "https://www.webmd.com/add-adhd/qa/default.htm?pg=1"

            try:
                resp = req.get(page)
                soup = BeautifulSoup(resp.text, 'html.parser')
                contents = soup.body.find_all("ul", {"class": "main-indexList-ul"})[0].find_all("a")
                for link_ in contents:
                    if (link_.string):
                        href = link_.string
                        questions.append(href)
            except:
                print("uable to process")

questions_formated = '\n'.join(questions)
with open("../data/ENTY_dismed.txt", "w") as f:
    f.write(questions_formated)


