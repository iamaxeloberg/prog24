class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        # Skapa en spelare med namn, servevinstprocent, antal vinster och matcher
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches

    def win_percentage(self):
        # Räkna ut spelarens vinstprocent
        if self.matches > 0:
            return self.wins / self.matches
        else:
            return 0  # Returnera 0 om inga matcher spelats

    def update_result(self, won):
        # Uppdatera spelarens matcher och vinster baserat på om hen vann
        self.matches += 1
        if won:
            self.wins += 1

    def to_string(self):
        # Skapa en textrepresentation av spelaren för att spara i en fil
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

    def from_file(filename):
        # Läs in spelardata från en fil
        players = []
        with open(filename, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):  # Varje spelare är 4 rader
                name = lines[i].strip()
                serve_win_prob = float(lines[i + 1].strip())
                wins = int(lines[i + 2].strip())
                matches = int(lines[i + 3].strip())
                players.append(Player(name, serve_win_prob, wins, matches))
        return players

    def to_file(filename, players):
        # Skriv spelardata till en fil
        with open(filename, "w") as file:
            for player in players:
                file.write(player.to_string() + "\n")

    def display_players(players):
        # Visa alla spelare med deras statistik
        print("\nAvailable players:")
        for index in range(len(players)):
            player = players[index]
            print(f"{index + 1}. {player.name} - Wins: {player.wins}, Matches: {player.matches}, "
                  f"Win Percentage: {player.win_percentage():.3f}")

    def select_player(players, prompt):
        # Låt användaren välja en spelare med ett nummer
        while True:
            Player.display_players(players)  # Visa listan med spelare
            try:
                choice = int(input(prompt)) - 1  # Fråga om spelarens nummer
                if 0 <= choice < len(players):  # Kontrollera att numret är giltigt
                    return players[choice]
                else:
                    print("Invalid selection. Please choose a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def sort_by_win_percentage(players):
        # Sortera spelare efter vinstprocent
        return sorted(players, key=lambda player: player.win_percentage(), reverse=True)


class Match:
    def __init__(self, player1, player2):
        # Skapa en match med två spelare
        self.player1 = player1
        self.player2 = player2

    def update_result(self, winner_name):
        # Uppdatera spelarnas statistik baserat på vem som vann
        if self.player1.name == winner_name:
            self.player1.update_result(True)
            self.player2.update_result(False)
        elif self.player2.name == winner_name:
            self.player2.update_result(True)
            self.player1.update_result(False)


def main():
    # Filnamn där spelardata sparas
    filename = "pd.txt"

    # Läs in spelare från fil
    players = Player.from_file(filename)

    # Låt användaren välja två spelare
    player1 = Player.select_player(players, "Select player 1 by number: ")
    player2 = Player.select_player(players, "Select player 2 by number: ")

    # Skapa en match mellan de två spelarna
    match = Match(player1, player2)

    # Fråga vem som vann
    while True:
        winner = input(f"Who won the match? ({player1.name} or {player2.name}): ").strip()
        if winner in [player1.name, player2.name]:
            break
        print("Invalid input. Please enter the name of the winner.")

    # Uppdatera matchresultatet
    match.update_result(winner)

    # Sortera spelarna efter vinstprocent
    players = Player.sort_by_win_percentage(players)

    # Visa den uppdaterade rankingen
    print("\nUpdated player rankings:")
    for i in range(len(players)):
        player = players[i]
        print(f"{i + 1}. {player.name} - Wins: {player.wins}, Matches: {player.matches}, "
              f"Win Percentage: {player.win_percentage():.3f}")

    # Skriv uppdaterad data tillbaka till filen
    Player.to_file(filename, players)


if __name__ == "__main__":
    main()
