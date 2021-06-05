import os
import requests
from urllib.parse import urlsplit


def get_filename(book_url):
    splitted_url = urlsplit(book_url)
    book_id = splitted_url.query.replace('id=', '')
    return book_id


def download_book(book_url, book_id):
    response = requests.get(book_url)
    response.raise_for_status()
    filename = f'{book_id}.txt'
    with open(f'{directory}{filename}', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    url_sheet = []
    for i in range(1, 11):
        url = f'https://tululu.org/txt.php?id={i}'
        url_sheet.append(url)

    directory = f'{os.getcwd()}/books/'
    os.makedirs(directory, exist_ok=True)

    for book_url in url_sheet:
        book_id = get_filename(book_url)
        download_book(book_url, book_id)
