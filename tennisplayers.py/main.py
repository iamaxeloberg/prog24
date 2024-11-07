import os
from player import player


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

def main():


    filename = "C:/Users/stadi/OneDrive/Skrivbord/github/prog24/tennisplayers.py/playerdata.txt"

    # read players from file
    players = read_stats_from_file(filename)

    # present players and let user choose
    display_players(players)
    player1 = select_player(players, "Select player 1 by number: ")
    player2 = select_player(players, "Select player 2 by number: ")

    # input winner
    winner = input(f"Who won the match? {player1.name} or {player2.name}): ").strip()

    # uppdate playerdata
    update_match_result(player1, player2, winner)

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
