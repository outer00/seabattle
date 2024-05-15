from Game import *
from Ship import *


class Player:
    numbers_to_letters = [chr(i) for i in range(ord('A'), ord('J') + 1)]
    letters_to_numbers = {chr(i): i - 65 for i in range(ord('A'), ord('J') + 1)}

    def __init__(self, name):
        self.name = name
        self.ships = []
        self.enemy_ships = []
        self.field = Field(10)

    @staticmethod
    def get_input(typee, loader):
        if typee == 'ship_setup':
            loader.context[
                'text'] = 'Введите букву A-J (строку), 1-10 (столбец), 1-2 (1, если горизонтально, 2 если вертикально) через пробел.'
            user_input = loader.entry.get().upper().split()
            if len(user_input) < 3:
                return -1, -1, -1
            x, y, r = user_input[0], user_input[1], user_input[2]
            if (not x in Player.numbers_to_letters) or (not y.isdigit()) or (not int(y) in range(1,
                                                                                                 Game.field_sz + 1)) or (
                    r not in (
                    '1', '2')):
                return -1, -1, -1
            return Player.letters_to_numbers[x], int(y) - 1, int(r)
        if typee == 'shot':
            loader.context['text'] = 'Введите букву A-J (строку), 1-10 (столбец) через пробел'
            user_input = loader.entry.get().upper().split()
            if len(user_input) < 2:
                return -1, -1
            x, y = user_input[0], user_input[1]
            if (not x in Player.numbers_to_letters) or (not y.isdigit()) or (not int(y) in range(1, Game.field_sz + 1)):
                return -1, -1
            return Player.letters_to_numbers[x], int(y) - 1

    def make_shot(self, target_player, loader):
        sx, sy = self.get_input('shot', loader)
        if sx + sy == -2 or self.field.radar[sx][sy] != ' ':
            return 'retry'
        shot_res = target_player.receive_shot((sx, sy))
        if shot_res == 'miss':
            self.field.radar[sx][sy] = '•'
        if shot_res == 'get':
            self.field.radar[sx][sy] = '□'
        if isinstance(shot_res, Ship):
            self.field.mark_destroyed_ship(shot_res, 'radar')
            self.enemy_ships.remove(shot_res.size)
            shot_res = 'kill'
        return shot_res

    def receive_shot(self, shot):
        sx, sy = shot
        if isinstance(self.field.map[sx][sy], Ship):
            ship = self.field.map[sx][sy]
            ship.hp -= 1
            if ship.hp <= 0:
                self.field.mark_destroyed_ship(ship, 'map')
                self.ships.remove(ship)
                return ship
            self.field.map[sx][sy] = '□'
            return 'get'
        else:
            self.field.map[sx][sy] = '•'
            return 'miss'
