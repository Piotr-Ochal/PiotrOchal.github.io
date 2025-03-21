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

for i, elem in enumerate(myListElements):
    time.sleep(2)

    prevName = myListElements[i-1] if i > 0 else ""
    nextName = myListElements[i+1] if i+1 < len(myListElements) else ""
    prevUrl = prevName.replace(" ","") + ".md"
    nextUrl = nextName.replace(" ","") + ".md"

    print(f'doing {elem}')

    if '\'' in elem:
        continue
    
    newFile = elem.replace(" ","") + ".md"
    markdown_page += f'{str(i+1)}. [{elem}]({newFile})\n'
    
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
        body = f'\n### {result["body"]}  [Read More]({result["href"]})'
        
    markdown_addition += body
    markdown_addition += "\n\n"
    if i>0:
        markdown_addition += f'|[<- {prevName}]({prevUrl})'
    else:
        markdown_addition += f'|     '
    markdown_addition += "|[Return To Main Page](index.md)|"
    if i+1 < len(myListElements):
        markdown_addition += f'[{nextName} ->]({nextUrl})|'
    else: 
        markdown_addition += f'     |'

    markdown_addition += '\n|:----|:---:|----:|'

    with open(newFile, "w", encoding="utf-8") as f:
        f.write(markdown_addition)

mylinks = soup.find_all("a")
link = None
for elem in mylinks:
    if '#' not in elem.get("href"):
        link = elem.get("href")
        break

markdown_page += f'\n\n[Original Page]({link})'

with open("index.md", "w", encoding="utf-8") as f:
    f.write(markdown_page)