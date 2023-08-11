import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from time import sleep


def send(text, img_link):
    load_dotenv()
    bot_token = os.getenv('token')
    chat_id = os.getenv('id')
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    data = {'chat_id': chat_id, 'caption': text, 'photo': img_link}
    requests.post(url, json=data)


def scraping():
    url_news = 'https://coop-land.ru/news/'
    response = requests.get(url_news)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="html.parser")
    headline = soup.find('h2').text
    img = soup.find('a', class_='img').find('img')['data-src'].replace('/', '', 1)
    final_img = url_news + img
    final_img = final_img.replace('news/', '', 1)
    preview = soup.find('div', class_='preview-text').text.strip()
    main_link = soup.find('a', class_='big-link')['href']
    return headline, preview, final_img, main_link


def main():
    while True:
        headline, preview, main_link, final_img = scraping()
        formated_post = f'{headline}\n\n' \
                        f'{preview}\n\n' \
                        f'Ссылка на источник: {main_link}'

        send(formated_post, final_img)
        sleep(18000)


if __name__ == '__main__':
    main()