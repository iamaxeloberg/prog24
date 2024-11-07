
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
    
def read_stats_from_file(playerdata.txt):
    with open(playerdata.txt, "r") as f:
        players = []
        player = playerdata.readline().strip().slit("\n")
        for i in range(0, len(players), 4):
            