tv_kladd 

#Importera TV från TV.py
from TV import TV #läser in data från filen allatv.txt varje rad i filen representerar ett tv objekt i csv format (comma separeted values)

def read_file(file_name): #Funktion som läser från textfilen
    TV_list = [] #skapar en tom lista för att lagra värden i sen 
    with open(file_name, "r") as file: #Öppnar filen för läsoperationer
        for row in file: # iterarar över varje rad i filen, raden rensas från m,ellanslag och delas upp vid kommatecken med strip().split()
            item = row.strip().split(",") #Delar sträng ""
            TV_list.append(TV(item[0], int(item[1]), int(item[2]), int(item[3]), int(item[4]))) # de extraherade värdena används för att skapa ett tv obejkt med rätt ratat
    return TV_list

def write_file(item_list, file_name): # skriver en lista av tv objekt till en fil i CVS format
    with open(file_name, "w") as file:
        for item in item_list: 
            file.write(item.str_for_file() + "\n")  # Se till att varje TV får en egen rad i textfilen.

def change_channel(tv): # funktionen låter användaren byta kanal på en tv men endast om kanalen är inom tillåtna gränser
    while True: # oändlig while loop används för att säkerställa att användaren ger en giltig input
        try: 
            channel = int(input("Inmata kanal att byta till: ")) #Försök hämta input och konvertera till heltal
            
            if 1 <= channel <= tv.max_channel: #Kolla om kanalen är inom begränsningarna
                tv.change_channel(channel)
                break  #Lämna loopen om vi lyckats byta kanal

            raise ValueError(f"Inmata värde mellan 1 och {tv.max_channel}.")  #Raisa error om något gick snett.
        
        except ValueError:
            print(f"Ogiltig input. Ange ett nummer mellan 1 och {tv.max_channel}.")  #Hantera except genom att printa Ogiltigt input...

#Måste returnera annars helt useless, går emot uppgiftsbeskrivning  
def increase_volume(tv):
    return tv.increase_volume()

def decrease_volume(tv):
    return tv.decrease_volume()

def adjust_TV_menu():
    choice = input("1. Byt kanal \n2. Sänk ljudnivå \n3. Höj ljudnivå\n4. Gå till huvudmenyn\nVälj: ")
    return choice

                
def select_TV_menu(tv_list):

    while True:
        i = 0 #räknare för att iterara över listan av tv bjekt  
        valid_inputs = [] # en lista där alla giltiga inmatningar (srtängar etc) lagras ,

        print()

        while i < len(tv_list) #för varje TV skrivs ett alternativ ut på formen TV_namn
            valid_inputs.append(str(i+1)) # numreringen ska börja från 1 för att det är så ovan
            print(str(i+1) + ".", tv_list[i].tv_name) #Vi vill att listan i terminalen ska börja från 1 och måste därför offseta med ett värde av ett då ett list objekt börjar med index 0.
            i+=1
            
        valid_inputs.append(str(i+1)) #Det sista alternativet ska vara avsluta. därför läggs till separat
        print(str(i+1)+". Avsluta") #Adderar vi fler TV objekt kommer avsluta fortfarande vara sist. (Dynamiskt)
        choice = input("Välj: ") #användaren ombeds ge ett val 
        if choice in valid_inputs: # kolla så att användarens val är valid or nah
            choice = int(choice) 
            if choice == i+1:
                return None
            return tv_list[choice-1] # Om användaren väljer i+1 (det sista alternativet som motsvarar "Avsluta"), returneras None. Detta signalerar att användaren vill avsluta programmet.
        else:
            print("\nEj giltig indata. Testa igen.\n")

def tv_prompt(selected_tv):
    valid_operations = ["1","2","3","4"] 
    while True: #While true loop som kommer visa TV och dess attribut samt be användaren om indata
        
        print()
        print(selected_tv) #Printa TV objektet som valts

        choice = adjust_TV_menu()

        if choice not in valid_operations: #Om strängen vid input finns i valid choice listan så fortsätt
            print("\nFelaktig inmatning. Försök igen.")

        else:
            if choice == "1": #Om den är lika med 1 så ändra kanal
                change_channel(selected_tv)

            if choice == "2":
                if not decrease_volume(selected_tv):
                    print("\nVolymnivån är på lägsta redan.")

            if choice == "3":
                if not increase_volume(selected_tv):
                    print("\nVolymnivån är på högsta redan.")
 
            if choice == "4": #Lämna whileloopen om användaren matade in 4 i som input.
                break

# Läs data från allatv.txt filen med hjälp av denna funktion
tv_obj_list = read_file("allatv.txt")

#Program logik börjar här
print("***Välkommen till TV-simulatorn****")

while True: #Avslutas genom att användaren inmatar värdet för att avsluta. Gameloop
    selected_tv = select_TV_menu(tv_obj_list)
    if not selected_tv:
        break
    tv_prompt(selected_tv)

# Skriv in den modifierade listan i allatv.txt filen igen.
write_file(tv_obj_list, "allatv.txt")
