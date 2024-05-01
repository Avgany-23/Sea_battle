from random import randint
from copy import copy
from time import sleep


class Ship:  # Для представления кораблей
    _id = 0

    def __init__(self, length, tp=1, x=None, y=None):
        self.check_length_tp(length, tp)
        self._length = length  # Длина корабля (от 1 до 4)
        self._tp = tp  # Направление (1 - горизонтальное, 2 - вертикальное)
        self._x, self._y = x, y  # Координата начала корабля
        self._is_move = True  # True - корабль может перемещаться, False - не может. Если хоть 1 попадание, то False
        self._cells = [1 for i in range(self._length)]  # Список длиной _length. 1 - нет попадания, 2 - попадание
        self.ship_coord = 'Координаты не сгенерированы'
        if self._x is not None and self._y is not None:
            self.generate_ship_coord()

    def generate_ship_coord(self):
        vector1, vector2 = 0 if self._tp == 1 else 1, 1 if self._tp == 1 else 0
        self.ship_coord = [(self._x + i * vector1, self._y + i * vector2) for i in range(self._length)]

    def check_length_tp(self, l, tp):  # Проверка длины и направление корабля
        if l not in range(1, 5) or tp not in range(1, 3) or not isinstance(tp, int) or not isinstance(l, int):
            raise IndexError('Неправильные координаты корабля')

    def set_start_coords(self, x, y):  # Установка начального положения
        self._x = x
        self._y = y
        self.generate_ship_coord()

    def get_start_coords(self):  # Получение координат корабля
        return self._x, self._y

    def move(self, go):  # Если go -1 движение вперед, если -1, то движение в противоположную сторону
        if go not in range(-1, 2, 2):
            raise TypeError('Неверно введено перемещение корабля')
        if not self._is_move:
            raise IndexError('Корабль поврежден, движение невозможно')
        try:
            vector1, vector2 = 0 if self._tp == 1 else 1, 1 if self._tp == 1 else 0
            self._x, self._y = (self._x - 1 * vector1, self._y - 1 * vector2) if go == -1 else (self._x + 1 * vector1, self._y + 1 * vector2)
        except:
            pass


    def is_collide(self, ship):  # Проверка на то, пересекается ли корабль с другим
        c = ship.get_start_coords()
        x_y = self.get_start_coords()
        if self._length == 1:
            coord = x_y,
        else:
            coord = (x_y, (x_y[0], x_y[1] + self._length - 1)) if self._tp == 1 else (x_y, (x_y[0] + self._length - 1, x_y[1]))

        for q in coord:
            for i in ((q[0] - 1, q[1]), (q[0] - 1, q[1] + 1), (q[0], q[1] + 1), (q[0] + 1, q[1] + 1), (q[0], q[1]),
                      (q[0] + 1, q[1]), (q[0] + 1, q[1] - 1), (q[0], q[1] - 1), (q[0] - 1, q[1] - 1)):
                if i in tuple((c[0] + i, c[1]) if ship._tp == 2 else (c[0], c[1] + i) for i in range(ship._length)):
                    return True
        return False

    def is_out_pole(self, size=10):  # Если корабль выходит за поле, вернёт True, если нет, то False
        x_pole = self._x + self._length - 1 if self._tp == 2 else self._x
        y_pole = self._y + self._length - 1 if self._tp == 1 else self._y
        if x_pole > size - 1 or y_pole > size - 1:
            return True
        return False

    def __setattr__(self, key, value):
        if key in ('_x', '_y') and value is not None:
            if value < 0 or value > 10:
                raise IndexError(f'Координата {key} выходит за размер поля 10 на 10')
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        if value != 2:
            raise TypeError('Value в методе setitem должно быть равно 2')
        self._cells[key] = value

    def __str__(self):
        return (f'координаты = {self.get_start_coords()}, длина = {self._length}, '
                f'направление = {self._tp}, полные координаты = {self.ship_coord}')


