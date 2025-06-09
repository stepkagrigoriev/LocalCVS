# LocalCVS

## Описание
LocalCVS — это простая локальная система контроля версий, очень похожая на известный всем Git

- Инициализировать репозиторий (`init`)
- Добавлять файлы в буферную зону (`add`)
- Создавать коммиты с сообщениями (`commit`)
- Просматривать историю коммитов (`log`)
- Откатываться к предыдущим коммитам (`reset`)
- Создавать и работать с тэками (`tag`)

---

## Установка и использование
!!! Система позволяет объявить только один репозиторий, который лежит в директории вместе с клонированным LocalCVS

Клонируем репозиторий
```shell
git clone https://github.com/stepkagrigoriev/LocalCVS.git
```
Поддерживаемые команды:
```shell
# Инициализация репозитория в корневой папке
python -m LocalCVS init .

# Добавление файлов в buffer
python -m LocalCVS add file1.txt file2.txt

# Создание коммита с сообщением
python -m LocalCVS commit -m "Initial commit"

# Просмотр истории коммитов
python -m LocalCVS log

# Откат к предыдущему коммиту (SHA взят случайный)
python -m LocalCVS reset abcdefgh0123456789

# Работа с тэгами (SHA взят случайный)
python -m LovalCVS tag v1.0 abcdefgh0123456789
python -m LocalCVS tag v1.0 # ставит тэг на указатель HEAD
python -m LocalCVS tag -d v1.0
python -m LovalCVS tag #посмотреть все тэги и коммиты, привязанные к ним
```
---
## Тестирование
```shell
# Перейдем в директорию проекта
cd LocalCVS 

# Запустим модульные тесты
python -m unittest discover Tests
```
## Автор - Григорьев Степан [stepkagrigoriev](https://github.com/stepkagrigoriev)

## Материалы: https://code-handbook.vercel.app/fundamentals/version-control-systems https://habr.com/ru/articles/313890/
