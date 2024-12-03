import os
import random
import time

class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches
        self.games_won = 0 
        self.games_lost = 0

    def win_percentage(self):
        if self.matches > 0 :
            return self.wins / self.matches
        else:
            return "N/A"
        
    def uppdated_result(self, won):
        self.matches += 1
        if won:
            self.wins += 1

    def __str__(self):
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

def read_stats_from_file(filename):
    players = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            name = lines[i].strip()
            serve_win_prob = float(lines[i+1].strip())
            wins = int(lines[i+2].strip())
            matches = int(lines[i+3].strip())
            players.append(Player(name, serve_win_prob, wins, matches))
    return players  

def write_players_to_file(filename, players):
    with open(filename, "w") as f:
        for player in players:
            f.write(str(player)+ "\n")
        
def display_players(players):
    print("Available players:")
    for i, player in enumerate(players):
        win_percentage = player.win_percentage() if player.matches > 0 else 0
        print(f"{i+1}. {player.name} - Wins: {player.wins}, Matches: {player.matches}, Win Percentage: {player.win_percentage():.3f}")
    
def select_player(players, prompt):
    while True:
        try:
            index = int(input(prompt)) - 1
            if 0 <= index < len(players):
                return players[index]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def update_match_result(player1, player2, winner_name):
    if player1.name == winner_name:
        player1.uppdated_result(True)
        player2.uppdated_result(False)
    elif player2.name == winner_name:
        player1.uppdated_result(False)
        player2.uppdated_result(True)

def sort_players_by_win_percentage(players):
    return sorted(players, key=lambda p: p.win_percentage(), reverse=True)

def play_point(serving_player, receiving_player):
    # Nu tar denna funktion båda spelarna och beräknar poängen baserat på servern.
    return random.random() < serving_player.serve_win_prob

def play_game(player1, player2):
    points = [0, 15, 30, 40]
    player1_score = 0
    player2_score = 0
    serving_player = player1  # Start with player1 serving
    
    while True:
        # Player wins a point based on their serve probability
        if play_point(serving_player, player2 if serving_player == player1 else player1):
            player1_score += 1
        else:
            player2_score += 1
        
        if player1_score >= 4 and player1_score > player2_score + 1:
            print(f"Game to {player1.name}")
            return player1
        elif player2_score >= 4 and player2_score > player1_score + 1:
            print(f"Game to {player2.name}")
            return player2 
        
        if player1_score >= 3 and player2_score >= 3:
            if player1_score == player2_score:
                print("Deuce")
            elif player1_score > player2_score:
                print(f"Advantage {player1.name}")
            else:
                print(f"Advantage {player2.name}")
        else:
            print(f"{points[player1_score]} - {points[player2_score]}")


def play_set(player1, player2):
    player1.games_won = 0
    player2.games_won = 0
    serving_player = player1 if random.choice([True, False]) else player2

    while True:
       print(f"\n{serving_player.name} to serve")
       game_winner = play_game(player1, player2)

    if game_winner == player1:
        player1.games_won += 1
    else: 
        player2.games_won += 1

    print(f"Current game score: {player1.name} {player1.games_won} - {player2.name} {player2.games_won}")

    if player1.games_won >= 6 and player1.gameswon >= player2.games_won + 2:
        print(f"Set to {player1.name}")
        return player1
    elif player2.games_won >= 6 and player2.gameswon >= player1.games_won + 2:
        print(f"Set to {player2.name}")
        return player2

    #växla spelare
    serving_player = player2 if serving_player == player1 else player1

def play_match(player1, player2):
    player1.sets_won = 0
    player2.sets_won = 0
    while player1.sets_won <2 and player2.sets_won < 2:
        print(f"\nStarting new set: {player1.name} {player1.sets_won} - {player2.name} {player2.sets_won} ")
        set_winner = play_set(player1, player2)
        set_winner.sets_won += 1
        print(f"Set score: {player1.sets_won}-{player2.sets_won} ub sets")
        time.sleep(2)  # Paus efter varje set
    match_winner = player_a if player_a.sets_won > player_b.sets_won else player_b
    print(f"\nMatch winner: {match_winner.name}")
    print(f"Final score: {player_a.sets_won}-{player_b.sets_won} in sets")

def main():


    filename = "C:/Users/stadi/OneDrive/Skrivbord/github/prog24/tennisplayers.py/playerdata.txt"

    # read players from file
    players = read_stats_from_file(filename)

    # present players and let user choose
    display_players(players)
    player1 = select_player(players, "Select player 1 by number: ")
    player2 = select_player(players, "Select player 2 by number: ")

    play_match(player1, player2)

    # input winner
    winner_name = input(f"Who won the match? {player1.name} or {player2.name}): ").strip()
    update_match_result(player1, player2, winner_name)

    #sort players after win percentage
    players = sort_players_by_win_percentage(players)

    # show the uppdated list
    print("\nUppdated player rankings:")
    print(f"{'Position':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
    for i, player in enumerate(players):
        print(f"{i+1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    write_players_to_file(filename, players)

if __name__ == "__main__":
    main()
