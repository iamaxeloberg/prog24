class TV: #Klass # klassen som kapslar in information om en tv såsom dess namn, kanal och volyminställningar
    def __init__(self, tv_name, max_channel, current_channel, max_volume, current_volume): #init funktion
        self.tv_name = tv_name
        self.current_volume = current_volume
        self.current_channel = current_channel #Interna variabler
        self.max_volume = max_volume
        self.max_channel = max_channel
        
    def change_channel(self, new_channel): #Metod för att byta kanal
        if new_channel<1 or new_channel>self.max_channel: # den ändrar den aktuella kanalen till en ny kanal, om den nya kanalen är inom det illåtna intervallet 1 till maxchanallen
            return False # 
        self.current_channel = new_channel
        return True

    def increase_volume(self): #Metod för att öka volymen
        if self.current_volume == self.max_volume: 
            return False # går allt som det ska ökas volymen med ett
        self.current_volume+=1 
        return True
    
    def decrease_volume(self): #Metod för att sänka volymen
        if self.current_volume == 0: # man kan inte  sänka när skiten är noll duuuuh
            return False
        self.current_volume-=1
        return True
    
    def __str__(self): #dundermetod som används för att definiera hur ett objekt sak representeras som en sträng, när man anropar print(tvokbejt eller konveraretet)
        return self.tv_name + "\nKanal: " + str(self.current_channel) + "\nLjudvolym: " + str(self.current_volume) + "\n" # skapar en sträng av skiten istället för en ful jälva rad
    
    def str_for_file(self): #skapar en kommasaparerad asträng med all information för TV objektet, ger en struktur som är idealisk för att återskapa tv objekt vid behov.
        return str(self.tv_name) + "," + str(self.max_channel) + "," + str(self.current_channel) + "," + str(self.max_volume) + "," + str(self.current_volume)
