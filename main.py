from Player import *
from Game import *

if __name__ == '__main__':
    players = [Player(input("Введите имя: ")), Player(input("Введите имя: "))]
    game = Game()
    game.status_check()
    game.add_player(players[0])
    game.add_player(players[1])
    while True:
        if game.status == 'game':
            Game.clear_screen()
            print('Ждем приказа: ')
            game.draw()
            shot_result = game.current_player.make_shot(game.next_player)
            if shot_result == 'miss':
                print(f'{game.current_player.name} промахнулся!')
                print(f'Ваш ход, {game.next_player.name}.')
                game.switch_players()
                game.status_check()
                continue
            if shot_result == 'retry':
                print('Попробуйте еще раз!')
                game.status_check()
                continue
            if shot_result == 'get':
                print(f'Отличный выстрел, {game.current_player.name}, продолжайте')
                game.status_check()
                continue
            if shot_result == 'kill':
                print('Корабль противника уничтожен!')
                game.status_check()
                continue
        if game.status == 'game over':
            Game.clear_screen()
            game.next_player.field.draw_field('map')
            game.current_player.field.draw_field('map')
            print(f'{game.current_player.name} выиграл игру!')
            break
        game.status_check()

    input()
