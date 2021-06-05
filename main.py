import os
import logging
import requests
from urllib.parse import urlsplit


def get_book_id(book_url):
    splitted_url = urlsplit(book_url)
    book_id = splitted_url.query.replace('id=', '')
    return book_id


def check_for_redirect(response):
    redirects = response.history
    if redirects:
        raise requests.HTTPError


def get_book_link():
    books_urls = []
    for i in range(1, 11):
        url = f'https://tululu.org/txt.php?id={i}'
        books_urls.append(url)
    return books_urls


def download_book(book_id, directory):
    url = f'https://tululu.org/txt.php'
    payload = {
        'id': book_id
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    filename = f'{book_id}.txt'
    with open(f'{directory}{filename}', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    logging.basicConfig(filename='sample.log', filemode='w',
                        format='%(filename)s - %(levelname)s - %(message)s',
                        level=logging.ERROR)

    directory = f'{os.getcwd()}/books/'
    os.makedirs(directory, exist_ok=True)

    books_links = get_book_link()

    for book_link in books_links:
        try:
            book_id = get_book_id(book_link)
            download_book(book_id, directory)
        except requests.HTTPError:
            logging.error('Данного id не существует')
            continue

