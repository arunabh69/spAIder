
from datetime import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

root = 'https://nicepage.com'
link1 = []

for i in range(1, 41):
    url = 'https://nicepage.com/html-templates?page={}'.format(i)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'lxml')

    for link in soup.findAll('a', class_="thumbnail"):
        x = link.get('style')

        y = re.findall('[0-9]+', x)
        ans = int(y[1])
        print(ans)
        if ans <= 200:
            link1.append(link.get('href'))
        print(link1)
        print(len(link1))

link2 = []
for links in link1:
    req = requests.get(f'{root}{links}')
    content = req.text
    soup = BeautifulSoup(content, "lxml")
    box = soup.find('a', class_="demo-link")
    link2.append(box.get('href'))

print(link2)

final = []
for links in link2:
    req = requests.get(f'{root}{links}')
    content = req.text
    soup = BeautifulSoup(content, "lxml")
    box = soup.find('iframe')
    final.append(box.get('src'))
print(final)

# dict = {'LINKS': final}
# 
# df = pd.DataFrame(dict)
# df.to_csv('dataset.csv')
