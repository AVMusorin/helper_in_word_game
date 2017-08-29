import pymongo
import sys
import time
from settings import (LETTERS,
                      SIZE_MATRIX,
                      MONGO,
                      DIAGONAL,
                      DEEP)



class Graph:
    def __init__(self, label, letter, important=False):
        self.name = label
        self.arcs = []
        self.num = int(label[1:])
        self.letter = letter
        self.important = important

    def __repr__(self):
        return self.name

  
    def search(self, goal, max_len):
        Graph.solns = []
        self.generate([self], goal, max_len)
        Graph.solns.sort(key=lambda x: len(x))
        return Graph.solns


    def generate(self, path, goal, max_len):
        variants = []
        variants.append(path)
        while True:    
            if len(variants) == 0:
                break
            for variant in variants:
                if variant[-1] == goal:
                    Graph.solns.append(variant)
                    variants.remove(variant)
                    continue
                if len(variant) >= max_len:
                    variants.remove(variant)
                    continue
                else:
                    arcs = variant[-1].arcs
                    new_variants = [variant+[arc] for arc in arcs if arc not in variant]
                    variants.remove(variant)
                    for var in new_variants:
                        variants.append(var)


def make_matrix(matrix):
    ''' Создание двумерной матрицы
        matrix - размерность матрицы

        На выходе получаем номера элементов матрицы, те ['11','12',..]
        Создается только квадратная матрица    
    '''
    if matrix < 2:
        raise Exception('Размерность матрицы должна быть >= 2')

    array = []
    for i in range(1, matrix + 1):
        l = []
        for j in range(1, matrix + 1):
            l.append(str(i)+str(j))
        array.append(l)
    return array


def letter_matrix(letters, length):
    ''' Преобразует строку с слов в матрицу размерности length
        letters = 'abCcdeRty' 
        return example: ['abc','cde','rty']
    '''
    if len(letters) != length**2:
        raise Exception('Количество слов не совпадает с количеством элементов в матрице')
    letter_matrix = []
    for _ in range(length):
        letter_matrix.append(letters[:length].lower())
        letters = letters[length:]
    return letter_matrix


def print_matrix(function):
    ''' Декоратор для вывода найденных слов '''
    def the_wrapper(letter_matrix, positions):
        matrix = function(letter_matrix, positions)
        for row in matrix:
            print('','_'*4*len(matrix)) 
            line = '| '
            for element in row:
                if element.isupper():
                    line += element + ' | '
                else:
                    line += ' ' + ' | ' 
            print(line)
    return the_wrapper


@print_matrix
def print_letter_matrix(matrix, positions):
    ''' 
    Функция печатает всю матрицу и выделяет слово, найденное в ней

    positions = [(i_pos, j_pos), ...]
    '''
    for pos in positions:
        if pos[1] == len(matrix[0]):
            matrix[pos[0]-1] = matrix[pos[0]-1][:pos[1]-1] + matrix[pos[0]-1][-1].upper()
        elif pos[1] == 1:
            # если это начало ряда
            matrix[pos[0]-1] = matrix[pos[0]-1][pos[1]-1].upper() + matrix[pos[0]-1][1:]
        else:
            matrix[pos[0]-1] = matrix[pos[0]-1][:pos[1]-1] + matrix[pos[0]-1][pos[1]-1].upper()+matrix[pos[0]-1][pos[1]:]
    return matrix


