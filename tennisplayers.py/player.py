class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches

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