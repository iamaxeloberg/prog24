import os

class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches
        self.games_won = 0

    def win_percentage(self):
        if self.matches > 0:
            return self.wins / self.matches
        else:
            return 0  # Returnera 0 istället för "N/A"
        
    def update_result(self, won):
        self.matches += 1
        if won:
            self.wins += 1
    
    def __str__(self):
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

    @staticmethod
    def read_players_from_file(filename):
        players = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                lines = f.read().strip().split("\n")
                for i in range(0, len(lines), 4):
                    name = lines[i].strip()
                    serve_win_prob = float(lines[i+1].strip())
                    wins = int(lines[i+2].strip())
                    matches = int(lines[i+3].strip())
                    players.append(Player(name, serve_win_prob, wins, matches))
        return players

    @staticmethod
    def write_players_to_file(filename, players):
        with open(filename, "w") as f:
            for player in players:
                f.write(str(player) + "\n")

    @staticmethod
    def display_players(players):
        print("Available players:")
        for i, player in enumerate(players):
            print(f"{i+1}. {player.name} - Wins: {player.wins}, Matches: {player.matches}, Win Percentage: {player.win_percentage():.3f}")

    @staticmethod
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

    @staticmethod
    def update_match_result(player1, player2, winner_name):
        if player1.name == winner_name:
            player1.update_result(True)
            player2.update_result(False)
        elif player2.name == winner_name:
            player2.update_result(True)
            player1.update_result(False)

    @staticmethod
    def sort_players_by_win_percentage(players):
        return sorted(players, key=lambda p: p.win_percentage(), reverse=True)

def main():
    filename = "playerdata.txt"

    # Läs in spelare från fil
    players = Player.read_players_from_file(filename)

    # Presentera spelare och låt användaren välja två
    Player.display_players(players)
    player1 = Player.select_player(players, "Select player 1 by number: ")
    player2 = Player.select_player(players, "Select player 2 by number: ")

    # Mata in vem som vann
    winner = input(f"Who won the match? ({player1.name} or {player2.name}): ").strip()

    # Uppdatera spelardata
    Player.update_match_result(player1, player2, winner)

    # Sortera spelare efter vinstprocent
    players = Player.sort_players_by_win_percentage(players)

    # Visa den uppdaterade listan
    print("\nUpdated player rankings:")
    print(f"{'Position':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
    for i, player in enumerate(players):
        print(f"{i+1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    # Spara uppdaterade spelardata tillbaka till filen
    Player.write_players_to_file(filename, players)

if __name__ == "__main__":
    main()
