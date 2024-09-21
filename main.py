import time
from rich import print
import random
import math
from dataclasses import dataclass
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
#defined all variables --------------------

def print_options():
    print("Chose your next move!")
    print("1. Attack")
    print("2. Defend")
    print("3. Heal")
    print()

def move_choice(move, turn):
    match move:
        case 1: #attack
            #player
            if turn == "player":
                player.defending = False

                player.attack_power = random.randint(10,20)
                if random.randint(0,10) == player.crit_chance:
                    player.attack_power *= 2
                    print("You hit a crit!")
                if ai.defending:
                    player.attack_power -= math.floor(player.attack_power * (1 - ai.defence_power))
                    print(f"You attacked the AI, but it blocked your attack so you only did {player.attack_power} damage.")
                else:
                    print(f"You attack the AI, doing {player.attack_power} damage!")
                ai.health -= player.attack_power
                if ai.health < 0:
                    ai.health = 0

            #AI
            else:
                ai.defending = False

                ai.attack_power = random.randint(8,18)
                if random.randint(0, 10) == player.crit_chance:
                    ai.attack_power *= 1.75
                    print("The AI hit a crit!")
                if player.defending:
                    ai.attack_power -= math.floor(ai.attack_power * (1 - player.defence_power))
                    print(f"The AI attacked you, but since you blocked it, only did {ai.attack_power} damage!")
                else:
                    print(f"The AI attacked you for {ai.attack_power} damage!")
                player.health -= ai.attack_power
                if player.health < 0:
                    player.health = 0

        case 2: #defend
            defence_amount = random.randint(30,60)/100

            #Player
            if turn == "player":
                player.defence_power = defence_amount
                player.defending = True
                print("You are defending the AI's next attack.")

            #AI
            else:
                ai.defence_power = defence_amount
                ai.defending = True
                print("The AI is defending your next attack.")

        case 3: #heal
            if turn == "player":
                player.defending = False

                heal_amount = random.randint(15,25)
                player.health += heal_amount
                if player.health > 100:
                    player.health = 100
                    print("You are now at full HP!")
                else:
                    print(f"You healed {heal_amount} HP!")

            else:
                ai.defending = False

                heal_amount = random.randint(12,22)
                ai.health += heal_amount
                if ai.health > 100:
                    ai.health = 100
                print(f"The AI healed {heal_amount} HP!")


    print()
    print(f"Your health: {player.health}")
    print(f"AI health: {ai.health}")
    print()

def player_turn():
    print_options()
    player.move = 0
    player.move = int(input("> "))
    if 1 <= player.move <= 3:
        move_choice(player.move, "player")
    else: player_turn()

    return False

def ai_turn():
    print("AI's turn...")
    time.sleep(2)

    #AI choice making
    if ai.health > 50:
        ai.move = 1
    elif ai.health < 30:
        ai.move = 3
    elif player.health <= 40:
        ai.move = 1
    else:
        ai.move = 2

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
    reset_game()
    print()
    print(f"[red bold italic]ROUND {game_round}[/red bold italic]")
    time.sleep(1)
    print(f"[red]FIGHT[/red]")
    print()
    while player.health > 0 and ai.health > 0:
        if player.health <= 0:
            ai.winner = True
            break
        player_turn()
        if ai.health <= 0:
            player.winner = True
            break
        ai_turn()

    if player.winner:
        print("[green bold]You WON! Well done![/green bold]")
        if input("The AI would like to have a rematch, do you accept it?(y/n)") == "y":
            battle_arena()
    else:
        print("[red]You lost![/red] Would you like a rematch against the AI?")
        if input("(y/n)") == "y":
            battle_arena()

if __name__ == '__main__':
    print("Welcome Fighter! Please input your username to personalize your play experience!")
    username = input("Username: ")
    print(f"Good to see your {username}!")

    battle_arena()