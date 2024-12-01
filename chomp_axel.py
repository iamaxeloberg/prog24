    # Laboration 4
    # Axel Öberg 20040902-4155
    # DD1310 

print("\nVälkommen till spelet Chomp. \n")
print("I spelet kommer du utmanas om att välja ett blocknummer från spelplanen.")
print("Det valda blocket och alla block under och till högre kommer att raderas.")
print("Spelet går ut på att undvika välja P, den spelare som väljer P förlorar och den andra spelare vinner \n")

# Lista med giltiga inmatningsnummer sedan validering => korrekt inmating
valid_numbers = ["2", "3", "4", "5", "6", "7", "8", "9"]

#kontrollerar att användarens inmatning är en siffra mellan 2 och 9. Detta används när användaren matar in antal rader och kolumner för spelplanen.
def matrix_input_valid(input):
    return input.isdigit() and 2 <= int(input) <= 9

# Upprepar sig tills användaren matar in korrekt värde.
while True:
    row = input("Hur många rader ska chokladbaren bestå av (siffra mellan 2-9): ")
    col = input("Hur många kolumner ska chokladbaren bestå av (siffra mellan 2-9): ")
    if matrix_input_valid(row) and matrix_input_valid(col):
        row = int(row)
        col = int(col)
        break
    else:
        print("Ogiltig inmatning, försök igen!")

#funktion som skapar en matris av chockladkakan, gör även om [0][0] till giftrutan
def create_chocolate_bar(row, col):
    matrix = [[str((y+1)*10 + (x+1)) for x in range(col)] for y in range(row)]
    matrix[0][0] = "P "  # Markera första rutan som giftig (P)
    return matrix


def print_chocolate_bar(matrix):
    for i in range(len(matrix)):
        print()
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
    print()  # Ny rad efter matrisutskrift
    return None

def chomp(matrix, delcol, delrow): #
    if delcol < 0 or delrow < 0: #ogiltigt drag vid negativt.
        return None
    for k in range(delrow, len(matrix)):
        matrix[k] = matrix[k][:delcol]
    matrix = [row for row in matrix if row] #tar bort alla tomma rader från matrisen i.e. om en rad inte innehåller några elememt
    if not matrix: #kontrollerar att matrisen inte är tom 
        return []
    return matrix

def check_winner(matrix):
    if len(matrix) == 1 and len(matrix[0]) == 1:
        return True
    return False

def ask_cell_number(matrix):
    while True:
        try:
            user_input = input("Välj ett blocknummer: ")
            if user_input == "P":
                raise ValueError("Du kan inte välja giftiga rutan (P). Försök igen.")
            for row in range(len(matrix)):
                for col in range(len(matrix[row])):
                    if user_input == matrix[row][col]:
                        return (row, col)
            raise ValueError("Ruta " + user_input + " finns ej på spelplanen, försök igen!")
        except ValueError as e:
            print(e)

# Skapa chokladmatrisen
matrix = create_chocolate_bar(row, col)
print_chocolate_bar(matrix)

# Växla mellan spelare 1 och spelare 2
player_turn = 1
while True:
    print(f"\nSpelare {player_turn}s tur:")
    row, col = ask_cell_number(matrix)
    matrix = chomp(matrix, col, row)
    print_chocolate_bar(matrix)
    
    if check_winner(matrix):
        print("Spelet är slut, Vinnaren är andra spelaren! ")
        break
    
    player_turn = 2 if player_turn == 1 else 1
