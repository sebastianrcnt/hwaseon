from bs4 import BeautifulSoup
import requests

response = requests.get("https://cafe.naver.com/ca-fe/home/search/combinations?q=가상화폐")

print(response.text)