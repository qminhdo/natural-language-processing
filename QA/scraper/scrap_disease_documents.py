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
prefix = https://www.mayoclinic.org

Disease link for symptom and causes: /diseases-conditions/petit-mal-seizure/symptoms-causes/syc-20359683
Disease link for diagnosis and treatment: have to get when scraping
"""


def get_dt_content(link):
    resp = req.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    menu_links = soup.find(id="access-nav").find_all('a')

    for ml in menu_links:
        r = re.compile(r'(treatment)', re.IGNORECASE)
        if r.search(ml.string):
            dt_href = ml.get('href')
            if dt_href:
                link_dt = (prefix + dt_href).strip()
                print(link_dt)

            # get content from diagnose and treatment
            resp = req.get(link_dt)
            soup = BeautifulSoup(resp.text, 'html.parser')

    all_h2 = soup.find_all("h2")
    for h2 in all_h2:
        r = re.compile(r'(diagnosis|treatment)', re.IGNORECASE)
        if r.search(h2.string):
            return get_content(h2.parent)


def get_sc_content(link):
    resp = req.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')

    all_h2 = soup.find_all("h2")
    for h2 in all_h2:
        r = re.compile(r'(overview)', re.IGNORECASE)
        if r.search(h2.string):
            return get_content(h2.parent)


def get_content(content):
    contents = ""

    for tag in content.children:
        # check if next sibling is a list
        if tag.name != None:
            if tag.name == "p":
                if tag.string:
                    contents += tag.string + "\n"

            if tag.name == "ul":
                all_li = tag.find_all("li")
                # print('=======', tag.name)
                tmp_contents = ""
                for li in all_li:
                    # print('===', li.name)
                    for child in li.descendants:
                        # The only child in li
                        if child.name == None:
                            tmp_contents += "{} , ".format(child)
                        else:
                            for child in child.descendants:
                                if child.name == None:
                                    tmp_contents += "{} , ".format(child)

                tmp_contents = re.sub('\.', ' ', tmp_contents)
                tmp_contents = re.sub('\s\s', '', tmp_contents)


                contents += tmp_contents + " . \n"
    # print("==============================")
    # print(contents)
    return contents


links = []
prefix = "https://www.mayoclinic.org"



index = 0
# loop over all links in file
with open("./disease_links.txt", 'r', encoding='utf-8') as f:
    for line in f:
        # line = "https://www.mayoclinic.org/diseases-conditions/shellfish-allergy/symptoms-causes/syc-20377503"
        contents = ""
        link = line.strip()
        print(link)

        try:
            # get content from symptom and causes
            contents += get_sc_content(link)
        except Exception as e:
            print("Unable to process", link)

        # Try to find if there are links for diagnose and treatment
        try:
            contents += get_dt_content(link)
        except Exception as e:
            print("Unable to process", link)


        if contents:
            r = re.compile(r'^.*\/diseases-conditions\/(?P<name>.*)\/symptoms-causes.*',re.IGNORECASE)
            match = r.search(link)
            if match:
                filename = match.groupdict().get('name')

            with (open("../data/assorted/{}-disease-{}.txt".format(index, filename), 'w', encoding='utf-8')) as f:
                f.write(contents)

            index += 1