class GamePole:  # Для описания игрового поля
    def __init__(self, size=10):
        self.check_size(size)
        self.size = size
        self.pole = [[0] * self.size for i in range(self.size)]
        self._ships = []  # Список кораблей

    def check_size(self, size):
        if not isinstance(size, int):
            raise TypeError('Size должно быть целым числом')
        if size <= 0:
            raise TypeError('Size должно быть положительным числом')

    def init(self):
        add_3_size_ship = [self._ships.append(Ship(4, tp=randint(1, 2))) for i in range(1)]
        add_3_size_ship = [self._ships.append(Ship(3, tp=randint(1, 2))) for i in range(2)]
        add_2_size_ship = [self._ships.append(Ship(2, tp=randint(1, 2))) for i in range(3)]
        add_1_size_ship = [self._ships.append(Ship(1, tp=randint(1, 2))) for i in range(4)]
        pole_check = []
        for ship_main in self._ships:
            count_ship_main = True
            while count_ship_main:
                ship_main.set_start_coords(randint(0, 10), randint(0, 10))
                if not ship_main.is_out_pole(self.size):
                    if len(pole_check) == 0:
                            count_ship_main = False
                            pole_check.append(ship_main)
                    else:
                        count = 0
                        for i in pole_check:
                            if not i.is_collide(ship_main):
                                count += 1
                        if count == len(pole_check):
                            count_ship_main = False
                            pole_check.append(ship_main)
        self.generate_pole(self.size)

    def get_ships(self):
        return self._ships

    def move_ships(self):  # Перемещает вперёд или назад, если невозможно, то ничего не делает
        for index, ship in enumerate(self._ships):
            if self.move_one_ship(index, 1):
                pass
            else:
                self.move_one_ship(index, -1)

    def move_one_ship(self, index, vector):  # True, если сдвинулся, False - если не сдвинулся
        ship = copy(self._ships[index])
        if not ship.is_out_pole(self.size):
            ship.move(vector)
        check_move_all = list(True if i != ship and not ship.is_collide(i) else False for i in self._ships)
        if (True if len(list(filter(lambda x: x, check_move_all))) == (len(self._ships) - 1) else False) and not ship.is_out_pole(self.size):
            self._ships[index].move(vector)
            vec1, vec2 = (0, 1) if ship._tp == 1 else (1, 0)
            if vector == 1:
                self.pole[ship._x - 1 * vec1][ship._y - 1 * vec2] = 0
            else:
                self.pole[ship._x + 1 * vec1 * (ship._length)][ship._y + 1 * vec2 * (ship._length)] = 0
            return True
        return False

    def generate_pole(self, i=10):
        for ship in self._ships[:i]:
            vector_1, vector_2 = 0 if ship._tp == 1 else 1, 1 if ship._tp == 1 else 0
            for i in range(ship._length):
                self.pole[ship.get_start_coords()[0] + 1 * i * vector_1][ship.get_start_coords()[1] + 1 * i * vector_2] = ship._cells[i]

    def show(self):
        unicode = {0: '⬜', 1: '🔴', 2: '❌'}
        print('\n'.join('\t'.join(unicode[q] for q in i) for i in self.pole))

    def get_pole(self):
        return tuple(tuple(i for i in q) for q in self.pole)


