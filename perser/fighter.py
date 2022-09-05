import requests
from bs4 import BeautifulSoup

URL = "https://rezka.ag/"

HEADERS = {
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def get_html(url, params=''):
    reg = requests.get(url, headers=HEADERS, params=params)
    return reg

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="b-content__inline_item")
    fighter = []
    for item in items:
        desc =  item.find("div",  class_="b-content__inline_item-link").find("div").getText().split(', ')
        fighter.append({
            "title": item.find("div",class_="b-content__inline_item-link").find("a").getText(),
            "year": desc[0],
            "city":desc[1],
            "genre": desc[2],
            "link": item.find("div", class_="b-content__inline_item-link").find("a").get("href")
        })
    return fighter

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        answer = []
        for page in range(1, 2):
            html = get_html(f"{URL}page/{page}/")
            answer.extend(get_data(html.text))
        return answer
    else:
        raise Exception("Error in parser!")