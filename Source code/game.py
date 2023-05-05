import random
import os
import time
import pygame
from pynput import keyboard

pygame.mixer.init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    for row in board:
        print(''.join(row))

def update_record(score, difficulty):
    record_files = {
        1: "record_easy.txt",
        2: "record_medium.txt",
        3: "record_hard.txt"
    }

    record_file = record_files[difficulty]

    if not os.path.exists(record_file):
        with open(record_file, "w") as file:
            file.write(str(score))
        return score

    with open(record_file, "r") as file:
        record_content = file.read().strip()
        record = int(record_content) if record_content else 0

    if score > record:
        with open(record_file, "w") as file:
            file.write(str(score))
        return score
    else:
        return record

def update_board(board, player_position, egg_position):
    for i in range(4):
        if player_position + i < len(board[-1]):
            board[-1][player_position + i] = 'V'
    board[egg_position[0]][egg_position[1]] = 'O'

def on_key_release(key, player_position, board, egg_position):
    if key == keyboard.Key.left and player_position[0] > 0:
        player_position[0] -= 1
        update_board(board, player_position[0], egg_position)
    elif key == keyboard.Key.right and player_position[0] < len(board[-1]) - 4:
        player_position[0] += 1
        update_board(board, player_position[0], egg_position)

def choose_difficulty():
    print("Выберите уровень сложности:")
    print("1. Легкий")
    print("2. Средний")
    print("3. Сложный")
    difficulty = int(input("Введите число от 1 до 3: "))
    while difficulty not in [1, 2, 3]:
        print("Неверный выбор. Пожалуйста, выберите число от 1 до 3.")
        difficulty = int(input("Введите число от 1 до 3: "))
    return difficulty

def main():
    print("Добро пожаловать в игру 'Ну, погоди!'")
    print("Управляйте корзинкой с помощью клавиш со стрелками влево и вправо.")
    print("Наберите 10 яиц, чтобы выиграть. У вас есть 3 попытки.")
    difficulty = choose_difficulty()
    background_music_files = {
        1: "background_music_easy.mp3",
        2: "background_music_medium.mp3",
        3: "background_music_hard.mp3",
    }
    egg_speeds = {
        1: 0.6,
        2: 0.4,
        3: 0.15,
    }
    pygame.mixer.music.load(background_music_files[difficulty])
    pygame.mixer.music.play(-1)
    board = [[' ' for _ in range(20)] for _ in range(10)]
    player_position = [8]
    egg_position = [0, random.randint(0, 19)]
    score = 0
    missed_eggs = 0
    max_missed_eggs = 3
    start_time = time.time()
    game_start_time = start_time
    egg_speed = egg_speeds[difficulty]

    with keyboard.Listener(on_release=lambda key: on_key_release(key, player_position, board, egg_position)) as listener:
        while missed_eggs < max_missed_eggs:
            elapsed_time = time.time() - start_time

            if elapsed_time > egg_speed:
                start_time = time.time()

                egg_position[0] += 1
                if egg_position[0] == len(board) - 1:
                    if egg_position[1] in range(player_position[0], player_position[0] + 4):
                        score += 1
                        egg_caught_sound = pygame.mixer.Sound("egg_caught.wav")
                        egg_caught_sound.play()
                    else:
                        missed_eggs += 1
                    egg_position = [0, random.randint(0, 19)]

                board = [[' ' for _ in range(20)] for _ in range(10)]

            clear_screen()
            print(f"Score: {score}")
            print(f"Missed eggs: {missed_eggs}")
            game_elapsed_time = time.time() - game_start_time
            print(f"Current time: {game_elapsed_time:.2f} seconds")
            update_board(board, player_position[0], egg_position)
            print_board(board)
            time.sleep(0.05)

            if not listener.running:
                break
        if missed_eggs >= max_missed_eggs:
            print("К сожалению, вы разбили яйца. Попробуйте еще раз!")
    pygame.mixer.music.stop()
    record = update_record(score, difficulty)
    if record == score:
        print("Поздравляем! Вы обновили рекорд!")
    print(f"Ваш счет: {score}")
    print(f"Рекорд: {record} на сложности: {difficulty}")

if __name__ == "__main__":
    main()
