# Välkomstmeddelande till spelaren
print("\nVälkommen till spelet Chomp. \n")
print("I spelet väljer du ett blocknummer från chokladkakan.")
print("Det valda blocket och alla block till höger och nedåt tas bort.")
print("Målet är att undvika att välja den giftiga rutan (P). Den som väljer P förlorar.\n")

# Funktion som kontrollerar att användarens inmatning för rader/kolumner är giltig (2-9)
def valid_input(user_input):
    return user_input.isdigit() and 2 <= int(user_input) <= 9

# Funktion som upprepar tills korrekt input (antal rader och kolumner) ges av användaren
while True:
    rows = input("Hur många rader ska chokladkakan ha (2-9): ")
    cols = input("Hur många kolumner ska chokladkakan ha (2-9): ")
    if valid_input(rows) and valid_input(cols):  # Kontrollera om input är giltig
        rows = int(rows)  # Konvertera input till heltal
        cols = int(cols)
        break  # Avbryt loopen när giltiga värden anges
    else:
        print("Ogiltig inmatning, försök igen!")  # Meddelande om ogiltig inmatning

# Funktion som skapar chokladkakan och sätter 'P' som den giftiga rutan i det övre vänstra hörnet
def create_chocolate_bar(rows, cols):
    chocolate_bar = []
    for row in range(rows):  # Loopar igenom varje rad
        new_row = []
        for col in range(cols):  # Skapar en kolumn med blocknummer
            new_row.append(str((row + 1) * 10 + (col + 1)))  # Skapa blocknummer som sträng
        chocolate_bar.append(new_row)  # Lägg till raden i chokladkakan
    chocolate_bar[0][0] = "P"  # Sätter den första rutan till 'P', vilket är den giftiga rutan
    return chocolate_bar  # Returnerar chokladkakan

# Funktion som skriver ut chokladkakan
def print_chocolate_bar(chocolate_bar):
    for row in chocolate_bar:  # För varje rad i chokladkakan
        print(" ".join(row))  # Skriv ut radens element separerade med ett mellanrum
    print()

# Funktion som tar bort rutor från chokladkakan baserat på spelarnas val
def chomp(chocolate_bar, row_choice, col_choice):
    for i in range(row_choice, len(chocolate_bar)):  # Starta från vald rad och fortsätt nedåt
        chocolate_bar[i] = chocolate_bar[i][:col_choice]  # Ta bort alla kolumner till höger om den valda rutan
    chocolate_bar = [row for row in chocolate_bar if row]  # Ta bort tomma rader från listan
    return chocolate_bar  # Returnera den uppdaterade chokladkakan

# Funktion som kontrollerar om spelet är slut (när endast 'P' finns kvar)
def check_winner(chocolate_bar):
    if len(chocolate_bar) == 1 and len(chocolate_bar[0]) == 1:  # Om endast 'P' är kvar
        return True  # Spelet är slut
    return False  # Spelet fortsätter

# Funktion som låter användaren välja en ruta i chokladkakan
def ask_for_square(chocolate_bar):
    while True:
        user_input = input("Välj ett blocknummer: ")  # Fråga efter blocknummer
        if user_input == "P":  # Om användaren väljer 'P'
            print("Du kan inte välja den giftiga rutan (P). Försök igen.")  # Felmeddelande
            continue
        # Loopar igenom chokladkakan för att hitta den valda rutan
        for row in range(len(chocolate_bar)):
            for col in range(len(chocolate_bar[row])):
                if chocolate_bar[row][col] == user_input:  # Om rutan hittas
                    return row, col  # Returnera vald rad och kolumn
        print(f"Ruta {user_input} finns inte. Försök igen.")  # Felmeddelande om rutan inte finns

# Skapar chokladkakan och printar den
chocolate_bar = create_chocolate_bar(rows, cols)
print_chocolate_bar(chocolate_bar)

# Växlar mellan spelare 1 och 2
player_turn = 1
while True:
    print(f"\nSpelare {player_turn}s tur:")  # Meddelande om vems tur det är
    chosen_row, chosen_col = ask_for_square(chocolate_bar)  # Spelaren väljer en ruta
    chocolate_bar = chomp(chocolate_bar, chosen_row, chosen_col)  # Uppdatera chokladkakan
    print_chocolate_bar(chocolate_bar)  # Skriv ut den uppdaterade chokladkakan
    
    if check_winner(chocolate_bar):  # Kontrollera om spelet är slut
        print("Spelet är slut! Den andra spelaren vann!")  # Meddelande om att spelet är över
        break  # Avsluta spelet

    # Byt spelare (om det är spelare 1, byt till spelare 2 och tvärtom)
    player_turn = 2 if player_turn == 1 else 1
