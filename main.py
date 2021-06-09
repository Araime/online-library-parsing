import os
import logging
import requests
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


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
        raise requests.HTTPError(history_of_redirects)


def parse_book_page(book_id):
    book_page_link = f'https://tululu.org/b{book_id}'
    response = requests.get(book_page_link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title = title_tag.text.split('::')
    book_name = title[0].strip()
    author = title[1].strip()
    img = soup.find(class_='bookimage').find('img')['src']
    img_link = urljoin('https://tululu.org', img)
    comments_tags = soup.find_all('div', class_='texts')
    comments = [comment.span.text for comment in comments_tags]
    genre_tag = soup.find('span', class_='d_book').find_all('a')
    all_genres = [genre.text for genre in genre_tag]
    book_page_information = {
        'book_name': book_name,
        'author': author,
        'img_link': img_link,
        'comments': comments,
        'genre': all_genres
    }
    return book_page_information


def download_txt(book_id, book_link, book_page_info, folder='books'):
    clean_filename = sanitize_filename(book_page_info['book_name'])
    book_path = os.path.join(folder, f'{book_id}. {clean_filename}.txt')
    os.makedirs(folder, exist_ok=True)
    response = requests.get(book_link)
    response.raise_for_status()
    with open(book_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_image(book_page_info, folder='images'):
    url = book_page_info['img_link']
    img_name = url.split('/')[-1]
    img_path = os.path.join(folder, img_name)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(img_path, 'wb') as file:
        file.write(response.content)


def get_args():
    parser = argparse.ArgumentParser(description='Программа для скачивания книги и обложки к ней')
    parser.add_argument('start_id', help='С какой страницы скачивать книги', type=int, default=1)
    parser.add_argument('end_id', help='По какую страницу скачивать книги', type=int, default=11)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    logging.basicConfig(filename='sample.log', filemode='w',
                        format='%(filename)s - %(levelname)s - %(message)s',
                        level=logging.ERROR)

    for book_id in tqdm(range(args.start_id, args.end_id), ncols=100):
        try:
            book_link = get_book_link(book_id)
            book_page_info = parse_book_page(book_id)
            download_txt(book_id, book_link, book_page_info)
            download_image(book_page_info)
        except requests.HTTPError:
            logging.error(f'Книги с id № {book_id} не существует')
            continue
