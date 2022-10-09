# В данной директории все необходимое для развертывания СУБД и сервисов


# Запуск
```bash
docker-compose up -d
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