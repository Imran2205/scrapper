import requests
from bs4 import BeautifulSoup

url = 'https://www.fiercewireless.com/'
reqs = requests.get(url)
print(reqs)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    print(link.get('href'))

with open('fiercewireless_all_urls.txt', 'w') as f:
    f.write("\n".join(urls))
