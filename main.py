from bs4 import BeautifulSoup
import requests

url = "https://chessfox.com/chess-openings-list/"
response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")

list = soup.find("ol")

markdown_page = f'---\ntitle: Chess Openings\nauthor: cotes\ndate: 2025-03-14 00:30:00 +0800\ncategories: [Blogging, Tutorial]\n'
markdown_page += f'tags: [favicon]\n---\n# Chess Openings\n'
i = 1
for elem in list:
    markdown_page += f'{str(i)}. {elem.text}\n'
    i+=1

mylinks = soup.find_all("a")
link = None
for elem in mylinks:
    if '#' not in elem.get("href"):
        link = elem.get("href")
        break

markdown_page += f'[random link]({link})'

with open("index.md", "w", encoding="utf-8") as f:
    f.write(markdown_page)
