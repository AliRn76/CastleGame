import os
from time import sleep


RANGE_X = 10
RANGE_Y = 3
RANGE_Z = 3
EMPTY = '-'

board = [[[EMPTY for _ in range(RANGE_X)] for _ in range(RANGE_Y)] for _ in range(RANGE_Z)]
database = []


class Game:
    @staticmethod
    def print_board():
        print(board)

    @classmethod
    def print_ground(cls):
        os.system('clear')  # on Linux System

        ground = board[0]
        for row in ground:
            for col in row:
                print(col['character'] if isinstance(col, dict) else EMPTY, end=' ')
            print()
        print()

        cls.print_units()

    @staticmethod
    def units():
        return [unit['obj'] for unit in database]

    @classmethod
    def print_units(cls):
        units = cls.units()
        for u in units:
            print(f'Unit: {u.name}\t\t HP: {u.hp}')

    @classmethod
    def remove_point(cls, *_point):
        x, y, z = _point
        board[z][y][x] = EMPTY
        return _point


class Unit(Game):
    def __init__(self, x, y, z, hp, attack, range, speed, is_team1: bool, character='*'):
        self._x = x if is_team1 else RANGE_X - x - 1
        self._y = y
        self._z = z
        self._hp = hp
        self._attack = attack
        self._range = range if is_team1 else -range
        self._speed = speed if is_team1 else -speed
        self._character = character
        self._team = is_team1
        self._target = None
        self.is_dead = False
        self.set_unit(self._x, self._y, self._z)
        self.name = id(self)

    @property
    def hp(self):
        return self._hp

    def has_target(self):
        return bool(self._target)

    def get_attacked(self, damage):
        if self._hp <= damage:
            print(f'{self.name} Just Died.')
            self._hp = 0
            self.died()
        else:
            self._hp -= damage

    def died(self):
        self.is_dead = True
        for i in database:
            if i['id'] == self.name:
                del i
        self.remove_point(self._x, self._y, self._z)

    def attack(self):
        if self._target.is_dead:
            self._target = None
        else:
            self._target.get_attacked(self._attack)

    def is_won(self):
        if self._team:
            return bool(self._x == RANGE_X-1)
        else:
            return bool(self._x == 0)

    def set_target(self, _id):
        for data in database:
            if data['id'] == _id:
                self._target = data['obj']

    def move_straight(self) -> None:
        self.remove_point(self._x, self._y, self._z)
        self._x, self._y, self._z = self.set_unit(self._x + self._speed, self._y, self._z)

    def is_enemy_in_range(self) -> bool:
        __range = range(1, self._range) if self._range > 0 else range(self._range, -1)
        for i in __range:
            if board[self._z][self._y][self._x + i] is not EMPTY:
                self.set_target(board[self._z][self._y][self._x + i]['id'])
                return True
            else:
                return False

    def set_unit(self, *_point) -> tuple:
        x, y, z = _point
        _data = {'character': self._character, 'hp': self._hp, 'id': id(self)}
        board[z][y][x] = _data
        return _point


u1 = Unit(x=0, y=1, z=0, hp=100, attack=20, range=2, speed=1, is_team1=True)
database.append({'id': u1.name, 'obj': u1})
u2 = Unit(x=0, y=1, z=0, hp=100, attack=10, range=2, speed=1, is_team1=False)
database.append({'id': u2.name, 'obj': u2})
# u3 = Unit(x=0, y=2, z=0, hp=100, attack=20, range=2, speed=1, is_team1=False)
# database.append({'id': u3.name, 'obj': u3})

for i, d in enumerate(database):
    print(f'Player {i}: {d["id"]}')


nobody_wins = True
while nobody_wins:
    Game.print_ground()
    sleep(.6)
    for unit in Game.units():
        if unit.is_dead:
            del unit
        else:
            if unit.is_won():
                print(f'Player {unit.name} Just Won The Game.')
                nobody_wins = False
                break

            if unit.has_target() or unit.is_enemy_in_range():
                unit.attack()
            else:
                unit.move_straight()

# TODO:
# [x]   1. Create Board
# [x]   2. Create Unit
# [x]   3. Move Unit
# [x]   4. Move Unit Till Find First Enemy in Line
# [x]   5. Stop & Attack Enemy
# [x]   6. Move After Killing Enemy
# [ ]   7. Find Enemy In Other Lines
# [ ]   8. Set Action Time For Attack
# [ ]   9. Find Measure For Speed And Range (board x = 1000, speed = 2, range = 50
# [ ]   10. Change Line When It Couldn't Move In His Line (randomly left or right)
# [ ]   11. Create Towers
# [ ]   12. Tower Attack Units
# [ ]   13. Unit Attack Towers
# [ ]   14. User Wins After Destroyed Tower
# [ ]   15. Add Air Units
# [ ]   16. Find Air Enemies
# [ ]   17. Attack Of Air Cards 
