import requests
from bs4 import BeautifulSoup
from time import time, sleep


def get_posts():
    """Возвращает список новостей"""
    link = 'https://lenta.ru/parts/news/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/100.0.4896.75 Safari/537.36'}
    resp = requests.get(link, headers=headers).text
    # with open('text.txt', 'r', encoding='UTF-8') as file:
    #     resp = file.read()
    soup = BeautifulSoup(resp, 'lxml')
    # создаем список со всеми li
    list_news: list[BeautifulSoup] = soup.find_all(class_='parts-page__item')
    # создаем список, который будем наполнять новостями
    final_list = []
    for item in list_news:
        href = item.find('a').get('href')
        if href[0] != '/':
            continue
        try:
            title = item.find('h3').text
        except:
            continue
        final_list.append({'title': title, 'href': 'https://lenta.ru' + href})
    return final_list


def send_message(text: str):
    """Создает новое сообщение в Discord"""
    link = 'https://discord.com/api/v9/channels/949692477248524388/messages'
    header = {
        'authorization': TOKEN,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.75 Safari/537.36'}
    data = {'content': text, 'nonce': str(int(time())), 'tts': False}
    requests.post(link, headers=header, json=data)


def show_news():
    """Проверяет новости и если есть новые отправляет сообщение в Discord"""
    last_news = get_posts()[0]
    while True:
        sleep(20)
        news = get_posts()[0]
        if last_news != news:
            show_text = "Новая новость! \n{} {}".format(news['title'], news['href'])
            send_message(show_text)
            last_news = news


if __name__ == "__main__":
    with open('config.txt', 'r', encoding='UTF-8') as file:
        TOKEN = file.read().strip()
    show_news()

