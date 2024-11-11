import tkinter as tk
from tkinter import messagebox
import random
import os

class TennisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tennis Match Simulator")
        self.players = self.read_players('players.txt')
        self.create_widgets()

    def read_players(self, file_name):
        if not os.path.exists(file_name):
            messagebox.showerror("Error", f"Filen {file_name} existerar inte.")
            self.root.destroy()
            return
        
        players = {}
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if len(lines) % 4 != 0:
                messagebox.showerror("Error", "Felaktigt format i spelardatafilen.")
                self.root.destroy()
                return
            
            for i in range(0, len(lines), 4):
                name = lines[i].strip()
                serve_probability = float(lines[i+1].strip())
                won_matches = int(lines[i+2].strip())
                total_matches = int(lines[i+3].strip())
                
                if not (0 <= serve_probability <= 1):
                    messagebox.showerror("Error", f"Felaktig sannolikhet för {name}: {serve_probability}")
                    self.root.destroy()
                    return
                
                players[name] = {
                    'serve_probability': serve_probability,
                    'won_matches': won_matches,
                    'total_matches': total_matches
                }
        return players

    def create_widgets(self):
        tk.Label(self.root, text="Välj två spelare att möta varandra:").pack()
        
        self.player1_var = tk.StringVar(value=list(self.players.keys())[0])
        self.player2_var = tk.StringVar(value=list(self.players.keys())[1])
        
        tk.OptionMenu(self.root, self.player1_var, *self.players.keys()).pack()
        tk.OptionMenu(self.root, self.player2_var, *self.players.keys()).pack()
        
        tk.Button(self.root, text="Starta match", command=self.start_match).pack()
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack()

    def start_match(self):
        player1 = self.player1_var.get()
        player2 = self.player2_var.get()
        
        if player1 == player2:
            messagebox.showerror("Error", "Du måste välja två olika spelare.")
            return
        
        match_winner = self.play_match(player1, player2)
        self.players[match_winner]['won_matches'] += 1
        self.players[player1]['total_matches'] += 1
        self.players[player2]['total_matches'] += 1
        self.display_results()

    def play_match(self, player1, player2):
        sets = {player1: 0, player2: 0}
        server = player1 if random.random() < 0.5 else player2
        
        while sets[player1] < 2 and sets[player2] < 2:
            winner = self.play_set(server, player2 if server == player1 else player1)
            sets[winner] += 1
            self.result_text.insert(tk.END, f"Setvinnare: {winner}\n")
        
        match_winner = player1 if sets[player1] > sets[player2] else player2
        self.result_text.insert(tk.END, f"Matchvinnare: {match_winner}\n")
        return match_winner

    def play_set(self, server, opponent):
        games = {server: 0, opponent: 0}
        
        while True:
            winner = self.play_game(server, opponent)
            games[winner] += 1
            if games[server] >= 6 and games[server] - games[opponent] >= 2:
                return server
            elif games[opponent] >= 6 and games[opponent] - games[server] >= 2:
                return opponent
            server, opponent = opponent, server

    def play_game(self, server, opponent):
        points = {server: 0, opponent: 0}
        
        while True:
            winner = self.play_ball(server, opponent)
            points[winner] += 1
            if points[server] >= 4 and points[server] - points[opponent] >= 2:
                return server
            elif points[opponent] >= 4 and points[opponent] - points[server] >= 2:
                return opponent

    def play_ball(self, server, opponent):
        serve_prob = self.players[server]['serve_probability']
        return server if random.random() < serve_prob else opponent

    def display_results(self):
        sorted_players = sorted(self.players.items(), key=lambda x: x[1]['won_matches'] / x[1]['total_matches'] if x[1]['total_matches'] != 0 else 0, reverse=True)
        self.result_text.insert(tk.END, f"{'Placering':<10} {'Namn':<20} {'Vunna':<10} {'Spelade':<10} {'Andel Vunna':<15}\n")
        for i, (name, data) in enumerate(sorted_players, 1):
            win_ratio = data['won_matches'] / data['total_matches'] if data['total_matches'] != 0 else 0
            self.result_text.insert(tk.END, f"{i:<10} {name:<20} {data['won_matches']:<10} {data['total_matches']:<10} {win_ratio:<15.3f}\n")

root = tk.Tk()
app = TennisApp(root)
root.mainloop()
