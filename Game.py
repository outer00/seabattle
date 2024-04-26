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

    def add_player(self, player):
        player.field = Field(self.field_sz)
        player.enemy_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        self.ships_setup(player)
        self.players.append(player)

    def ships_setup(self, player):
        for ship_value in [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            ship = Ship(ship_value, 0, 0, 0)
            while True:
                Game.clear_screen()
                player.field.draw_field('map')
                print(f'{player.name}, куда поставить {ship_value} корабль?')
                x, y, r = player.get_input('ship_setup')
                if x + y + r == -3:
                    print('Введите координаты еще раз')
                    continue
                ship.set_position(x, y, r)
                if player.field.check_ship_fits(ship, 'map'):
                    print('===')
                    player.field.add_ship_to_field(ship, 'map')
                    player.ships.append(ship)
                    break
                print('Так поставить корабль нельзя')

    def draw(self):
        self.current_player.field.draw_field('map')
        self.current_player.field.draw_field('radar')

    def switch_players(self):
        self.next_player, self.current_player = self.current_player, self.next_player

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
