# Importera TV-klassen från TV.py (där TV är en egen klass som representerar en TV med specifika attribut och metoder)
from TV import TV

# Funktion som läser in data från en textfil och skapar en lista med TV-objekt
def read_file(file_name):  
    TV_list = []  # Tom lista för att lagra TV-objekt
    with open(file_name, "r") as file:  # Öppnar textfilen i läsläge ("r")
        for row in file:  # Loopar igenom varje rad i filen
            item = row.strip().split(",")  # Raden delas upp vid varje komma (","), vilket skapar en lista av attribut
            # Skapar ett nytt TV-objekt med de värden som finns i raden, och konverterar nödvändiga strängar till heltal
            TV_list.append(TV(item[0], int(item[1]), int(item[2]), int(item[3]), int(item[4])))
    return TV_list  # Returnerar listan med alla TV-objekt

# Funktion som skriver data (uppdaterade TV-objekt) till en textfil
def write_file(item_list, file_name):  
    with open(file_name, "w") as file:  # Öppnar textfilen i skrivläge ("w") så att innehållet kan ersättas
        for item in item_list:  # Loopar igenom varje TV-objekt i listan
            # Skriver varje TV-objekt till filen som en sträng (som skapats med en metod i TV-klassen)
            file.write(item.str_for_file() + "\n")  # \n lägger till en ny rad efter varje TV-objekt

# Funktion som låter användaren byta kanal på en specifik TV
def change_channel(tv):
    while True:  # Oändlig loop tills korrekt kanal har valts
        try:
            # Ber användaren mata in kanalnummer och försöker konvertera detta till ett heltal
            channel = int(input("Inmata kanal att byta till: "))
            
            # Kontrollera om den valda kanalen är inom den tillåtna gränsen (mellan 1 och maxkanal för den TV:n)
            if 1 <= channel <= tv.max_channel:
                tv.change_channel(channel)  # Anropar en metod i TV-klassen för att byta kanal
                break  # Avslutar loopen när kanalen har bytts framgångsrikt

            # Om kanalnumret är utanför gränserna kastas ett felmeddelande
            raise ValueError(f"Inmata värde mellan 1 och {tv.max_channel}.")  
        
        except ValueError:  # Hanterar ogiltiga inmatningar, t.ex. icke-heltal eller nummer utanför gränserna
            print(f"Ogiltig input. Ange ett nummer mellan 1 och {tv.max_channel}.")

# Funktion som ökar volymen på en TV genom att anropa en metod i TV-klassen
def increase_volume(tv):
    return tv.increase_volume()  # Returnerar om volymen lyckades höjas (hanteras i TV-klassen)

# Funktion som minskar volymen på en TV genom att anropa en metod i TV-klassen
def decrease_volume(tv):
    return tv.decrease_volume()  # Returnerar om volymen lyckades sänkas (hanteras i TV-klassen)

# Funktion som visar en meny för användaren för att välja vad de vill göra med TV:n (byt kanal, höj/sänk volym, eller återgå till huvudmenyn)
def adjust_TV_menu():
    # Visa en meny med valmöjligheter och returnera användarens val
    choice = input("1. Byt kanal \n2. Sänk ljudnivå \n3. Höj ljudnivå\n4. Gå till huvudmenyn\nVälj: ")
    return choice  # Returnerar det valda alternativet

# Funktion för att låta användaren välja vilken TV i listan de vill interagera med
def select_TV_menu(tv_list):
    while True:  # Oändlig loop som låter användaren välja tills ett giltigt val görs
        i = 0  # Indexvariabel för att numrera TV-apparater i listan
        valid_inputs = []  # Lista över giltiga inmatningar

        print()  # Tom rad för bättre läsbarhet

        # Loop som visar alla tillgängliga TV-apparater med ett nummer
        while i < len(tv_list):
            valid_inputs.append(str(i + 1))  # Lägger till giltig inmatning (startar från 1)
            # Visar TV:ns namn och associerar det med ett nummer (från 1 uppåt)
            print(str(i + 1) + ".", tv_list[i].tv_name)
            i += 1  # Ökar indexet

        # Lägg till alternativet för att avsluta (detta visas sist)
        valid_inputs.append(str(i + 1))  # Lägg till avslutningsalternativ som ett giltigt val
        print(str(i + 1) + ". Avsluta")  # Visar avslutningsalternativet

        # Ber användaren göra ett val
        choice = input("Välj: ")
        if choice in valid_inputs:  # Kontrollera om inmatningen är ett giltigt val
            choice = int(choice)  # Konvertera val till ett heltal
            if choice == i + 1:  # Om användaren valde "Avsluta"
                return None  # Returnera None för att avsluta
            return tv_list[choice - 1]  # Returnera den valda TV:n (justera indexet med -1)
        else:
            print("\nEj giltig indata. Testa igen.\n")  # Felmeddelande om ogiltig inmatning
    
# Funktion som hanterar användarens interaktion med en specifik TV (baserat på menyval)
def tv_prompt(selected_tv):
    valid_operations = ["1", "2", "3", "4"]  # Giltiga menyval
    while True:  # Oändlig loop tills användaren väljer att återgå till huvudmenyn
        
        print()  # Tom rad för bättre läsbarhet
        print(selected_tv)  # Visar den valda TV:ns attribut (t.ex. namn, kanal, volym)

        choice = adjust_TV_menu()  # Visar TV-menyn och får användarens val

        if choice not in valid_operations:  # Kontrollera om valet är giltigt
            print("\nFelaktig inmatning. Försök igen.")  # Felmeddelande om inmatningen är ogiltig

        else:  # Om valet är giltigt, utför motsvarande åtgärd
            if choice == "1":  # Byt kanal
                change_channel(selected_tv)

            if choice == "2":  # Sänk volymen
                if not decrease_volume(selected_tv):  # Om volymen redan är på lägsta nivå
                    print("\nVolymnivån är på lägsta redan.")

            if choice == "3":  # Höj volymen
                if not increase_volume(selected_tv):  # Om volymen redan är på högsta nivå
                    print("\nVolymnivån är på högsta redan.")
 
            if choice == "4":  # Återgå till huvudmenyn
                break  # Avslutar loopen för att gå tillbaka till TV-menyn

# Huvudprogrammet börjar här

# Läs in data från textfilen (laddar alla TV-apparater från filen och skapar objekt)
tv_obj_list = read_file("TV_data.txt")

# Välkomstmeddelande för användaren
print("***Välkommen till TV-simulatorn****")

# Huvudloopen för programmet, som låter användaren välja TV och göra ändringar tills de väljer att avsluta
while True:
    selected_tv = select_TV_menu(tv_obj_list)  # Låt användaren välja en TV att interagera med
    if not selected_tv:  # Om användaren valde "Avsluta"
        break  # Avsluta programmet
    tv_prompt(selected_tv)  # Hantera användarens val för den valda TV:n

# Skriv tillbaka den modifierade TV-listan till filen när programmet avslutas
write_file(tv_obj_list, "TV_data.txt")
