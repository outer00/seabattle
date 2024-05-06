from Player import *
from Game import *
import tkinter as tk
from tkinter import ttk


class Loader:
    def __init__(self):
        self.game = Game()
        self.game.status_check()
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.title('Морской бой')
        self.cnt_players = 0
        self.entry = ttk.Entry()
        self.entry_name_btn = ttk.Button(command=self.get_name)
        self.context = ttk.Label(text='введите имя первого игрока')
        self.cur_player_map = ttk.Label()
        self.cur_player_radar = ttk.Label()
        self.players = []
        self.entry_setup_btn = ttk.Button(command=self.setup)
        self.playa = None
        self.entry_command_btn = ttk.Button(command=self.command)

    def command(self):
        if self.game.status == 'game':
            self.game.current_player.field.draw_field('map', self)
            self.game.current_player.field.draw_field('radar', self)
            shot_result = self.game.current_player.make_shot(self.game.next_player, self)
            if shot_result == 'miss':
                self.context[
                    'text'] = f'{self.game.current_player.name} промахнулся!\nВаш ход, {self.game.next_player.name}.'
                self.game.switch_players()
                self.game.status_check()
            if shot_result == 'retry':
                self.context['text'] = 'Попробуйте еще раз!'
                self.game.status_check()
                self.cur_player_radar.destroy()
                self.cur_player_map.destroy()
                return
            if shot_result == 'get':
                print(f'Отличный выстрел, {self.game.current_player.name}, продолжайте')
                self.game.status_check()
                self.cur_player_radar.destroy()
                self.cur_player_map.destroy()
                return
            if shot_result == 'kill':
                self.context['text'] = f'Отличный выстрел, {self.game.current_player.name}, продолжайте'
                self.game.status_check()
                self.cur_player_radar.destroy()
                self.cur_player_map.destroy()
                return
        if self.game.status == 'game over':
            self.game.next_player.field.draw_field('map', self)
            self.game.current_player.field.draw_field('map', self)
            self.context['text'] = f'{self.game.current_player.name} выиграл игру!'
        self.game.status_check()

    def setup(self):
        if self.game.ships_setup(self.playa, self):
            if self.playa.name == self.players[1].name:
                self.game.status_check()
                self.entry_setup_btn.destroy()
                self.entry_command_btn.pack()
                return
            self.playa = self.players[1]

    def get_name(self):
        if self.cnt_players == 0:
            self.context['text'] = 'введите имя второго игрока'
            self.players.append(Player(self.entry.get()))
            self.cnt_players += 1
        elif self.cnt_players == 1:
            self.players.append(Player(self.entry.get()))
            self.entry_name_btn.destroy()
            self.entry_setup_btn.pack()
            self.cur_player_map.pack()
            self.context['text'] = ''
            self.game.add_player(Player(self.players[0]), self)
            self.game.add_player(Player(self.players[1]), self)
            self.playa = self.players[0]

    def start_game(self):
        self.entry.pack()
        self.entry_name_btn.pack()
        self.context.pack()
        self.root.mainloop()
