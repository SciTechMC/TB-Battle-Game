#version 0.2.0
#developer: SciTechMC
#latest patch notes
#adding an error exempt to run health window, added compatibility to run hp window using py file
#
#
#
import os.path

health_file_path = os.path.abspath(r'.\TBBG-files\TBBG-STM-Health.txt')
health_window_fp = os.path.abspath(r'.\TBBG-files\TBBG-HP-Window.exe')
health_window_fp_python = os.path.abspath(r'.\TBBG-files\TBBG-HP-Window.py')
#fp = filepath

#Main window------------------------------------------------
import time
from rich import print
import random
import math
from dataclasses import dataclass
import subprocess
#define all variables

#player
@dataclass
class Player:
    username :str = ""
    move : str = ""
    health : int = 100
    attack_power : int = 0
    defence_power :int = 0
    crit_chance : str = 1
    defending : bool = False
    winner : bool = False

#AI
class Ai:
    move : str = ""
    health : int = 100
    attack_power : int = 0
    defence_power :int = 0
    crit_chance : str = 1
    defending : bool = False
    winner : bool = False

player = Player
ai = Ai
game_round = 0
health_bars_window = ""
#defined all variables --------------------

def print_options(scenario):
    """ scenario = game / menu """
    match scenario:
        case "menu":
            print()
            print("Welcome to TBBG-STM!")
            print()
            print("1. Start a fight")
            print("2. Exit game")
        case "game:":
            print("[bright_white bold on black]Chose your next move![/bright_white bold on black]")
            print("1. [red bold]Attack[/red bold]")
            print("2. [blue bold]Defend[/blue bold]")
            print("3. [bright_green bold]Heal[/bright_green bold]")
            print()

def move_choice(move, turn):
    """ move = 1-2-3, turn = player / AI """
    match move:
        case 1: #attack
            #player
            if turn == "player":
                player.defending = False

                player.attack_power = random.randint(10,20)
                if random.randint(0,10) == player.crit_chance:
                    player.attack_power *= 2
                    print("You hit a [blue]crit[/blue]!")
                if ai.defending:
                    player.attack_power -= math.floor(player.attack_power * (1 - ai.defence_power))
                    print(f"You [red bold]attacked[/red bold] the AI, but it [blue bold]blocked[/blue bold] your attack so you only did [yellow bold]{player.attack_power} damage[/yellow bold].")
                else:
                    print(f"You [red bold]attacked[/red bold] the AI, doing [red bold]{player.attack_power} damage[/red bold]!")

                ai.health -= player.attack_power

                if ai.health < 0:
                    ai.health = 0

            #AI
            else:
                ai.defending = False

                ai.attack_power = random.randint(8,18)
                if random.randint(0, 10) == ai.crit_chance:
                    ai.attack_power = math.ceil(ai.attack_power*1.75)
                    print("The AI hit a [blue]crit[/blue]!")

                if player.defending:
                    ai.attack_power -= math.floor(ai.attack_power * (1 - player.defence_power))
                    print(f"The AI [red bold]attacked[/red bold] you, but since you [blue bold]blocked[/blue bold] it, only did [yellow bold]{ai.attack_power} damage[/yellow bold]!")
                else:
                    print(f"The AI [red bold]attacked[/red bold] you for [red bold]{ai.attack_power} damage[/red bold]!")

                player.health -= ai.attack_power
                if player.health < 0:
                    player.health = 0

        case 2: #defend
            defence_amount = random.randint(30,60)/100

            #Player
            if turn == "player":
                player.defence_power = defence_amount
                player.defending = True
                print("You are [blue bold]defending[/blue bold]!")

            #AI
            else:
                ai.defence_power = defence_amount
                ai.defending = True
                print("The AI is [blue bold]defending[/blue bold]!")

        case 3: #heal
            if turn == "player":
                player.defending = False

                heal_amount = random.randint(15,25)
                player.health += heal_amount
                if player.health > 100:
                    player.health = 100
                    print("You are now at [bright_green bold]full HP[/bright_green bold]!")
                else:
                    print(f"You [bright_green bold]healed {heal_amount} HP[/bright_green bold]!")

            else:
                ai.defending = False

                heal_amount = random.randint(12,22)
                ai.health += heal_amount
                if ai.health > 100:
                    ai.health = 100
                    print("The AI is now at [bright_green bold]full HP[/bright_green bold]")
                print(f"The AI [bright_green bold]healed {heal_amount} HP[/bright_green bold]!")

def player_turn():
    print_options("game")
    player.move = 0
    player.move = input("> ")
    if not player.move:
        player_turn()
    elif 1 <= int(player.move) <= 3:
        move_choice(int(player.move), "player")
    else:
        player_turn()

    return False

def ai_turn():
    print("[bright_white bold on black]AI's turn...[/bright_white bold on black]")
    time.sleep(2)

    #AI choice making
    if ai.health > 50:
        ai.move = random.choice([1,1,1,1,2,3])
    elif ai.health < 30:
        if player.health < 45:
            ai.move = random.choice([1,1,1,2])
            if player.move != 1:
                ai.move = random.choice([1,1,3])

        if ai.health < 10:
            ai.move = 3
            if player.health < ai.health:
                ai.move = 1

        else:
            ai.move = random.choice([3,3,2,1])
    else:
        ai.move = random.choice([1,1,2,3])

    move_choice(ai.move, "ai")
    return False

def reset_game():
    global game_round
    game_round += 1
    player.winner = False
    ai.winner = False
    ai.health = 100
    player.health = 100

def battle_arena():

    print("Welcome Fighter! Please input your username to personalize your play experience!")
    username = input("Username: ")
    print(f"Good to see you {username}!")

    global health_bars_window
    reset_game()
    print()
    print(f"[red bold italic]ROUND {game_round}[/red bold italic]")
    time.sleep(1)
    print(f"[red]FIGHT[/red]")
    print()

    if game_round == 1:
        try:
            health_bars_window = subprocess.Popen(health_window_fp, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception:
            try:
                subprocess.Popen(["start", "cmd", "/k", "python", health_window_fp_python], shell=True)
            except Exception:
                print(f"[red bold italic]Unable to find TBBG-HP-Window.exe/.py file! Please check your game files!")
                time.sleep(9999)

    while player.health > 0 and ai.health > 0:

        with open(health_file_path, 'w') as healthFile:
            healthFile.write(f"{player.health},{ai.health}")

        if player.health <= 0:
            ai.winner = True
            break
        player_turn()
        print()

        with open(health_file_path, 'w') as healthFile:
            healthFile.write(f"{player.health},{ai.health}")

        if ai.health <= 0:
            player.winner = True
            break
        ai_turn()
        print()


    if player.winner:
        print("[green bold]You WON! Well done![/green bold]")
        if input("The AI would like to have a rematch, do you accept it?(y/n)") == "y":
            battle_arena()
    else:
        print("[red]You lost![/red] Would you like a rematch against the AI?")
        if input("(y/n)") == "y":
            battle_arena()

    health_bars_window.terminate()

def main_menu():
    with open(health_file_path, 'w') as healthFile:
        healthFile.write(f"{player.health},{ai.health}")
    print_options("menu")
    menu_choice = int(input())
    match menu_choice:
        case 1:
            battle_arena()
        case 2:
            return
        case _:
            print("Invalid choice. Please try again.")
            main_menu()

if __name__ == '__main__':
    main_menu()