import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from typing import List, Tuple, Optional
import os

class TennisScore:
    POINTS = {0: "0", 1: "15", 2: "30", 3: "40"}
    
    def __init__(self):
        self.points = [0, 0]  # [player1, player2]
        self.games = [0, 0]
        self.sets = [0, 0]
        self.deuce = False
        self.advantage = None  # None, 0 for player1, 1 for player2
        
    def add_point(self, player_index: int) -> bool:
        """Returns True if the game is won"""
        if self.deuce:
            if self.advantage is None:
                self.advantage = player_index
            elif self.advantage == player_index:
                self.points = [0, 0]
                self.deuce = False
                self.advantage = None
                return True
            else:
                self.advantage = None
            return False
            
        if self.points[player_index] == 3:
            if self.points[1-player_index] == 3:
                self.deuce = True
                return False
            self.points = [0, 0]
            return True
            
        if self.points[player_index] < 3:
            self.points[player_index] += 1
            if self.points[player_index] == 3 and self.points[1-player_index] < 3:
                self.points = [0, 0]
                return True
        return False

    def add_game(self, player_index: int) -> bool:
        """Returns True if the set is won"""
        self.games[player_index] += 1
        if self.games[player_index] >= 6 and self.games[player_index] - self.games[1-player_index] >= 2:
            self.games = [0, 0]
            self.sets[player_index] += 1
            return True
        return False

    def get_score_string(self) -> str:
        if self.deuce:
            if self.advantage is None:
                return "Lika"
            return f"Fördel {['Spelare 1', 'Spelare 2'][self.advantage]}"
        return f"{self.POINTS[self.points[0]]} - {self.POINTS[self.points[1]]}"

    def get_game_string(self) -> str:
        return f"{self.games[0]} - {self.games[1]}"

    def get_set_string(self) -> str:
        return f"{self.sets[0]} - {self.sets[1]}"

class Player:
    def __init__(self, name: str, serve_probability: float, wins: int = 0, matches_played: int = 0):
        self.name = name
        self.serve_probability = serve_probability
        self.wins = wins
        self.matches_played = matches_played

    @property
    def win_percentage(self) -> float:
        if self.matches_played == 0:
            return 0.0
        return self.wins / self.matches_played

class TennisMatch:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.score = TennisScore()
        self.current_server = random.randint(0, 1)
        self.game_count = 0

    def play_point(self) -> Tuple[int, str]:
        server = self.player1 if self.current_server == 0 else self.player2
        rand = random.random()
        winner_idx = self.current_server if rand < server.serve_probability else 1 - self.current_server
        
        game_won = self.score.add_point(winner_idx)
        if game_won:
            self.game_count += 1
            self.current_server = 1 - self.current_server
            set_won = self.score.add_game(winner_idx)
            if set_won and self.score.sets[winner_idx] == 2:
                return winner_idx, "match"
            elif set_won:
                return winner_idx, "set"
            return winner_idx, "game"
        return winner_idx, "point"

class TennisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tennis Match Simulator")
        self.setup_gui()
        self.players = self.load_players("tennis_players.txt")
        self.current_match = None
        self.update_speed = 1.0  # seconds between points

    def setup_gui(self):
        # Player selection frame
        select_frame = ttk.LabelFrame(self.root, text="Välj spelare", padding="10")
        select_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(select_frame, text="Spelare 1:").grid(row=0, column=0, padx=5, pady=5)
        self.player1_var = tk.StringVar()
        self.player1_combo = ttk.Combobox(select_frame, textvariable=self.player1_var)
        self.player1_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(select_frame, text="Spelare 2:").grid(row=1, column=0, padx=5, pady=5)
        self.player2_var = tk.StringVar()
        self.player2_combo = ttk.Combobox(select_frame, textvariable=self.player2_var)
        self.player2_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Score frame
        score_frame = ttk.LabelFrame(self.root, text="Poängställning", padding="10")
        score_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.score_label = ttk.Label(score_frame, text="", font=("Courier", 14))
        self.score_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Control frame
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Button(control_frame, text="Starta match", command=self.start_match).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Visa ranking", command=self.show_rankings).grid(row=0, column=1, padx=5, pady=5)
        
        # Speed control
        ttk.Label(control_frame, text="Hastighet:").grid(row=1, column=0, padx=5, pady=5)
        self.speed_scale = ttk.Scale(control_frame, from_=0.1, to=2.0, orient="horizontal")
        self.speed_scale.set(1.0)
        self.speed_scale.grid(row=1, column=1, padx=5, pady=5)

    def load_players(self, filename: str) -> List[Player]:
        players = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                while True:
                    name = file.readline().strip()
                    if not name:
                        break
                    serve_prob = float(file.readline().strip())
                    wins = int(file.readline().strip())
                    matches = int(file.readline().strip())
                    players.append(Player(name, serve_prob, wins, matches))
            
            # Update comboboxes
            player_names = [p.name for p in players]
            self.player1_combo['values'] = player_names
            self.player2_combo['values'] = player_names
            
            return players
        except Exception as e:
            messagebox.showerror("Fel", f"Kunde inte läsa spelare från fil: {e}")
            return []

    def save_players(self):
        try:
            with open("tennis_players.txt", 'w', encoding='utf-8') as file:
                for player in self.players:
                    file.write(f"{player.name}\n")
                    file.write(f"{player.serve_probability}\n")
                    file.write(f"{player.wins}\n")
                    file.write(f"{player.matches_played}\n")
        except Exception as e:
            messagebox.showerror("Fel", f"Kunde inte spara spelardata: {e}")

    def update_score_display(self):
        if not self.current_match:
            return
            
        score = self.current_match.score
        score_text = f"""
{self.current_match.player1.name:<15} vs {self.current_match.player2.name}
Sets:  {score.get_set_string()}
Games: {score.get_game_string()}
Score: {score.get_score_string()}
"""
        self.score_label.config(text=score_text)

    def play_point(self):
        if not self.current_match:
            return
            
        winner_idx, result = self.current_match.play_point()
        self.update_score_display()
        
        if result == "match":
            winner = self.current_match.player1 if winner_idx == 0 else self.current_match.player2
            loser = self.current_match.player2 if winner_idx == 0 else self.current_match.player1
            winner.wins += 1
            winner.matches_played += 1
            loser.matches_played += 1
            self.save_players()
            messagebox.showinfo("Match slut", f"{winner.name} vann matchen!")
            self.current_match = None
        else:
            self.root.after(int(self.speed_scale.get() * 1000), self.play_point)

    def start_match(self):
        if self.current_match:
            return
            
        player1_name = self.player1_var.get()
        player2_name = self.player2_var.get()
        
        if player1_name == player2_name:
            messagebox.showerror("Fel", "Välj två olika spelare!")
            return
            
        player1 = next((p for p in self.players if p.name == player1_name), None)
        player2 = next((p for p in self.players if p.name == player2_name), None)
        
        if not player1 or not player2:
            messagebox.showerror("Fel", "Välj giltiga spelare!")
            return
            
        self.current_match = TennisMatch(player1, player2)
        self.update_score_display()
        self.play_point()

    def show_rankings(self):
        sorted_players = sorted(self.players, key=lambda x: x.win_percentage, reverse=True)
        ranking_text = "Placering  Namn            Vunna  Spelade  Andel vunna\n"
        ranking_text += "=" * 55 + "\n"
        
        for i, player in enumerate(sorted_players, 1):
            ranking_text += f"{i:<10} {player.name:<15} {player.wins:<7} {player.matches_played:<8} {player.win_percentage:.3f}\n"
        
        messagebox.showinfo("Ranking", ranking_text)

    def run(self):
        self.root.mainloop()

# [Tidigare kod förblir densamma fram till main]

if __name__ == "__main__":
    # Ändrar sökvägen till den specificerade filen
    filepath = "/Users/axeloberg/Documents/GitHub/prog24/tennisfolder/playerdata.txt"
    app = TennisGUI()
    # Uppdaterar load_players anropet i TennisGUI.__init__
    app.players = app.load_players(filepath)
    # Uppdaterar save_players metoden i TennisGUI klassen
    def save_players(self):
        try:
            with open("/Users/axeloberg/Documents/GitHub/prog24/tennisfolder/playerdata.txt", 'w', encoding='utf-8') as file:
                for player in self.players:
                    file.write(f"{player.name}\n")
                    file.write(f"{player.serve_probability}\n")
                    file.write(f"{player.wins}\n")
                    file.write(f"{player.matches_played}\n")
        except Exception as e:
            messagebox.showerror("Fel", f"Kunde inte spara spelardata: {e}")
    
    # Ersätter den gamla save_players metoden
    TennisGUI.save_players = save_players
    
    app.run()