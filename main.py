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
    markdown_page += f'{str(i)}. {elem.text} \n'
    print(elem.text)
    i+=1


with open("2025-03-14-Chess-Openings.md", "w", encoding="utf-8") as f:
    f.write(markdown_page)