class SeaBattle:
    def __init__(self):  # Создание полей
        self.pole_gamer = GamePole()
        self.pole_gamer.init()
        self.gamer_pole_fire = [['⬜'] * 10 for i in range(10)]
        self.check_coord = []

        self.pole_computer = GamePole()
        self.pole_computer.init()
        self.computer_pole_fire = [['⬜'] * 10 for i in range(10)]


        print(f'\n{chr(10146)}Для победы нужно набрать 20 очков (1 очко - 1 попадание)\n'
              f'{chr(10146)}Данное количество очков наберётся тогда, когда будут уничтожены все вражеские корабли\n'
              f'{chr(10146)}Если корабль взорвется, то вокруг него автоматически проставятся крестики и эти поля будут считаться стрелянными\n')

        # Данные для стрельбы компьютера
        self.yes_hit = True  # Пока True, компьютер будет стрелять
        self.x_comp_hit, self.y_comp_hit = None, None  # Для запоминания выстрела
        self.x_comp_hit2, self.y_comp_hit2 = None, None  # Для запоминания второго выстрела
        self.hit_index = 0  # Чтобы контролировать весь фон попадания
        self.hit_ship_computer = 0  # Количества попаданий компьютера
        self.random_hit = True  # Разрешение на случайную стрельбу, изначально разрешено
        self.next_hit = False  # Разрешение на осознанную стрельбу, изначально запрещено
        self.hit_index = 0  # Для запоминания горизонтального и вертикального фона
        self.num_hit = 1  # Количество попаданий, если 1 - то стрельба по всему фону, если 2 - то по выбранному фону
        self.vector_two_hit = None
        self.hit_tuple2 = None  # Для третьего и четвертого выстрела
        self.hit_index2 = 0  # Чтобы контролировать НУЖНЫЙ фон
        self.block_hit_tuple2 = True  # Разрешаем создавать НУЖНЫЙ фон для осознанного выстрел
        self.block_hit_tuple2_end = False  # Запрет на создание НУЖНОГО ПОСЛЕДНЕГО фона для осознанного выстрела
        self.nums_hit = 0  # Для контроля того, когда запоминать второй выстрел
        self.cells_computer = []  # Список для выстрелов компьютера, здесь ячейки, по которым он стрелять не будет
        self.countssss = 0  # Счетчик для остановки при бесконечном цикле, потом УДАЛИТЬ
        self.result_game = None  # Итог игры, показывает, кто выиграл

    def start_game(self):  # Запуск игры
        hit_gamer = 0
        while hit_gamer != 20:  # Пока не выиграл человек или компьютер

            # Тут стреляет игрок
            next_step_gamer = True
            while next_step_gamer:
                print(f'{chr(127993)}Количество ваших очков: {hit_gamer}{' ' * 29}{chr(128187)}Количество очков, которые набрал компьютер: {self.hit_ship_computer}')
                print(f'Вражеское поле, выстрелы совершайте по нему{' ' * 15} Выстрелы, которые совершил компьютер по вашему полю')
                self.show_gamer_pole_fire()
                check_hit_gamer = True
                x_gamer, y_gamer = None, None
                while check_hit_gamer:
                    try:
                        x_gamer, y_gamer = input('Ваш ход: ').split()
                    except ValueError:
                        print('Должно быть две координаты')
                        continue
                    if not x_gamer.isdigit() or not y_gamer.isdigit():
                        print('Координаты должны быть целым числом')
                        continue
                    if (int(x_gamer), int(y_gamer)) in self.check_coord:
                        print('На эту точку уже был произведён выстрел, сделайте другой ход')
                        continue
                    if int(x_gamer) not in range(1, 11) or int(y_gamer) not in range(1, 11):
                        print('Выстрел выходит за границы поля. Координаты должны быть в диапазоне [1, 10]')
                        continue
                    check_hit_gamer = False
                self.check_coord.append((int(x_gamer), int(y_gamer)))
                # Производится выстрел
                self.step_fire(int(x_gamer) - 1, int(y_gamer) - 1, self.pole_computer, self.gamer_pole_fire, 2)

                if self.pole_computer.pole[int(x_gamer) - 1][int(y_gamer) - 1] == 1:
                    print('Ты попал')
                    hit_gamer += 1
                    if hit_gamer == 20:  # Выиграл человек, условие заканчивает игру
                        self.result_game = 1
                        break

                else:
                    next_step_gamer = False
                    print('Ты промахнулся')
                sleep(0.4)
                print(f"{'-' * 39}")
            if hit_gamer == 20:  # Выиграл человек, условие заканчивает игру
                self.result_game = 1
                break

            print('Ход бездушной машины по вашему полю')
            sleep(0.4)
            # Тут стреляет компьютер, сначала на рандом
            while self.yes_hit:
                if self.random_hit:  # Проверяет, стрелять ли наугад
                    if self.hit_cumputer_random():  # Стреляет наугад и возвращает условие

                        self.next_hit = True  # Чтобы следующий выстрел был осознанный
                        self.random_hit = False  # После попадания запрещаем стрелять на рандом
                        if self.hit_ship_computer == 20:
                            self.result_game = 0
                            break

                if self.hit_ship_computer == 20:
                    self.result_game = 0
                    break

                if self.next_hit:
                    self.hit_cumputer_deliberate()

            self.yes_hit = True  # Чтобы компьютер стрелял после игрока
            print(f"{'-' * 39}")

            if self.hit_ship_computer == 20:  # Выиграл компьютер, условие заканчивает игру
                self.result_game = 0
                break

            sleep(0.3)

        for i in range(1, 10):
            sleep(0.3)
            print(i * '.')
        print('Победа кожаного мешка' if self.result_game == 1 else 'Победа бездушной машины')

    def hit_cumputer_deliberate(self):
        next_step_computer = True

        while next_step_computer:  # Пока это условие верно

            # Когда одно попадание, то стреляет во все стороны (во весь фон)
            if self.num_hit == 1:  # Одно попадание, стреляем по всему фону

                x_new, y_new = self.x_comp_hit - 1, self.y_comp_hit - 1
                hit_tuple = ((x_new + 1, y_new), (x_new - 1, y_new), (x_new, y_new + 1), (x_new, y_new - 1))

                for fire in hit_tuple[self.hit_index:]:
                    if 0 <= fire[0] <= 9 and 0 <= fire[1] <= 9:  # Если выстрел находится в зоне поля

                        # Проверяем, не стрелял ли в эту точку компьютер
                        if self.computer_pole_fire[fire[0]][fire[1]] == '⬜':  # Если не стрелял, то делает выстрел
                            self.step_fire(fire[0], fire[1], self.pole_gamer, self.computer_pole_fire, 1) # Выстрел
                            self.cells_computer.append((fire[0] + 1, fire[1] + 1))  # Добавляем выстрел в стрелянный
                            self.show_computer_pole_fire()  # Отображение поля после данного выстрела


                            # Проверяем, попал ли компьютер
                            if self.pole_gamer.pole[fire[0]][fire[1]] == 1:
                                self.hit_ship_computer += 1  # Прибавляем компьютеру попадание
                                yes_kill = 0  # 0 - корабль не уничтожен, 1 - уничтожен



                                # Проверить, уничтожен ли корабль
                                for ship in self.pole_gamer._ships:
                                    if (fire[0], fire[1]) in ship.ship_coord:
                                        if all(True if i == 2 else False for i in ship._cells):  # Корабль уничтожен
                                            yes_kill = 1


                                if yes_kill == 1:  # Корабль уничтожен
                                    # Но значит нужно запустить рандомный выстрел !!!!!!!!!!!!!!!!!
                                    self.random_hit = True  # Запускаем снова рандомные выстрелы
                                    self.next_hit = False  # Запрещаем осознанные выстрелы
                                    next_step_computer = False  # Выходим из текущего while
                                    self.hit_index = 0  # Обнуляем общий фон
                                    self.x_comp_hit, self.y_comp_hit = None, None  # Обнуляем выстрелы, которые запоминали
                                    print('Компьютер попал и уничтожил ваш корабль')
                                    sleep(1)
                                    return True  # Выходим с функции


                                else:  # Корабль НЕ уничтожен после ВТОРОГО выстрела
                                    '''
                                    Есть два попадания, но корабль не уничтожен, значит выбираем нужный фон
                                    1) Узнать, по какому кораблю идет стрельба и выбрать у него нужный фон, горизонтальный
                                    или вертикальный.
                                    2) Переопределить фон
                                    3) Выйти из этого условия, то есть self.num_hit = 2
                                    Для начала запущу снова рандомный выстрел, то есть вернет True
                                    А так должен вернуть 'FonTwo', чтобы стрелял по нужному фону
                                    '''
                                    self.nums_hit += 1  # Для количества попадания
                                    self.num_hit = 2  # Чтобы перейти к обстрелу НУЖНОГО фона
                                    # if self.nums_hit == 2:

                                    self.hit_index = 0  # Обнуляем общий фон
                                    self.x_comp_hit2, self.y_comp_hit2 = fire[0] + 1, fire[1] + 1  # Запоминаем второй выстрел
                                    print('Компьютер попал')
                                    sleep(1)
                                    break  # Выходим из цикла for, который обстреливает ОБЩИЙ фон

                            else:  # Компьютер промахнулся, выстрел по следующему полю
                                print('Компьютер промахнулся')
                                sleep(1)
                                # Если промах, то стреляет по следующей зоне возле корабля
                                self.hit_index += 1  # Для следующего выстрела по фону
                                next_step_computer = False  # Закрываем цикл while
                                self.yes_hit = False  # Заканчивает стрелять и выстрел переходит игроку
                                return True  # Выходим с функции

            if self.num_hit == 2:  # Два попадания попадание, стреляем по нужному фону

                if self.block_hit_tuple2:  # Проверяем, можно ли создавать НУЖНЫЙ фон

                    # Определяем положение корабля: 1 - горизонтальный, 2 - вертикальный
                    self.vector_two_hit = 1 if self.x_comp_hit == self.x_comp_hit2 else 2

                    if self.vector_two_hit == 1:  # Горизонтальное положение
                        if self.y_comp_hit < self.y_comp_hit2:
                            self.hit_tuple2 = [(self.x_comp_hit, self.y_comp_hit - 1), (self.x_comp_hit2, self.y_comp_hit2 + 1)]
                        else:
                            self.hit_tuple2 = [(self.x_comp_hit, self.y_comp_hit + 1), (self.x_comp_hit2, self.y_comp_hit2 - 1)]
                    else:  # Вертикальное положение
                        if self.x_comp_hit < self.x_comp_hit2:
                            self.hit_tuple2 = [(self.x_comp_hit - 1, self.y_comp_hit), (self.x_comp_hit2 + 1, self.y_comp_hit2)]
                        else:
                            self.hit_tuple2 = [(self.x_comp_hit + 1, self.y_comp_hit), (self.x_comp_hit2 - 1, self.y_comp_hit2)]

                for fire in self.hit_tuple2[self.hit_index2:]:
                    fire = list(fire)
                    fire[0] -= 1
                    fire[1] -= 1
                    if 0 <= fire[0] <= 9 and 0 <= fire[1] <= 9:  # Если выстрел находится в зоне поля

                        # Проверяем, не стрелял ли в эту точку компьютер
                        if self.computer_pole_fire[fire[0]][fire[1]] == '⬜':  # Если не стрелял, то делает выстрел
                            self.step_fire(fire[0], fire[1], self.pole_gamer, self.computer_pole_fire, 1)  # Выстрел
                            self.cells_computer.append((fire[0] + 1, fire[1] + 1))  # Добавляем выстрел в стрелянный
                            self.show_computer_pole_fire()  # Отображение поля после данного выстрела
                            # Проверяем, попал ли компьютер
                            if self.pole_gamer.pole[fire[0]][fire[1]] == 1:
                                self.hit_ship_computer += 1  # Прибавляем компьютеру попадание

                                yes_kill2 = 0  # 0 - корабль не уничтожен, 1 - уничтожен

                                # Проверить, уничтожен ли корабль
                                for ship in self.pole_gamer._ships:
                                    if (fire[0], fire[1]) in ship.ship_coord:
                                        if all(True if i == 2 else False for i in ship._cells):  # Корабль уничтожен
                                            yes_kill2 = 1

                                if yes_kill2 == 1:  # Попал и корабль уничтожен
                                    # Но значит нужно запустить рандомный выстрел !!!!!!!!!!!!!!!!!
                                    self.random_hit = True  # Запускаем снова рандомные выстрелы
                                    self.next_hit = False  # Запрещаем осознанные выстрелы
                                    next_step_computer = False  # Выходим из текущего while
                                    self.hit_index2 = 0  # Обнуляем НУЖНЫЙ фон
                                    self.x_comp_hit, self.y_comp_hit = None, None  # Обнуляем выстрелы, которые запоминали
                                    self.x_comp_hit2, self.y_comp_hit2 = None, None  # Обнуляем выстрелы, которые запоминали
                                    self.num_hit = 1  # Обнуляем попадания, чтобы в следующий раз стрелял по фону
                                    self.vector_two_hit = None  # Обнуляем направление корабля
                                    self.hit_tuple2 = None  # Обнуляем список с ФОНОМ
                                    self.block_hit_tuple2 = True  # Разрешаем определять третий ФОН
                                    print('Компьютер попал и уничтожил ваш корабль')
                                    sleep(1)
                                    return True  # Выходим с функции

                                else:  # Попал, но корабль НЕ уничтожен
                                    '''
                                    Третье и четвертое попадание
                                    Нужно обновить self.hit_tuple2 и запретить его создание в начале
                                    '''
                                    self.block_hit_tuple2 = False  # Запрещаем переопределять НУЖНЫЙ фон в начале for
                                    self.num_hit = 2  # Чтобы перейти к обстрелу НУЖНОГО фона
                                    self.hit_index2 = 0  # Обнуляем общий фон

                                    # Тут переопределяем ПОСЛЕДНИЙ ФОН
                                    fire[1] += 1
                                    fire[0] += 1
                                    if self.vector_two_hit == 1:  # Горизонтальный корабль
                                        if self.y_comp_hit < fire[1]:
                                            if self.y_comp_hit < self.y_comp_hit2:
                                                self.hit_tuple2 = [(self.x_comp_hit, self.y_comp_hit - 1),
                                                                (fire[0], fire[1] + 1)]
                                            else:
                                                self.hit_tuple2 = [(self.x_comp_hit, self.y_comp_hit2 - 1),
                                                                    (fire[0], fire[1] + 1)]

                                        else:
                                            if self.y_comp_hit < self.y_comp_hit2:
                                                self.hit_tuple2 = [(self.x_comp_hit, self.y_comp_hit2 + 1),
                                                                    (fire[0], fire[1] - 1)]
                                            else:
                                                self.hit_tuple2 = [(self.x_comp_hit, self.y_comp_hit + 1),
                                                                    (fire[0], fire[1] - 1)]


                                    else:  # Вертикальный корабль
                                        if self.x_comp_hit < fire[0]:
                                            if self.x_comp_hit > self.x_comp_hit2:
                                                self.hit_tuple2 = [(self.x_comp_hit - 1, self.y_comp_hit),
                                                                    (fire[0] + 1, fire[1])]
                                            else:
                                                self.hit_tuple2 = [(self.x_comp_hit2 - 1, self.y_comp_hit),
                                                                    (fire[0] + 1, fire[1])]
                                        else:
                                            if self.x_comp_hit > self.x_comp_hit2:
                                                self.hit_tuple2 = [(self.x_comp_hit + 1, self.y_comp_hit),
                                                                    (fire[0] - 1, fire[1])]
                                            else:
                                                self.hit_tuple2 = [(self.x_comp_hit2 + 1, self.y_comp_hit),
                                                                    (fire[0] - 1, fire[1])]

                                    self.block_hit_tuple2_end = False  # Запрещаем переопределять последний ФОН
                                    print('Компьютер попал')
                                    sleep(1)
                                    break  # Выходим из цикла for, который обстреливает ОБЩИЙ фон

                            else:  # Компьютер промахнулся, выстрел по следующему ФОНУ
                                print('Компьютер промахнулся')
                                sleep(1)
                                # Если промах, то стреляет по следующей зоне возле корабля
                                self.hit_index2 += 1  # Для следующего выстрела по фону
                                next_step_computer = False  # Закрываем цикл while
                                self.yes_hit = False  # Заканчивает стрелять и выстрел переходит игроку
                                return True  # Выходим с функции


    def hit_cumputer_random(self):
        random_hit = True
        x_comp, y_comp = None, None
        while random_hit:
            check_cells = True
            while check_cells:  # Стреляет, пока не попадет на свободную клетку
                x_comp_, y_comp_ = randint(1, 10), randint(1, 10)
                if (x_comp_, y_comp_) not in self.cells_computer:
                    self.cells_computer.append((x_comp_, y_comp_))
                    x_comp, y_comp = x_comp_, y_comp_
                    check_cells = False

            # Производится выстрел на рандом
            self.step_fire(x_comp - 1, y_comp - 1, self.pole_gamer, self.computer_pole_fire, 1)  # Выстрел
            self.show_computer_pole_fire()  # Отображение поля после данного выстрела

            if self.pole_gamer.pole[x_comp - 1][y_comp - 1] == 1:  # Проверка на попадание
                self.hit_ship_computer += 1  # Прибавляем попадание компьютеру

                # Если корабль уничтожен, то снова стреляет наугад
                for ship in self.pole_gamer._ships:
                    if (x_comp - 1, y_comp - 1) in ship.ship_coord:
                        if all(True if i == 2 else False for i in ship._cells):
                            print('Компьютер попал и уничтожил ваш корабль')
                            sleep(1)
                            return False  # Следующий выстрел будет снова наугад

                        else:
                            '''
                            Если корабль не уничтожен, то следующий выстрел будет осознанный по границам.
                            Из этого цикла While надо выйти и сказать работать следующему циклу while
                            '''
                            random_hit = False
                            # Надо как-нибудь сохранить выстрел попадания, после которого корабль НЕ уничтожился
                            print('Компьютер попал')
                            sleep(1)
                            self.x_comp_hit,  self.y_comp_hit = x_comp_, y_comp_
                            return True  # Следующий выстрел будет осознанный
            else:  # Компьютер промахнулся
                random_hit = False
                self.yes_hit = False  # Заканчивает стрелять и ход переходит игроку
                print('Компьютер промахнулся')
                sleep(1)
        return False  # Следующий выстрел будет снова наугад

    def show_gamer_pole_fire(self):
        print(f' 1  2  3   4  5  6   7  8  9  10{' ' * 27} 1  2  3   4  5  6   7  8  9  10')
        # 20 19
        for q in range(len(self.gamer_pole_fire)):
            print(f' '.join(f"""{''.join(str(q) for q in self.gamer_pole_fire[q])}{q + 1} {' ' * 10 if q != (len(self.gamer_pole_fire) - 1) else ' ' * 9} {''.join(str(q) for q in self.computer_pole_fire[q])}{q + 1}"""))


    def show_computer_pole_fire(self):
        print(f' 1  2  3   4  5  6   7  8  9  10\n' +
              '\n'.join(f"{' '.join(str(q) for q in i)}{q + 1}" for q, i in enumerate(self.computer_pole_fire)))

    def step_fire(self, x, y, pole, pole_fire, cells_comp=None):  # Выстрел
        if pole.pole[x][y] == 0:
            pole_fire[x][y] = '❌'

        elif pole.pole[x][y] == 1:
            pole_fire[x][y] = '✅'
            for ship in pole._ships:
                vector_1, vector_2 = 0 if ship._tp == 1 else 1, 1 if ship._tp == 1 else 0
                for i in range(ship._length):
                    x_ship, y_ship = (ship.get_start_coords()[0] + 1 * i * vector_1), (ship.get_start_coords()[1] + 1 * i * vector_2)
                    if x == x_ship and y == y_ship:
                        ship._cells[i] = 2

                    if all(True if i == 2 else False for i in ship._cells):
                        for i in range(ship._length):
                            x_ship, y_ship = (ship.get_start_coords()[0] + 1 * i * vector_1), (ship.get_start_coords()[1] + 1 * i * vector_2)
                            for q in ((x_ship - 1, y_ship), (x_ship + 1, y_ship), (x_ship, y_ship - 1), (x_ship, y_ship + 1),
                                (x_ship - 1, y_ship - 1), (x_ship + 1, y_ship - 1), (x_ship - 1, y_ship + 1), (x_ship + 1, y_ship + 1)):
                                if 0 <= q[0] <= 9 and 0 <= q[1] <= 9:
                                    if pole_fire[q[0]][q[1]] == '⬜':
                                        pole_fire[q[0]][q[1]] = '❌'
                                        if cells_comp == 1:
                                            self.cells_computer.append((q[0] + 1, q[1] + 1))
                                        else:
                                            self.check_coord.append((q[0] + 1, q[1] + 1))

            return True
        return False


a = SeaBattle()
a.start_game()