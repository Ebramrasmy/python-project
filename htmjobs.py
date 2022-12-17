import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
locations_name = []
skills = []
links = []
page_num = 0

while True:
    try:
        # fetch the url
        page = requests.get(f"https://wuzzuf.net/search/jobs/?a=navbg&q=html&start={page_num}")

        # save page content
        content = page.content

        # create soup object to parse content
        soup = BeautifulSoup(content, "html.parser")
        page_limit = int(soup.find("strong").text)
        if (page_num > page_limit // 15):
            print("page ended, terminate")
            break

        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        locations_names = soup.find_all("span", {"class": "css-5wys0k"})
        jop_skills = soup.find_all("div", {"class": "css-y4udm8"})

        # step loop over returned lists to extract needed info into other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            locations_name.append(locations_names[i].text)
            skills.append(jop_skills[i].text)
        # print(job_title, company_name, locations_name, skills)
        page_num += 1
        print("page switched")
    except:
        print("error occurred")
        break

# step create csv file and fill it with values
file_list = [job_title, company_name, locations_name, skills, links]
exported = zip_longest(*file_list)
with open("D:\FCI\Level(3)1\html_jobs.csv", "w") as myfile:
    writer = csv.writer(myfile)
    writer.writerow(["Job title", "Company name", "Locations name", "Skills", "links"])
    writer.writerows(exported)
