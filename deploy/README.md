# В данной директории все необходимое для развертывания СУБД и сервисов

# Содержание
1. [Запуск](#запуск)
2. [Остановка](#остановка)
3. [MongoDB](#mongodb)
4. [PostgreSQL](#postgresql)
5. [MySQL](#mysql)
6. [Memcached](#memcached)
7. [SybaseIQ](#sybaseiq)

# Запуск
```bash
docker-compose -p home-automation up -d
```
## Проверка статусов сервисов

```bash
docker ps --all --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

# Остановка
```bash
docker-compose stop
```

# MongoDB

За развертывание MongoDB отвечает следующая часть compose-файла:

```bash
volumes:
  mongo-data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: ./mongo/data
services:
  mongo:
    image: mongo:6.0
    volumes:
      - mongo-data:/data/db
      - ./mongo/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js
    ports:
      - "27017:27017"
      - "27018:27018"
      - "27019:27019"
    environment:
      - MONGO_INITDB_DATABASE=home-automation
```

В нем:
- Создается диск (volume) с названием **mongo-data**, для хранения данных используется директория ./mongo/data. Рекомендуется добавить директорию в gitignore:

```bash
deploy/mongo/data/*
!deploy/mongo/data/.gitkeep
```
- Создается контейнер **mongo** на базе образа mongo:6.0
- К контейнеру монтируется volume **mongo**
- К контейнеру монтируется файл-конфигурации **init-mongo.js**
- Пробрасываются порты, Mongo будет доступна по {MACHINE_IP}:27017, например: 192.168.1.50:27017.
Для подключения можно использовать строку:
```bash
mongodb://home-automation:home-automation@192.168.1.50:27017/?directConnection=true&authMechanism=DEFAULT&authSource=home-automation
```
- Через переменную окружения дается название первичной базе данных:
```bash
MONGO_INITDB_DATABASE=home-automation
```

Также в развертывание используется файл **init-mongo.js**:
```bash
db.createUser(
    {
        user    : "home-automation",
        pwd     : "home-automation",
        roles   : [
            {
                role: "readWrite",
                db  : "home-automation"
            }
        ]    
    }
)
```

В нем создается пользователь с паролем и назначаются привелегии на запись в базу данных

Для тестирования подключения можно использовать MongoDB Atlas или любой другой GUI-клиент

## [Образ на Docker-хабе](https://hub.docker.com/_/mongo)
---

# PostgreSQL

За развертывание PostgreSQL отвечает следующая часть compose-файла:

```bash
volumes:
  postgresql-data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: ./postgresql/data
services:
  postgresql:
    image: postgres:12
    volumes:
      - postgresql-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: home-automation
      POSTGRES_USER: home-automation
      POSTGRES_DB: home-automation
      PGDATA: /var/lib/postgresql/data/db-files/
    ports:
      - 5432:5432
```

В нем:

- Создается диск (volume) с названием **postgresql-data**, для хранения данных используется директория ./postgresql/data. Рекомендуется добавить директорию в gitignore:

```bash
deploy/postgresql/data/*
!deploy/postgresql/data/.gitkeep
```
- Создается контейнер **postgresql** на базе образа postgres:12
- К контейнеру монтируется volume **postgresql-data**
- Пробрасываются порты, PostreSQL будет доступен по {MACHINE_IP}:5432, например: 192.168.1.50:5432.
- Через переменные окружения задается пользователь, название первичной базы данных и директория хранения данных внутри контейнера:
```bash
POSTGRES_PASSWORD: home-automation
POSTGRES_USER: home-automation
POSTGRES_DB: home-automation
PGDATA: /var/lib/postgresql/data/db-files/
```

Для тестирования подключения можно использовать утилиту psql или какой-либо GUI-клиент

## [Образ на Docker-хабе](https://hub.docker.com/_/postgres)
---

# MySQL

За развертывание MySQL отвечает следующая часть compose-файла:

```bash
volumes:
  mysql-data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: ./mysql/data
services:
  mysql:
    image: mysql:8
    command: --default-authentication-plugin=mysql_native_password
    volumes:
      - mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"
    environment:
      MYSQL_RANDOM_ROOT_PASSWORD: 'yes'
      MYSQL_USER: home-automation
      MYSQL_PASSWORD: home-automation
      MYSQL_DATABASE: home-automation
```

В нем:

- Создается диск (volume) с названием **mysql-data**, для хранения данных используется директория ./mysql/data. Рекомендуется добавить директорию в gitignore:

```bash
deploy/mysql/data/*
!deploy/mysql/data/.gitkeep
```
- Создается контейнер **mysql** на базе образа mysql:8
- К контейнеру монтируется volume **mysql-data**
- Пробрасываются порты, MySQL будет доступен по {MACHINE_IP}:3306, например: 192.168.1.50:3306.
- Через переменные окружения задается пользователь, название первичной базы данных:
```bash
MYSQL_RANDOM_ROOT_PASSWORD: 'yes'
MYSQL_USER: home-automation
MYSQL_PASSWORD: home-automation
MYSQL_DATABASE: home-automation
```

Для тестирования подключения можно использовать утилиту mysql или какой-либо GUI-клиент
## [Образ на Docker-хабе](https://hub.docker.com/_/mysql)

# Memcached

За развертывание Memcached отвечает следующая часть compose-файла:

```bash
memcached:
  image: memcached:1.6.17
  ports:
      - "11211:11211"
  command: ["memcached"]
```

В нем:

- Создается контейнер **memcached** на базе образа memcached:1.6.17
- Пробрасываются порты, Memcached будет доступен по {MACHINE_IP}:11211, например: 192.168.1.50:11211.

Протестировать подключение можно прямо из Python:

```bash
>>> from pymemcache.client import base
>>> client = base.Client(('192.168.1.50', 11211))
>>> client.set('some_key', 'some value')
True
>>> client.get('some_key')
b'some value'
```
## [Образ на Docker-хабе](https://hub.docker.com/_/memcached)

# SybaseIQ