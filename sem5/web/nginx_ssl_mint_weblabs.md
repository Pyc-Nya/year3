# Настройка nginx с SSL для проекта web_labs на Linux Mint

## 1. Установка nginx

```bash
sudo apt update
sudo apt install nginx
```

## 2. Создание самоподписанного SSL сертификата

```bash
# Создание директории для сертификатов
sudo mkdir -p /etc/nginx/ssl

# Генерация самоподписанного сертификата
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/selfsigned.key \
    -out /etc/nginx/ssl/selfsigned.crt
```

При запросе данных для сертификата указать:
- Country Name: RU
- State: Moscow  
- City: Moscow
- Organization Name: можно оставить пустым
- Organizational Unit Name: можно оставить пустым
- Common Name: **localhost** (обязательно!)
- Email Address: можно оставить пустым

## 3. Создание конфигурации nginx

```bash
sudo nano /etc/nginx/sites-available/web_labs
```

Содержимое файла конфигурации:

```nginx
server {
    listen 8001 ssl;
    server_name localhost;

    ssl_certificate /etc/nginx/ssl/selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/selfsigned.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 4. Активация конфигурации

```bash
# Создание символической ссылки
sudo ln -s /etc/nginx/sites-available/web_labs /etc/nginx/sites-enabled/

# Удаление конфигурации по умолчанию
sudo rm /etc/nginx/sites-enabled/default

# Проверка синтаксиса конфигурации
sudo nginx -t
```

## 5. Запуск nginx

```bash
# Запуск службы nginx
sudo systemctl start nginx

# Включение автозапуска при загрузке системы
sudo systemctl enable nginx

# Перезагрузка конфигурации
sudo systemctl reload nginx

# Проверка статуса службы
sudo systemctl status nginx
```

## 6. Запуск Express сервера

```bash
# Переход в директорию проекта
cd /path/to/web_labs

# Запуск Node.js приложения
node server.js
```

## 7. Проверка работы

Проверка портов:
```bash
sudo netstat -tlnp | grep nginx
sudo netstat -tlnp | grep 8000
```

Доступ к приложению:
- HTTPS через nginx: `https://localhost:8001`
- HTTP напрямую к Express: `http://localhost:8000`

## 8. Команды для отладки

```bash
# Просмотр логов ошибок nginx
sudo tail -f /var/log/nginx/error.log

# Просмотр логов доступа nginx
sudo tail -f /var/log/nginx/access.log

# Перезапуск nginx
sudo systemctl restart nginx

# Остановка nginx
sudo systemctl stop nginx

# Проверка активных конфигураций
ls -la /etc/nginx/sites-enabled/
```

## Результат

После выполнения всех шагов веб-приложение web_labs доступно по адресу `https://localhost:8001` с SSL-шифрованием через nginx, который проксирует запросы к Express серверу на порту 8000.