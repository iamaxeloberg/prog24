# Definition av TV-klassen, som representerar en TV med namn, kanal- och volyminställningar
class TV:  
    # Konstruktor (initieringsfunktion) för att skapa ett nytt TV-objekt
    def __init__(self, tv_name, max_channel, current_channel, max_volume, current_volume):
        # Variabler för att lagra TV:ns namn, nuvarande kanal, maxkanal, nuvarande volym och maxvolym
        self.tv_name = tv_name
        self.current_volume = current_volume
        self.current_channel = current_channel
        self.max_volume = max_volume
        self.max_channel = max_channel

    # Metod för att byta till en ny kanal, om den är inom giltigt kanalområde
    def change_channel(self, new_channel):
        # Kontrollera om den nya kanalen är inom gränserna (mellan 1 och maxkanal)
        if new_channel < 1 or new_channel > self.max_channel:
            return False  # Om kanalen inte är giltig, returnera False
        self.current_channel = new_channel  # Uppdatera till den nya kanalen
        return True  # Returnera True om kanalbytet lyckades

    # Metod för att öka volymen, men inte över den maximala volymen
    def increase_volume(self):
        if self.current_volume == self.max_volume:  # Kontrollera om volymen redan är på max
            return False  # Om volymen är på max, returnera False
        self.current_volume += 1  # Öka volymen med 1
        return True  # Returnera True om volymen ökades framgångsrikt

    # Metod för att sänka volymen, men inte under noll
    def decrease_volume(self):
        if self.current_volume == 0:  # Kontrollera om volymen redan är på lägsta nivå
            return False  # Om volymen är på noll, returnera False
        self.current_volume -= 1  # Sänk volymen med 1
        return True  # Returnera True om volymen sänktes framgångsrikt

    # Metod för att skapa en strängrepresentation av TV-objektet (används när objektet printas)
    def __str__(self):
        # Returnera en sträng som visar TV:ns namn, nuvarande kanal och nuvarande volym
        return self.tv_name + "\nKanal: " + str(self.current_channel) + "\nLjudvolym: " + str(self.current_volume) + "\n"
    
    # Metod för att skapa en strängrepresentation av TV-objektet för lagring i en fil
    def str_for_file(self):
        # Returnera en kommaseparerad sträng med alla attribut (namn, maxkanal, nuvarande kanal, maxvolym, nuvarande volym)
        return str(self.tv_name) + "," + str(self.max_channel) + "," + str(self.current_channel) + "," + str(self.max_volume) + "," + str(self.current_volume)
