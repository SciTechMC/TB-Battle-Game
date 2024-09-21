import time
import os
from rich.progress import Progress, BarColumn, TextColumn

def read_health_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                player_health, ai_health = map(int, f.readline().strip().split(','))
            except ValueError:
                time.sleep(1)
            else:
                return player_health, ai_health
    else:
        return 100, 80  # Default values if the file doesn't exist

def display_health_bars(file_path):
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.completed}/{task.total} HP"
    ) as progress:
        player_health = progress.add_task("[cyan bold]Your health:[/cyan bold]", total=100, completed=100)
        ai_health = progress.add_task("[magenta bold]AI health:[/magenta bold]", total=100, completed=100)

        while True:
            player, ai = read_health_from_file(file_path)
            progress.update(player_health, completed=player)
            progress.update(ai_health, completed=ai)
            time.sleep(0.5)

if __name__ == "__main__":
    time.sleep(3)
    health_file_path = "health.txt"
    display_health_bars(health_file_path)