def get_neighbors(number, matrix, stop = None):
    '''
    number(str) - позиция, которую надо найти в матрице, например "11"
    matrix - размер матрицы(!максимальный размер матрицы 9)
    если number лежит за пределами матрицы, то возвращается None
    '''
    if matrix <= 1 or matrix > 9:
        print('Матрица должна быть в пределах [2,9]')
        return None
    try:
        int(number)
    except ValueError as e:
        print(e, 'Невозможно преобразовать %s к типу данных int' %number)
        return None

    neighbors = []
    n_parts = list(number)

    if int(n_parts[0]) not in range(1, matrix + 1) or int(n_parts[1]) not in range(1, matrix + 1):
        print('Число %s не может быть индексами в матрице размерностью %s' %(number, matrix))
        return None    

    # для первой позиции 11
    if n_parts[0] == '1' and n_parts[1] == '1':
        if DIAGONAL:
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) + 11))
        else:
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) + 1))

    # для последней позиции в строке
    elif n_parts[0] == '1' and n_parts[1] == str(matrix):
        if DIAGONAL:
            neighbors.append(str(int(number) - 1))
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) + 9))
        else:
            neighbors.append(str(int(number) - 1))
            neighbors.append(str(int(number) + 10))

    # для позиции перовй строки [12..nn-1]
    elif n_parts[0] == '1' and n_parts[1] != '1' and n_parts[1] != str(matrix):
        if DIAGONAL:
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) + 11))
            neighbors.append(str(int(number) + 9))
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) - 1))
        else:
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) - 1))
            neighbors.append(str(int(number) + 10))

    # для позиции первого столбца [21 .. nn-1]
    elif n_parts[0] != '1' and n_parts[1] == '1' and n_parts[0] != str(matrix):
        if DIAGONAL: 
            neighbors.append(str(int(number) - 10)) 
            neighbors.append(str(int(number) - 9))
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) + 11))
            neighbors.append(str(int(number) + 10))
        else:
            neighbors.append(str(int(number) - 10)) 
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) + 1))

    # для последней позиции n1
    elif n_parts[0] == str(matrix) and n_parts[1] == '1':
        if DIAGONAL:
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 9))
            neighbors.append(str(int(number) + 1))
        else:
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) - 10))


    # для позиции последнего столбца [n2 .. nn-1]
    elif n_parts[0] == str(matrix) and n_parts[1] != '1' and n_parts[1] != str(matrix):
        if DIAGONAL:
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 9))
            neighbors.append(str(int(number) - 11))
            neighbors.append(str(int(number) - 1))
        else:
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 1))
            neighbors.append(str(int(number) + 1))

    # для последней позициии в последней строке nn
    elif n_parts[0] == str(matrix) and n_parts[1] == str(matrix):
        if DIAGONAL:
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 11))
            neighbors.append(str(int(number) - 1))
        else:
            neighbors.append(str(int(number) - 1))
            neighbors.append(str(int(number) - 10))

    # для последнего столбца [2n .. n-1n]
    elif n_parts[0] != '1' and n_parts[0] != str(matrix) and n_parts[1] == str(matrix):
        if DIAGONAL:
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 11))
            neighbors.append(str(int(number) - 1))
            neighbors.append(str(int(number) + 9))
            neighbors.append(str(int(number) + 10))
        else:
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 1))

    else:
        if DIAGONAL:
            neighbors.append(str(int(number) - 11))
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) - 9))
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) + 11))
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) + 9))
            neighbors.append(str(int(number) - 1))
        else:
            neighbors.append(str(int(number) - 10))
            neighbors.append(str(int(number) + 1))
            neighbors.append(str(int(number) + 10))
            neighbors.append(str(int(number) - 1))

    if stop:
        if stop in neighbors:
            neighbors.remove(stop)
    return neighbors

def add_acrs(matrix):
    for i in matrix:
        neighbors = get_neighbors(str(i.num), SIZE_MATRIX)
        for neighbor in neighbors:
            exec('%s.arcs.append(_%s)'%(i, neighbor))


def mongo_connect(db, collection):
    client = pymongo.MongoClient()
    db = client[db]
    collection = db[collection]
    return collection


def main(letters, matrix):
    collection = mongo_connect(MONGO['db_name'], MONGO['collection'])
    all_words = []
    for i in matrix:
        for j in matrix:
            if i != j:
                _goals = i.search(j, DEEP)
                for goal in _goals:
                    word = ""
                    important = False
                    positions = []
                    for item in goal:
                        word += item.letter
                        positions.append((int(item.num/10),item.num%10))
                        if item.important:
                            important = True
                    if word not in all_words:    
                        if collection.find_one({'word':word}):
                            if len(word) > 3:
                                _letter_matrix = letter_matrix(letters, SIZE_MATRIX)
                                if important:
                                    print(' БОЛЬШЕ ОЧКОВ')
                                    print(word.upper())
                                    print_letter_matrix(_letter_matrix, positions)
                                    print()
                                else:
                                    print(word.upper())
                                    print_letter_matrix(_letter_matrix, positions)
                                    print()
                            all_words.append(word)


if __name__ == '__main__':
    try:
        letters = sys.argv[1]
    except IndexError:
        letters = LETTERS

    matrix = []
    if letters:
        count = 0
        for i in make_matrix(SIZE_MATRIX):
            for j in i:
                if letters[count].isupper():
                    exec("_%s = Graph('_%s', '%s',important=%s)" %(j, j, letters[count].lower(), True))
                else:
                    exec("_%s = Graph('_%s', '%s')" %(j, j, letters[count].lower()))

                exec("matrix.append(_%s)"%j)
                count += 1
        add_acrs(matrix)
        main(letters, matrix)
    else:
        raise Exception('Необходимо передать строку из букв')
        
