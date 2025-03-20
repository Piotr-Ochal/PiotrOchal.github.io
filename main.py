from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import requests
import time

url = "https://chessfox.com/chess-openings-list/"
response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")

list = soup.find("ol")

markdown_page = f'---\ntitle: Chess Openings\nauthor: cotes\n' + f'date: 2025-03-14 00:30:00 +0800\n---\n# Chess Openings\n'

i = 1
for elem in list:
    if i>10:
        break
    time.sleep(2)
    if '\'' in elem.text:
        continue
    newFile = elem.text.replace(" ","") + ".md"
    markdown_page += f'[{str(i)}. {elem.text}]({newFile})\n'
    
    markdown_addition = f'# {elem.text}\n'
    query = f'{elem.text} description'
    results = DDGS().text(
        keywords=query,
        region='wt-wt',
        safesearch='off',
        timelimit='7d',
        max_results=1,
    )
    
    # Selecting and adding the description and link for a result found to markdown file
    body = ""
    for result in results:
        body = f'\n### {result["body"]}\n[Read more]({result["href"]})'
        
    markdown_addition += body
    markdown_addition += "\n\n[Main Page](index.md)"
    with open(newFile, "w", encoding="utf-8") as f:
        f.write(markdown_addition)
    i+=1

mylinks = soup.find_all("a")
link = None
for elem in mylinks:
    if '#' not in elem.get("href"):
        link = elem.get("href")
        break

markdown_page += f'\n\n[original page]({link})'

with open("index.md", "w", encoding="utf-8") as f:
    f.write(markdown_page)