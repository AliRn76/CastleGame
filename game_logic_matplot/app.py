import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep


RANGE_X = 10
RANGE_Y = 3
RANGE_Z = 3
EMPTY = '-'
DEBUG_RANGE = False
board = [[[EMPTY for _ in range(RANGE_X)] for _ in range(RANGE_Y)] for _ in range(RANGE_Z)]
database = []


class Game:
    @staticmethod
    def print_board():
        print(board)

    @classmethod
    def print_ground(cls):
        if DEBUG_RANGE:
            sleep(2)
        os.system('clear')  # on Linux System

        ground = board[0]
        for row in ground:
            for col in row:
                print(col['character'] if isinstance(col, dict) else EMPTY, end=' ')
            print()
        print()

        cls.print_units()
        sleep(.6)

    @staticmethod
    def units():
        return [unit['obj'] for unit in database]

    @classmethod
    def print_units(cls):
        units = cls.units()
        for u in units:
            print(f'Unit: {u.name}\t\t HP: {u.hp}')

    @classmethod
    def _remove_point(cls, *_point):
        """ Set EMPTY to given point """
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
        self._set_unit(self._x, self._y, self._z)
        self.name = id(self)

    @property
    def hp(self):
        return self._hp

    def has_target(self):
        return bool(self._target)

    def get_attacked(self, damage) -> bool:
        if self._hp <= damage:
            self._hp = 0
            self.died()
            return True
        else:
            self._hp -= damage
            return False

    def died(self):
        print(f'{self.name} Just Died.')
        sleep(3)
        self.is_dead = True
        for i in database:
            if i['id'] == self.name:
                database.remove(i)
        self._remove_point(self._x, self._y, self._z)

    def attack(self):
        # print("\nFunction attack() is running at time: " + str(int(time.time())) + " seconds.")
        # sleep(1)
        target_died = self._target.get_attacked(self._attack)
        if target_died:
            self._target = None

    def is_won(self):
        if self._team:
            return bool(self._x == RANGE_X-1)
        else:
            return bool(self._x == 0)

    def set_target(self, _id) -> None:
        """ get Object from DB and Set it to self._target """
        for data in database:
            if data['id'] == _id:
                self._target = data['obj']

    def move_straight(self) -> None:
        """ Clean current position & set new position for unit with self._set_unit() """
        self._remove_point(self._x, self._y, self._z)
        self._x, self._y, self._z = self._set_unit(self._x + self._speed, self._y, self._z)

    def _check_index(self, *_point) -> bool:
        """ return True if the index is exists (not IndexError) else False"""
        x, y, z = _point
        len_z = len(board)
        len_y = len(board[0])
        len_x = len(board[0][0])

        if 0 <= self._z + z < len_z \
                and 0 <= self._y + y < len_y \
                and 0 <= self._x + x < len_x:
            return True
        else:
            return False

    def is_enemy_in_range(self) -> bool:
        __range = range(1, self._range + 1, 1) if self._team else range(-1, self._range - 1, -1)

        debug_wait_time = 1
        if DEBUG_RANGE:
            print()

        for i in __range:
            if self._check_index(i, 0, 0):  # Check Forward
                if DEBUG_RANGE:
                    print(f'Forward\t {"-->" if self._team else "<--"} \t [Range: {abs(i)}]\t {board[self._z][self._y][self._x + i]}')
                    sleep(debug_wait_time)
                if board[self._z][self._y][self._x + i] is not EMPTY:
                    self.set_target(board[self._z][self._y][self._x + i]['id'])
                    return True

            if self._check_index(0, abs(i), 0):  # Check Down
                if DEBUG_RANGE:
                    print(f'Down \t {"-->" if self._team else "<--"} \t [Range: {abs(i)}]\t {board[self._z][self._y + abs(i)][self._x]}')
                    sleep(debug_wait_time)
                if board[self._z][self._y + abs(i)][self._x] is not EMPTY:
                    self.set_target(board[self._z][self._y + abs(i)][self._x]['id'])
                    return True

            if self._check_index(0, -abs(i), 0):  # Check Up
                if DEBUG_RANGE:
                    print(f'Up \t {"-->" if self._team else "<--"} \t [Range: {abs(i)}]\t {board[self._z][self._y - abs(i)][self._x]}')
                    sleep(debug_wait_time)
                if board[self._z][self._y - abs(i)][self._x] is not EMPTY:
                    self.set_target(board[self._z][self._y - abs(i)][self._x]['id'])
                    return True

            if self._check_index(-i, 0, 0):  # Check Back
                if DEBUG_RANGE:
                    print(f'Back \t {"-->" if self._team else "<--"} \t [Range: {abs(i)}]\t {board[self._z][self._y][self._x - i]}')
                    sleep(debug_wait_time)
                if board[self._z][self._y][self._x - i] is not EMPTY:
                    self.set_target(board[self._z][self._y][self._x - i]['id'])
                    return True

        return False

    def _set_unit(self, *_point) -> tuple:
        """ Set new position in board with given point """
        x, y, z = _point
        _data = {'character': self._character, 'hp': self._hp, 'id': id(self)}
        board[z][y][x] = _data
        return _point


def create_units():
    u1 = Unit(x=0, y=0, z=0, hp=100, attack=20, range=2, speed=1, is_team1=True)
    database.append({'id': u1.name, 'obj': u1})

    u2 = Unit(x=0, y=1, z=0, hp=100, attack=20, range=2, speed=2, is_team1=False)
    database.append({'id': u2.name, 'obj': u2})

    # u3 = Unit(x=0, y=2, z=0, hp=100, attack=20, range=2, speed=1, is_team1=False)
    # database.append({'id': u3.name, 'obj': u3})


nobody_wins = True

def main():
    global nobody_wins

    while nobody_wins:
        Game.print_ground()
        _units = Game.units()

        if len(_units) == 0:
            print('Draw')
            break

        # # # Model 1
        # for u in _units:
        #     run(u)

        # # # Model 2
        # with ThreadPoolExecutor(max_workers=len(_units)) as e:
        #     for u in _units:
        #         e.submit(run, u)

        # # # Model 3
        tasks = [Thread(target=run, args=(u, )) for u in _units]
        [t.start() for t in tasks]
        # [t.join() for t in tasks]

        # # # Model 4
        # tasks.append(asyncio.create_task(run(u)))

def run(u: Unit) -> None:
    global nobody_wins

    if u.is_dead:
        del u
    else:
        if u.is_won():
            print(f'Player {u.name} Just Won The Game.')
            nobody_wins = False
        elif u.has_target() or u.is_enemy_in_range():
            # sleep(.1)  # Don't know why, but it won't work correct without this sleep.
            u.attack()
        else:
            sleep(.1)  # Don't know why, but it won't work correct without this sleep.
            u.move_straight()


if __name__ == '__main__':
    create_units()
    main()
    # asyncio.run(main())

# TODO:
# [x]   1. Create Board
# [x]   2. Create Unit
# [x]   3. Move Unit
# [x]   4. Move Unit Till Find First Enemy in Line
# [x]   5. Stop & Attack Enemy
# [x]   6. Move After Killing Enemy
# [x]   7. Find Enemy In Other Lines
# [x]   7.1. Fix Range
# [x]   7.2. Make It Parallel
# [ ]   7.3 Change The "is not EMPTY" In is_enemy_in_range() TO Something Like: "is unit"
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
