# helper_in_word_game
python3.4, [pymongo](https://github.com/mongodb/mongo-python-driver)
- Помощник сможет найти слова из матрицы слов, например:
```
---------------------
| м | е | я | и | ь |
---------------------
| а | т | р | с | Т |
---------------------
| О | ж | а | ь | Н |
---------------------
| А | Л | о | б | о |
---------------------
| и | к | к | к | г |
--------------------- 
```

Есть матрицы состоящая из букв и необходимо найти все слова в ней, можно использовать переходы по диагонали. 
В программу необходимо передать ее как строку из символов 'меяиьатрсТОжаьНАЛобоикккг'.
Мы получим следующий вывод(часть):
```
БОЛЬШЕ ОЧКОВ
ТРАЛ
 ____________________
|   |   |   |   |   |
 ____________________
|   | Т | Р |   |   |
 ____________________
|   |   | А |   |   |
 ____________________
|   | Л |   |   |   |
 ____________________
|   |   |   |   |   | 
```
```
 БОЛЬШЕ ОЧКОВ
ТОЛКИ

 ____________________
|   |   |   |   |   | 
 ____________________
|   | Т |   |   |   | 
 ____________________
| О |   |   |   |   | 
 ____________________
|   | Л |   |   |   | 
 ____________________
| И | К |   |   |   |
```
*Примечание: если за слово можно получить больше очков, то необходимо написать его заглавной буквой.*

### Настройка:
`settings.py`
Для настройки работы программы нужно указать размерность матрицы
``` python
SIZE_MATRIX = 5
``` 
Строку букв из матрицы можно указать либо в настройках, либо передать аргументом из командной строки
``` python
LETTERS = None
``` 
Можно ли искать слова по диагонали
``` python
DIAGONAL = True
``` 
Максимальная длина слова, чем больше значение DEEP, тем дольше будет выполняться работа
``` python
DEEP = 5
``` 
Внутри программы лежит алгоритм поиска в глубину по графам, реализованный итеративно, но если вы хотите использовать рекурсию,
то необходимо поменять функцию generate.
``` python
def generate(self, path, goal, max_len):
        # рекурсивный метод
        if len(path) <= max_len:
            if self == goal:
                Graph.solns.append(path)
            else:
                for arc in self.arcs:
                    if arc not in path:
                        arc.generate(path + [arc], goal, max_len)
```

### Установка:
#### MongoDB
* pip install pymongo
* импортировать базу данных, которая находится в директории dump
#### Запуск:
```
python game.py меяиьатрсТОжаьНАЛобоикккг
```
