class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        # Initialiserar en spelare med namn, sannolikhet att vinna serve, antal vinster och matcher
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches

    def __str__(self):
        # Returnerar en strängrepresentation av spelaren för att skriva till fil
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

    def win_percentage(self):
        # Beräknar vinstprocenten; om inga matcher har spelats returneras 0
        if self.matches > 0:
            return self.wins / self.matches
        else:
            return 0

    def update_result(self, won):
        # Uppdaterar spelarens resultat efter en match
        # Ökar antalet matcher och, vid vinst, ökar antalet vinster
        self.matches += 1
        if won:
            self.wins += 1

    def read_players_from_file(self, filename):
        # Läser in spelardata från fil och skapar spelare
        players = []
        with open(filename, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):  # Varje spelare representeras av fyra rader
                name = lines[i].strip()
                serve_win_prob = float(lines[i + 1].strip())
                wins = int(lines[i + 2].strip())
                matches = int(lines[i + 3].strip())
                players.append(Player(name, serve_win_prob, wins, matches))
        return players

    def write_players_to_file(self, filename, players):
        # Skriver uppdaterad spelardata till fil
        with open(filename, "w") as file:
            for player in players:
                file.write(str(player) + "\n")

    def display_players(self, players):
        # Visar en lista över tillgängliga spelare med deras statistik
        print("\nAvailable players:")
        for i, player in enumerate(players):
            print(f"{i + 1}. {player.name} - Wins: {player.wins}, Matches: {player.matches}, Win Percentage: {player.win_percentage():.3f}")

    def select_player(self, players, prompt):
        # Låter användaren välja en spelare genom att ange ett nummer
        while True:
            self.display_players(players)
            try:
                choice = int(input(prompt)) - 1
                if 0 <= choice < len(players):
                    return players[choice]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def sort_players_by_win_percentage(self, players):
        # Sorterar spelare i fallande ordning baserat på deras vinstprocent
        return sorted(players, key=lambda p: p.win_percentage(), reverse=True)

class Match:
    def __init__(self, player1, player2):
        # Initialiserar en match med två spelare
        self.player1 = player1
        self.player2 = player2

    def update_match_result(self, winner_name):
        # Uppdaterar resultatet för matchen baserat på vinnaren
        if self.player1.name == winner_name:
            self.player1.update_result(True)
            self.player2.update_result(False)
        elif self.player2.name == winner_name:
            self.player2.update_result(True)
            self.player1.update_result(False)

def main():
    filename = "pd.txt"  # Filnamn för spelardata

    # Skapa en spelare för att använda dess metoder
    player_instance = Player("", 0, 0, 0)

    # Läs in spelare från fil
    players = player_instance.read_players_from_file(filename)

    # Låt användaren välja två spelare
    player1 = player_instance.select_player(players, "Select player 1 by number: ")
    player2 = player_instance.select_player(players, "Select player 2 by number: ")

    # Skapa en match med de två valda spelarna
    match = Match(player1, player2)

    # Fråga användaren vem som vann matchen
    while True:
        winner = input(f"Who won the match? ({player1.name} or {player2.name}): ").strip()
        if winner in [player1.name, player2.name]:
            break
        print("Invalid input. Please enter a valid name.")

    # Uppdatera matchresultatet
    match.update_match_result(winner)

    # Sortera spelarna efter vinstprocent
    players = player_instance.sort_players_by_win_percentage(players)

    # Visa den uppdaterade rankingen
    print("\nUpdated player rankings:")
    for i, player in enumerate(players):
        print(f"{i + 1}. {player.name} - Wins: {player.wins}, Matches: {player.matches}, Win Percentage: {player.win_percentage():.3f}")

    # Skriv tillbaka uppdaterad data till fil
    player_instance.write_players_to_file(filename, players)

if __name__ == "__main__":
    main()
