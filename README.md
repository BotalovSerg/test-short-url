## HTTP-сервис, для обрабатывает входящих запросов
Команды для сборки образа и запуска сервиса
```
docker build -t url-shortener .
docker run -p 8080:8080 url-shortener
```