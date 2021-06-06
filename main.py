import os
import logging
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_book_link(book_id):
    url = f'https://tululu.org/txt.php'
    payload = {'id': book_id}
    response = requests.get(url, params=payload)
    check_for_redirect(response)
    book_link = response.url
    return book_link


def check_for_redirect(response):
    history_of_redirects = response.history
    if history_of_redirects:
        raise requests.HTTPError


def parse_book_page(book_id):
    book_page_link = f'https://tululu.org/b{book_id}'
    response = requests.get(book_page_link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title = title_tag.text.split('::')
    book_name = title[0].strip()
    author = title[1].strip()
    book_page_information = {
        'book_name': book_name,
        'author': author
    }
    return book_page_information


def download_txt(book_id, book_link, book_page_info, folder='books/'):
    clean_filename = sanitize_filename(book_page_info['book_name'])
    book_path = os.path.join(folder, f'{book_id}. {clean_filename}.txt')
    os.makedirs(folder, exist_ok=True)
    response = requests.get(book_link)
    response.raise_for_status()
    with open(book_path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    logging.basicConfig(filename='sample.log', filemode='w',
                        format='%(filename)s - %(levelname)s - %(message)s',
                        level=logging.ERROR)

    for book_id in range(1, 11):
        try:
            book_link = get_book_link(book_id)
            book_page_info = parse_book_page(book_id)
            download_txt(book_id, book_link, book_page_info)
        except requests.HTTPError:
            logging.error(f'Книги с id № {book_id} не существует')
            continue
