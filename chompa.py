#test igen
# Funktion för att skapa chokladmatrisen
def create_chocolate_bar(rows, cols):
    if rows <= 0 or cols <= 0:
        return None # kontrollerar att row och col är större än noll
    chocolate_bar = [] #skapar en tom lista
    for i in range(1, rows + 1): #skapar en ytterloop (för rader) itererar från 1 till rows
        row = []
        for j in range(1, cols + 1): #skapar en inre loop från 1 till och med cols
            if i == 1 and j == 1: # (1,1) kommer alltid att vara giftig
                row.append("P")  # Förgiftat block
            else:
                row.append(f"{i}{j}") 
        chocolate_bar.append(row) # alla andra numrerar med deras row- och colnummer, kombinerade till en sträng.
    return chocolate_bar # När alla rader har lagts till i matrisen returnerar funktionen chokladmatrisen

# Funktion för att skriva ut chokladbaren från lista av strängar till snygg och städat formattering
def print_chocolate_bar(matrix):
    if matrix is None: #om matrisen är none avslutas skiten direkt
        return
    for row in matrix: #matrix är en lista av listor, loopen interar genom varje rad en i taget
        print("\t".join(row)) # #skapar en sträng där varje element är separerat med en tab

# Funktion för att "äta" en del av chokladbaren
def chomp(matrix, row, col):
    if row < 0 or col < 0 or row >= len(matrix) or col >= len(matrix[0]): # koll av row och col index kollar så ej negativt index och att raden inte är utanför col/rows längd
        return None # banga isf
    for i in range(row, len(matrix)): #loopen börjar vid den valda raden och slutar vid den sista i matrisen
        matrix[i] = matrix[i][:col]  # Ta bort block från kolumnindexet och framåt
    matrix = [r for r in matrix if r]  # ta bort tomma rader, 
    return matrix # returnerna ofc

# Funktion för att kontrollera om någon har vunnit (dvs om "P" är kvar i kakan)
def check_winner(matrix):
    return len(matrix) == 1 and len(matrix[0]) == 1 and matrix[0][0] == "P" # kolla så en rad kvar, kolla så en col kvar, och kolla så att de tär p

# Funktion för att fråga efter spelarens val och hantera lite felinmatning
def ask_cell_number(matrix):
    while True: #bryts bara vid giltig input
        try:
            cell_number = input("Välj ett blocknummer: ")
            for row in range(len(matrix)): #itererar över varje rad i matrisen
                if cell_number in matrix[row]: #kontrollera om det angivna blocknumret finns i den aktuella raden
                    col = matrix[row].index(cell_number) #om hittas 
                    return row, col #returnera col index
            print(f"{cell_number} är ogilltigt blocknummer, försök igen.") #om ej gör om 
        except ValueError:
            print("Felaktig inmatning, försök igen.") # generellt felinmating --> gör om gör rätt!

# Huvudprogrammet för Chomp-spelet
def chomp_game(): # ge spelaren en instruktion
    print("Välkommen till spelet Chomp.\n")
    print("Instruktioner: I spelet kommer du utmanas om att välja ett blocknummer från spelplanen.")
    print("Det valda blocket och alla block under och till höger kommer att raderas.")
    print("Spelet går ut på att undvika välja P, den spelare som väljer P förlorar och den andra spelaren vinner.\n")
    
    # Fråga efter antal rader och kolumner för att kunna skapa matrisen
    rows = int(input("Hur många rader ska chokladbaren bestå av: ")) #chockladbaren är en helt sjukt anglicism men aja
    cols = int(input("Hur många kolumner ska chokladbaren bestå av: "))
    
    # Skapa chokladbaren 
    chocolate_bar = create_chocolate_bar(rows, cols) #funktionen används för att generera en chokladmatris med givet row o col
    
    # Spelomgång
    player_turn = 1
    while not check_winner(chocolate_bar): #spelet körs i en while loop tills någon vinner
        print_chocolate_bar(chocolate_bar) 
        print(f"Spelare {player_turn}s tur")
        
        # Be spelaren välja en ruta
        row, col = ask_cell_number(chocolate_bar)
        
        # Modifiera matrisen enligt spelarens val
        chocolate_bar = chomp(chocolate_bar, row, col)
        
        # Byt spelare
        player_turn = 2 if player_turn == 1 else 1
    
    # Presentera vinnaren
    print(f"Spelet är slut, vinnare är spelare {2 if player_turn == 1 else 1}!")

# Starta spelet
chomp_game()