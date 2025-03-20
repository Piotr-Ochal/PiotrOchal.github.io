from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import requests
import time

url = "https://chessfox.com/chess-openings-list/"
response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")

list = soup.find("ol")

markdown_page = f'---\ntitle: Chess Openings\nauthor: cotes\n' + f'date: 2025-03-14 00:30:00 +0800\n---\n# Chess Openings\n'

myListElements = []
for elem in list:
    myListElements.append(elem.text)
myListElements.sort()

i = 1
for elem in myListElements:
    time.sleep(2)
    if '\'' in elem:
        continue
    
    newFile = elem.replace(" ","") + ".md"
    markdown_page += f'{str(i)}. [{elem}]({newFile})\n'
    
    markdown_addition = f'# {elem}\n'
    query = f'{elem} description'
    results = DDGS().text(
        keywords=query,
        region='wt-wt',
        safesearch='off',
        timelimit='7d',
        max_results=1,
    )
    
    body = ""
    for result in results:
        body = f'\n### {result["body"]}\n[Read More]({result["href"]})'
        
    markdown_addition += body
    markdown_addition += "\n\n[Return To Main Page](index.md)"
    with open(newFile, "w", encoding="utf-8") as f:
        f.write(markdown_addition)
    i+=1

mylinks = soup.find_all("a")
link = None
for elem in mylinks:
    if '#' not in elem.get("href"):
        link = elem.get("href")
        break

markdown_page += f'\n\n[Original Page]({link})'

with open("index.md", "w", encoding="utf-8") as f:
    f.write(markdown_page)