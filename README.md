# Сервис бронирования времени на фотосессии (Веб-сервер)

Веб-сервер для работы с сервисом бронирования фотосессий.

Функционал и API в репозитоии: https://github.com/eleneaa/book_photoshoot


## Установка

1. Склонируйте репозиторий:
  ```
git clone https://github.com/eleneaa/book_photoshoot
  ```
  
2. Перейдите в папку проекта:
  ```
cd book_photoshoot
  ```

3. Установите зависимости:
  ```
pip install -r requirements.txt
  ```

4. Примените миграции для настройки базы данных:
  ```
python manage.py migrate
  ```

5. Запустите сервер локально:
  ```
python manage.py runserver
  ```
