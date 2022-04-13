# Инициализация

```shell
python -m pip install pipenv
```
Из рабочей директории
```shell
pipenv sync
```

# Запуск

Из рабочей директории  
Windows:
```shell
run
```
POSIX:
```shell
./run.sh
```

# Ресурсы

* `resources/notify.mp3` - звук нотификации о новом
* `resources/urls.txt` - ссылки для парсинга. В ссылке обязательно должно быть `q=...` (что-то введено в поле поиска).
Каждая ссылка с новой строки, пустые строки игнорируются
* `resources/public.pem` - открытый сертифкат localhost proxy сервера при использовании
