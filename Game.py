import os

from Field import *
from Ship import *


class Game:
    field_sz = 10

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None
        self.status = 'prepare'
        self.cnt = 0

    def start_game(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def status_check(self):
        if self.status == 'prepare':
            if len(self.players) > 1:
                self.status = 'game'
                self.start_game()
                return
        if self.status == 'game' and (len(self.next_player.ships) == 0 or len(self.current_player.enemy_ships) == 0):
            self.status = 'game over'
            return

    def add_player(self, player, loader):
        player.field = Field(self.field_sz)
        player.enemy_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        # self.ships_setup(player, loader)
        self.players.append(player)

    def ships_setup(self, player, loader):
        ship_value = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4][len(player.ships)]
        ship = Ship(ship_value, 0, 0, 0)
        # Game.clear_screen()
        player.field.draw_field('map', loader)
        # print(f'{player.name}, куда поставить {ship_value} корабль?')
        x, y, r = player.get_input('ship_setup', loader)
        if x + y + r == -3:
            loader.context['text'] = 'Введите координаты еще раз'
            return False
        ship.set_position(x, y, r)
        if player.field.check_ship_fits(ship, 'map'):
            player.field.add_ship_to_field(ship, 'map')
            player.ships.append(ship)
            if len(player.ships) == 10:
                return True
            return False
        loader.context['text'] = 'Так поставить корабль нельзя'
        return False

    def draw(self, loader):
        self.current_player.field.draw_field('map', loader)
        self.current_player.field.draw_field('radar', loader)

    def switch_players(self):
        self.next_player, self.current_player = self.current_player, self.next_player


@staticmethod
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
