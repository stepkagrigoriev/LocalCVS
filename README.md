# LocalCVS

## Описание
LocalCVS — это простая локальная система контроля версий, очень похожая на известный всем Git

- Инициализировать репозиторий (`init`)
- Добавлять файлы в буферную зону (`add`)
- Создавать коммиты с сообщениями (`commit`)
- Просматривать историю коммитов (`log`)
- Откатываться к предыдущим коммитам (`reset`)

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