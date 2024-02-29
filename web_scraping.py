import requests
from bs4 import BeautifulSoup as bs
import csv

page = requests.get("https://codeforces.com/problemset/page/1?tags=600-2000")
code = page.content
cont = bs(code,"lxml")

# extract table of problems on codeforces
table_of_problems = cont.find("table", {"class": "problems"})
problems = table_of_problems.find_all("tr")
problems_list = []

# each problem consists of <td> that have the problem details which { second -> name and tags
#                                                                     fourth -> difficulty }
# another <td>s include elements that I don't need them

for i in range(1, len(problems)):
    problem_details = problems[i].find_all('td')
    # second <td>
    divs_of_problem = problem_details[1].find_all("div")
    # name
    problem_name = divs_of_problem[0].find('a').get_text().strip()
    # tags
    problem_tags = divs_of_problem[1].find_all('a')
    tags = []
    for tag in problem_tags:
        tags.append(tag.get_text().strip())
    # fourth <td>
    problem_diff = problem_details[3].span.get_text().strip()

    problems_list.append({'name': problem_name, 'tags': tags, 'difficulty': problem_diff})

keys = problems_list[0].keys()
file = open('project1.csv', 'w')
dict_writers = csv.DictWriter(file, keys)
dict_writers.writeheader()
dict_writers.writerows(problems_list)


