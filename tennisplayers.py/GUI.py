import os
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches
        self.games_won = 0
        self.games_lost = 0
        self.sets_won = 0

    def win_percentage(self):
        return self.wins / self.matches if self.matches > 0 else 0

    def update_result(self, won):
        self.matches += 1
        if won:
            self.wins += 1

    def __str__(self):
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

def read_stats_from_file(filename):
    players = []
    if not os.path.isfile(filename):
        messagebox.showerror("File Error", "File not found!")
        return players

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 4):
                name = lines[i].strip()
                serve_win_prob = float(lines[i+1].strip())
                wins = int(lines[i+2].strip())
                matches = int(lines[i+3].strip())
                players.append(Player(name, serve_win_prob, wins, matches))
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
    return players

def write_players_to_file(filename, players):
    with open(filename, "w") as f:
        for player in players:
            f.write(str(player) + "\n")

def play_point(serving_player):
    return random.random() < serving_player.serve_win_prob

def play_game(player1, player2, serving_player, display_callback):
    points = [0, 15, 30, 40]
    player1_score = 0
    player2_score = 0

    while True:
        # Om servande spelar vinner poängen
        if play_point(serving_player):
            if serving_player == player1:
                player1_score += 1
            else:
                player2_score += 1
        else:
            if serving_player == player1:
                player2_score += 1
            else:
                player1_score += 1

        # Deuce och Advantage hantering
        if player1_score >= 3 and player2_score >= 3:
            if player1_score == player2_score:
                display_callback("Deuce")
            elif player1_score == player2_score + 1:
                display_callback(f"Advantage {player1.name}")
            elif player2_score == player1_score + 1:
                display_callback(f"Advantage {player2.name}")
        else:
            # Poäng inom 0-40 för vardera spelare
            score1 = points[min(player1_score, 3)]
            score2 = points[min(player2_score, 3)]
            display_callback(f"{score1} - {score2}")

        # Kontrollera om någon vinner spelet
        if player1_score >= 4 and player1_score > player2_score + 1:
            display_callback(f"Game to {player1.name}")
            return player1
        elif player2_score >= 4 and player2_score > player1_score + 1:      
            display_callback(f"Game to {player2.name}")
            return player2

        time.sleep(1)  # Paus för att simulera matchens tempo

def play_set(player1, player2, display_callback):
    player1.games_won = 0
    player2.games_won = 0
    serving_player = player1 if random.choice([True, False]) else player2

    while True:
        display_callback(f"\n{serving_player.name} to serve")
        game_winner = play_game(player1, player2, serving_player, display_callback)

        # Uppdatera antalet vunna games
        if game_winner == player1:
            player1.games_won += 1
        else:
            player2.games_won += 1

        display_callback(f"Current game score: {player1.name} {player1.games_won} - {player2.name} {player2.games_won}")

        # Kontrollera om någon har vunnit setet
        if player1.games_won >= 6 and player1.games_won >= player2.games_won + 2:
            display_callback(f"Set to {player1.name}")
            return player1
        elif player2.games_won >= 6 and player2.games_won >= player1.games_won + 2:
            display_callback(f"Set to {player2.name}")
            return player2

        # Växla serverande spelare
        serving_player = player2 if serving_player == player1 else player1


def play_match(player1, player2, display_callback):
    player1.sets_won = 0
    player2.sets_won = 0

    while player1.sets_won < 2 and player2.sets_won < 2:
        display_callback(f"\nStarting new set: {player1.name} {player1.sets_won} - {player2.name} {player2.sets_won}")
        set_winner = play_set(player1, player2, display_callback)

        # Uppdatera antal vunna set
        if set_winner == player1:
            player1.sets_won += 1
        else:
            player2.sets_won += 1

        display_callback(f"Set score: {player1.sets_won} - {player2.sets_won} in sets")
        time.sleep(2)  # Paus för att simulera tid mellan set

    # Vinnaren av matchen
    match_winner = player1 if player1.sets_won > player2.sets_won else player2
    display_callback(f"\nMatch winner: {match_winner.name}")
    display_callback(f"Final score: {player1.sets_won} - {player2.sets_won} in sets")

    return match_winner  # Lägg till denna rad

class TennisApp:    
    def __init__(self, root):
        self.root = root
        self.root.title("Tennis Match Simulator")
        self.filename = "playerdata.txt"
        self.players = read_stats_from_file(self.filename)
        self.create_widgets()

    def create_widgets(self):
        self.player1_label = tk.Label(self.root, text="Select Player 1")
        self.player1_label.pack()
        
        # Dropdowns for player selection
        player_names = [player.name for player in self.players]  # Get player names for dropdown
        self.player1_combo = ttk.Combobox(self.root, values=player_names)
        self.player1_combo.pack()

        self.player2_label = tk.Label(self.root, text="Select Player 2")
        self.player2_label.pack()
        self.player2_combo = ttk.Combobox(self.root, values=player_names)
        self.player2_combo.pack()

        self.start_button = tk.Button(self.root, text="Start Match", command=self.start_match)
        self.start_button.pack()

        self.output_text = tk.Text(self.root, height=20, width=50)
        self.output_text.pack()

    def display_callback(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()

    def start_match(self):
        player1_name = self.player1_combo.get()
        player2_name = self.player2_combo.get()

        if not player1_name or not player2_name or player1_name == player2_name:
            messagebox.showerror("Selection Error", "Please select two different players.")
            return

        player1 = next(player for player in self.players if player.name == player1_name)
        player2 = next(player for player in self.players if player.name == player2_name)

        match_winner = play_match(player1, player2, self.display_callback)

        player1.update_result(match_winner == player1)
        player2.update_result(match_winner == player2)
        write_players_to_file(self.filename, self.players)

        messagebox.showinfo("Match Over", f"The winner is {match_winner.name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TennisApp(root)
    root.mainloop()
