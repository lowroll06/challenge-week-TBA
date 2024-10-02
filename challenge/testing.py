import random

def start_game(dag_limiet=False, max_days=3):
    print("Je belandt op een eiland, het laatste wat je je kan herinneren is dat je in een cruiseschip zat en van het leven genoot.")
    hp = 100
    day = 1  # De dag begint op 1
    while hp > 0:
        print(f"\nHet is dag nummer {day} en je hebt {hp} HP.")

        # Controleer of de daglimiet is bereikt
        if dag_limiet and day > max_days:
            print(f"\nJe hebt het spel voltooid! Je hebt {max_days} dagen overleefd.")
            break

        # begin spel
        if day == 1:
            choice = input("\nJe kijkt om je heen en hebt al een tentje. Naar wat zoek je? 1. Hout of 2. Eten?: ")
            if choice == "1":
                print("Je blijft warm en hebt de nacht overleefd.")
                hp += 5  # Bonus voor het verzamelen van hout
            elif choice == "2":
                hp = gather_food(hp)
            else:
                print("Typ 1 of 2 alsjeblieft.")
            
            # nacht
            print("\nDe nacht valt, je hoort vreemde geluiden en voelt de kou binnensluipen.")
            if choice == "1":
                print("Gelukkig heb je een vuurtje gemaakt en blijf je warm, maar je bent hongerig en verliest conditie -5 HP.")
                hp -= 5
            else:
                print("Je hebt geen vuur en voelt de kou. -10 HP.")
                hp -= 10

            if hp <= 0:
                print("Je hebt de nacht niet overleefd door de kou.")
                break

        # dag 2
        elif day == 2:
            print("Je besluit om het eiland te verkennen. Ga je richting het oosten of westen?")
            choice_day2 = input("1. Oost of 2. West?: ")
            
            if choice_day2 == "1":
                water_choice = input("Je ziet een tempel en vindt een vreemd object. 1. Oppakken of 2. Verder verkennen?: ")
                if water_choice == "1":
                    hp = computer_choice(hp)  # Random uitkomst
                elif water_choice == "2":
                    print("Je verkent de tempel verder en vindt twee deuren.")
                    door_choice = input("Kies een deur: 1. Links of 2. Rechts?: ")
                    if door_choice == "1":
                        print("Je vindt een kamer vol materialen om een hulpsignaal te maken.")
                    elif door_choice == "2":
                        print("Je vindt een kamer vol met slangen en wordt vergiftigd! -100 HP")
                        hp -= 100
                else:
                    print("Typ 1 of 2 alsjeblieft.")
                    
            elif choice_day2 == "2":
                tribe_choice = input("Je ontmoet een volk. 1. Communiceren of 2. Vechten?: ")
                if tribe_choice == "1":
                    print("Ze verwelkomen je en geven je voedsel en onderdak. +10 HP")
                    hp += 10
                elif tribe_choice == "2":
                    print("Je probeert te vechten, maar je wordt gedood. -100 HP")
                    hp -= 100
                else:
                    print("Typ 1 of 2 alsjeblieft.")
        
        # dag verhoger
        day += 1

    # Als je hp op is
    if hp <= 0:
        print("Je HP is op. Je hebt het niet overleefd.")
        ask = input("Wil je opnieuw proberen? (ja/nee): ")
        if ask.lower() == "ja":
            start_game(dag_limiet, max_days)
        else:
            print("Bedankt voor het spelen!")


# Functie voor de random keuze
def computer_choice(hp):
    outcomes = [
        {"message": "Het object glimt en wijst je naar een geheime koninkrijk. Je wordt koning!", "hp_change": 0},
        {"message": "Het object tikt en je beseft dat het een bom is. -100 HP", "hp_change": -100}
    ]
    
    outcome = random.choice(outcomes)
    print(outcome["message"])
    hp += outcome["hp_change"]
    
    return hp

# dag 1
def gather_food(hp):
    choice_2 = input("\nJe gaat op zoek naar eten. Wat ga je doen? 1. Bessen verzamelen of 2. Jagen?: ")
    if choice_2 == "1":
        print("Je vindt bessen, maar ze zijn giftig. -10 HP")
        hp -= 10
    elif choice_2 == "2":
        choice_3 = input("Maak je 1. een wapen of 2. jaag je met je handen?: ")
        if choice_3 == "1":
            print("Je komt een beer tegen en breekt je wapen. -100 HP")
            hp -= 100
        elif choice_3 == "2":
            print("Je vangt een vis. +10 HP")
            hp += 10
        else:
            print("Typ 1 of 2 alsjeblieft.")
    else:
        print("Typ 1 of 2 alsjeblieft.")
    return hp

# Start het spel
start_game(dag_limiet=True, max_days=3)
