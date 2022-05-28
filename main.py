import RPi.GPIO as GPIO
import modules as mod
import time
import threading
from timeit import default_timer as timer

buzzer = 7
greenLed = 25
redLed = 11

mod.initialize(buzzer, greenLed, redLed)


class Player:
    def __init__(self, name, lives, time, score):
        self.name = name
        self.lives = lives
        self.time = time
        self.score = score


def click_to_finish():
    global finished
    enter_to_finish = input("Press The Enter When You Are Finished...\n")
    finished = True
    return finished


finish = None
try:
    n = int(input("Enter number of players: "))
    while n > 9:
        print("Sorry, max number of players is 9.")
        n = int(input("Enter number of players: "))
    players = []
    for p in range(n):
        player_name = input(f"Enter name of {p + 1}. player: ")
        while len(player_name) > 15:
            print("Sorry, max length of player name is 15.")
            player_name = input(f"Enter name of {p + 1}. player: ")
        player = Player(player_name, 5, 0, 0)
        players.append(player)

    for player in players:
        global finished
        finished = False

        mod.reset_items(buzzer, greenLed, redLed)
        print(f"{player.name} it's your turn!")
        message = input("Press The Enter To Start...")
        mod.light_on_num(player.lives)
        start = timer()
        print(f"{player.name} you have {player.lives} lives.")
        finish = threading.Thread(target=click_to_finish)
        finish.start()

        last_pressed = False
        while True:
            if finished:
                end = timer()
                elapsed_time = end - start
                player.time = elapsed_time
                time_score = 120 / elapsed_time
                player.score = player.lives * 20 + time_score
                break

            if player.lives == 0:
                break

            btn_pressed = not GPIO.input(8)

            if btn_pressed and not last_pressed:
                GPIO.output(greenLed, GPIO.LOW)
                GPIO.output(buzzer, GPIO.HIGH)
                GPIO.output(redLed, GPIO.HIGH)

                mod.light_off_num(player.lives)
                player.lives = player.lives - 1
                mod.light_on_num(player.lives)
                print(f"{player.name} you have {player.lives} lives.")

            elif btn_pressed and last_pressed:
                GPIO.output(greenLed, GPIO.LOW)
                GPIO.output(buzzer, GPIO.HIGH)
                GPIO.output(redLed, GPIO.HIGH)

            else:
                GPIO.output(buzzer, GPIO.LOW)
                GPIO.output(redLed, GPIO.LOW)
                GPIO.output(greenLed, GPIO.HIGH)

            last_pressed = btn_pressed
            time.sleep(0.5)

        print(f"{player.name} you are finished!\n")

    for p_one in range(0, len(players) - 1):
        for p_two in range(p_one, len(players)):
            if players[p_one].score < players[p_two].score:
                t = players[p_one]
                players[p_one] = players[p_two]
                players[p_two] = t

    s = ' '
    buffer = 15
    print(f"|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|")
    print(f"|{s * 2}Leaderboard{s * 2}|{s * 6}Name{s * 5}|{s * 5}Lives{s * 5}|{s * 6}Time{s * 5}|{s * 5}Score{s * 5}|")
    print(f"|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|")
    for p in range(len(players)):
        name_len = len(players[p].name)
        available_name_space = buffer - name_len

        time_len = len(str(round(players[p].time, 2)))
        available_time_space = buffer - time_len

        score_len = len(str(int(players[p].score)))
        available_score_space = buffer - score_len

        print(f"|{s * 6}{p + 1}.{s * 7}|{s * (available_name_space // 2)}{players[p].name}"
              f"{s * (available_name_space // 2 + available_name_space % 2)}|"
              f"{s * 7}{players[p].lives}{s * 7}|{s * (available_time_space // 2)}"
              f"{round(players[p].time, 2)}{s * (available_time_space // 2 + available_time_space % 2)}|"
              f"{s * (available_score_space // 2)}{int(players[p].score)}"
              f"{s * (available_score_space // 2 + available_score_space % 2)}|")
        print(f"|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|{'-' * buffer}|")

except:
    mod.reset_items(buzzer, greenLed, redLed)
    if finish is not None:
        finish.join()

GPIO.cleanup()
