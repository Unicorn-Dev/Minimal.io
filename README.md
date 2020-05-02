# Сдача
## Часть 2
Добавленно:
1. Паттерн Деоратор static_vars (361 стр system/game_funktions.py) для счетчика тиков игры, чтобы регулировать чатоту обновления картинки (она обновляется реже, не на каждый основной цикл), благодаря чему экономится вычислительная мощность (обновление экрана доволно затратная операция)
1. Паттерн Фасад (в файле system/engine.py)

# Игра Minimal.io
Это кроссплатформенная игра Minimal.io. При создании авторов вдохновила игра SuperBlust. В качастве базового каркаса игры была взята игра alliens invasion из учебника Python Crash Course a hands-on, Project-Based Introduction to Programming by Eric Matthes.  
На данный момент есть реализация игры на Python (для сольной игры и игры с партнером).

## В стадии разработки

Проект находится на стадии бета-тестирования. Есть много недочётов, которые мы постараемся исправить. Можно играть аккуратным образом.

В дальнейшем игра будет развиваться в кросс-платформенном режиме (desktop-версии версии) и возможно появится возможность игры с двумя играками по онлайну.

## Архитектура программы
### UML
1. Классовая UML-диаграмма программа доступна [в данном репозитории](https://github.com/Unicorn-Dev/Minimal.io/blob/new_ver_dev/UML_Diagrams/Class.png) и [на данном сайте](https://www.lucidchart.com/documents/edit/079d5591-6cf0-497f-a332-7f91954b2154/0_0?shared=true#?folder_id=home&browser=icon).
1. Sequence UML-диаграмма программа доступна [в данном репозитории](https://github.com/Unicorn-Dev/Minimal.io/blob/new_ver_dev/UML_Diagrams/Sequence.png) и [на данном сайте](https://www.lucidchart.com/documents/edit/aca299c7-8387-4648-a8f0-25f96f441537/0_0?beaconFlowId=C25EA2C93E844225).
1. Use Case UML-диаграмма программа доступна [в данном репозитории](https://github.com/Unicorn-Dev/Minimal.io/blob/new_ver_dev/UML_Diagrams/UseCase.png) и [на данном сайте](https://www.lucidchart.com/documents/edit/e01f34aa-e097-4f86-8c6b-b8877d6c8307/0_0?beaconFlowId=182C5F7FA851B550#?folder_id=home&browser=icon).

## Запуск игры
Для начала необходимо установить все пакеты по списку из requirements.txt коммандой:  

$ pip install -r requirements.txt  

или  

$ pip3 install -r requirements.txt  

После чего запустить файл main.py интерпретатором Python (для пользователей mac необходима версия Python 3.7.2, иначе работоспосбность программы разработчиками не гарантируется):  

$ python main.py  

или  

$ python3 main.py  

## Правила игры можно найти 
[Тут](https://github.com/Unicorn-Dev/Minimal.io/blob/new_ver_dev/HELP.md).

## Обратная связь
Все пожелания и замечания можно писать в телеграме @AlexFreik, @cosdar.
