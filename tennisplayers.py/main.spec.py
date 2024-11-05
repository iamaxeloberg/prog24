# spec av uppgiften

# Axel Öberg
# 20040902-4155
# nr: 141
# tennismatch

# ******************** Användargränssnitt **********************

# programmet ska presentera en lista över spelare, där varje spelare har sitt namn, antal vunna matcher, antal spelade matcher och vinstprocent
# användare ska kunna välja två spelare och spela en match
# efter matchen ska användaren mata in vem som vann
# resultaten ska därefter upppdateras och en nu uppdaterad lista med alla spelare sorterade efter vinstprocent ska visas

# ******************* Minne / Datastruktuyr **********************

# spelardata ska lagras i en lista av objekt
# varje Spelar objekt ska innehålla: namn(sträng), spelade matcher(int), vunna matcher(int) och sannolikhet att vinna sin serve (0-1)(float)
# alla spelare lagras i en textfil som läses och skrives efter varje match

# ******************** algoritm *********************************

# programmet läser in information om spelarna från filen
# spelardatan från respektive spelare presenteras i en lista
# användaren väljer två spelare från listan
# användaren anger vilken spelare som vinner matchen som spelas
# statistiken uppdateras (varje spelare får += 1 match och en spelare får en vinst)
# spelarna sorteras efter vinstprocent 
# den nya sorterade listan visas
# den nya sortarade listan sparas tillbaka till textfilen

# ************************** Programskelett ******************************


#**************************** Funktioner *********************************
# - läser spelarinformation från textfilen och skapar splelar attribut som returneras i en lista. 
# - skriver ut listan med spelare och deras respektive statitisik (eventuellt ersätts av en GUI sen?)
# - låter användaren välja en spelare genom att mata in ett nummer som motsvara deras plats i listan
# - uppdaterar resultatet för de två splearna, ökar matcher och antalet vinster
# - sorterar listan av spelare i fallande ordning efter vinstprocent

#*************** Klasser och dess metoder******************

# Spelare, attribut: namn, sannolikhet att vinna serv, vinster, matcher
# Metoder: 
# vinsprocentberäkning,
# resulatat uppdatering i statitsiken

#************ Huvudprogrammet ********************
# Huvudprogrammet hanterar:
    # Läsning och visning av spelardata.
    # Val av spelare för en match.
    # Uppdatering av resultat efter matchen.
    # Sortering av spelarna efter vinstprocent.
    # Utskrift av uppdaterad ranking.
    # sparning av spelardata tillbaka till textfilen.