# Парсер книг с сайта tululu.org
Консольное приложения для скачивания книг и обложек.

### Как установить

#### Скачать

Python3 должен быть уже установлен. Скачать этот репозиторий себе на компьютер.

Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html)
для изоляции проекта.

#### Быстрая настройка venv

Начиная с Python версии 3.3 виртуальное окружение идёт в комплекте в виде модуля
venv. Чтобы его установить и активировать нужно выполнить следующие действия в
командной строке:  

Указать скачанный репозиторий в качестве каталога.
```
cd C:\Users\ваш_пользователь\Downloads\папка_репозитория
```
Установить виртуальное окружение в выбранном каталоге.
```
Python -m venv env
```
В репозитории появится папка виртуального окружения env  

<a href="https://imgbb.com/"><img src="https://i.ibb.co/Hn4C6PD/image.png" alt="image" border="0"></a>

Активировать виртуальное окружение.
```
env\scripts\activate
```
Если всё сделано правильно, вы увидите в командной строке (env) слева от пути 
каталога.  

<a href="https://imgbb.com/"><img src="https://i.ibb.co/MZ72r22/2.png" alt="2" border="0"></a>

#### Установить зависимости

Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки 
зависимостей:

```python
pip install -r requirements.txt
```

### Как использовать

Для запуска программа принимает два обязательных аргумента:
  1. `start_id` - указывает с какой страницы начать скачивание книг
  1. `end_id` - до какой страницы скачивать книги

При запуске скрипта программа проверит, есть ли в корневом каталоге папки
`books` и `images`, создаёт их при необходимости и скачивает в них книги и обложки
соответственно. Пример запуска:

```python
python main.py 20 30
```

#### Ведение логов

Если по какому-то id-страницы книга отсутствует, то программа продолжает скачивание
следующей страницы. Создаётся файл `sample.log`, куда записываются сообщения об
отсутствии страницы с номером id.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).