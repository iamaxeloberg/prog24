import os
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

class Player:
    def __init__(self, name, serve_win_prob, wins=0, matches=0):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches
        self.games_won = 0
        self.sets_won = 0

    def update_result(self, won):
        self.matches += 1
        self.wins += int(won)

    def __str__(self):
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

def read_stats_from_file(filename):
    if not os.path.isfile(filename):
        messagebox.showerror("File Error", "File not found!")
        return []
    try:
        with open(filename, "r") as f:
            return [
                Player(*line.strip().split("\n"))
                for line in zip(*[f] * 4)
            ]
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
        return []

def write_players_to_file(filename, players):
    with open(filename, "w") as f:
        f.writelines(str(player) + "\n" for player in players)

def play_point(player):
    return random.random() < player.serve_win_prob

def play_game(player1, player2, serving_player, display_callback):
    score = [0, 0]  # [player1, player2]
    points = [0, 15, 30, 40]
    while True:
        winner = 0 if play_point(serving_player) else 1
        score[winner] += 1 if serving_player == [player1, player2][winner] else 0

        if min(score) >= 3:
            if score[0] == score[1]:
                display_callback("Deuce")
            else:
                advantage = [player1, player2][score.index(max(score))]
                display_callback(f"Advantage {advantage.name}")

        display_callback(f"{points[min(score[0], 3)]} - {points[min(score[1], 3)]}")

        if max(score) >= 4 and abs(score[0] - score[1]) > 1:
            winner = player1 if score[0] > score[1] else player2
            display_callback(f"Game to {winner.name}")
            return winner
        time.sleep(1)

def play_set(player1, player2, display_callback):
    player1.games_won = player2.games_won = 0
    serving_player = random.choice([player1, player2])
    while True:
        display_callback(f"\n{serving_player.name} to serve")
        winner = play_game(player1, player2, serving_player, display_callback)
        winner.games_won += 1

        display_callback(f"Current score: {player1.name} {player1.games_won} - {player2.name} {player2.games_won}")

        if winner.games_won >= 6 and abs(player1.games_won - player2.games_won) >= 2:
            display_callback(f"Set to {winner.name}")
            return winner
        serving_player = player2 if serving_player == player1 else player1

def play_match(player1, player2, display_callback):
    player1.sets_won = player2.sets_won = 0
    while max(player1.sets_won, player2.sets_won) < 2:
        display_callback(f"\nStarting new set: {player1.name} {player1.sets_won} - {player2.name} {player2.sets_won}")
        winner = play_set(player1, player2, display_callback)
        winner.sets_won += 1
        display_callback(f"Set score: {player1.name} {player1.sets_won} - {player2.name} {player2.sets_won}")
        time.sleep(2)

    match_winner = player1 if player1.sets_won > player2.sets_won else player2
    display_callback(f"\nMatch winner: {match_winner.name}")
    display_callback(f"Final score: {player1.sets_won} - {player2.sets_won}")
    return match_winner

class TennisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tennis Match Simulator")
        self.filename = "C:/Users/stadi/OneDrive/Skrivbord/github/prog24/tennisplayers.py/playerdata.txt"
        self.players = read_stats_from_file(self.filename)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Player 1").pack()
        self.player1_combo = ttk.Combobox(self.root, values=[p.name for p in self.players])
        self.player1_combo.pack()
        tk.Label(self.root, text="Select Player 2").pack()
        self.player2_combo = ttk.Combobox(self.root, values=[p.name for p in self.players])
        self.player2_combo.pack()
        tk.Button(self.root, text="Start Match", command=self.start_match).pack()
        self.output_text = tk.Text(self.root, height=20, width=50)
        self.output_text.pack()

    def display_callback(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()

    def start_match(self):
        player1 = next(p for p in self.players if p.name == self.player1_combo.get())
        player2 = next(p for p in self.players if p.name == self.player2_combo.get())

        if not player1 or not player2 or player1 == player2:
            messagebox.showerror("Selection Error", "Please select two different players.")
            return

        winner = play_match(player1, player2, self.display_callback)
        player1.update_result(winner == player1)
        player2.update_result(winner == player2)
        write_players_to_file(self.filename, self.players)
        messagebox.showinfo("Match Over", f"The winner is {winner.name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TennisApp(root)
    root.mainloop()