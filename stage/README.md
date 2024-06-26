# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)  

[Пример рабочего сайта](https://swar.ga)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить сайт

Сайт запускается в докер. На сервере должен быть установлен и настроен Nginx или другой сервер для переадресации внешнего запроса.
Сервис будет развернут на `8080` порту. 

Скачайте код:
```sh
git clone https://github.com/c-Door-in/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Docker](https://docs.docker.com/engine/install/), если этого ещё не сделали.

Проверьте, что `docker` установлен и корректно настроен. Запустите его в командной строке:
```sh
docker --version
```

### Настроить .env
Создайте файл `.env` в каталоге `star_burger/stage/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```
Для расчета расстояния до ближайшего ресторана нужно получить токен системы геолокации Яндекс. Для этого небходимо зарегистрироваться 
в [разделе разработчиков Яндекс](https://developer.tech.yandex.ru/) 
и подключить API интерфейс "JavaScript API и HTTP Геокодер". Ключ этого интерфейса нужно положить в файл `.env`:
```sh
YANDEX_GEO_APIKEY=<Ваш ключ от API Яндекс геокодер>
```

Для отслеживания выпадающих исключений и других сообщений логгирования 
вы можете подключить систему [Rollbar](https://rollbar.com/). 
Пройдите на сайт и зарегистрируйтесь в системе. 
Среди предложенных SDK выберете Django. На шаге Integrate SDK будет предложена инструкция 
по конфигурации SDK. В предложенных настройках `ROLLBAR` найдите значение `access_token`
```
ROLLBAR = {
    'access_token': 'some_token',
    ...
}
```
Cкопируйте его в файл переменных окружения `.env`, присвоив переменной `DJANGO_ROLLBAR_TOKEN`. В последующем этот токен можно найти в настройках проекта `Project Access Tokens` как `post_server_item`. Также укажите текущую стадию разработки 
`ROLLBAR_ENVIRONMENT=development` или другую, отражающую вашу стадию:
```sh
DJANGO_ROLLBAR_TOKEN='your_rollbar_token'

ROLLBAR_ENVIRONMENT=stage
```

Остальные переменные:
```
DEBUG=True

ALLOWED_HOSTS — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)

База данных поднимается в контейнере. Нужно только определить, какие будут название, имя пользователя и пароль.
POSTGRES_DB - название базы данных
POSTGRES_USER - имя пользователя
POSTGRES_PASSWORD - пароль
```

### Настроить Nginx
Настройте nginx, используя как шаблон файл `nginx-default` в директории `star_burger/stage/`

### Запустить Docker Compose
Запустите команду:
```sh
docker compose up --build
```

## Быстрый деплой

После настройки Nginx и .env запустите скрипт `deploy-docker-star-burger.sh`. 
Чтобы файл сделать исполняемым, выполните:
```sh
sudo chmod u+x deploy-docker-star-burger.sh
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:


- Второй и третий урок [учебного модуля Django](https://dvmn.org/modules/django/)
