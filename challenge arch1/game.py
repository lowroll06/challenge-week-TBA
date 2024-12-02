import random

def start_game(dag_limiet=False, max_days=3): # hier ook dag verhogen
    print("je belandt je in een eiland, het laatste wat je je kan herinneren is dat je in cruiseship zat en van het leven zat te genieten.")
    hp = 100
    day = 1 # De dag begint op 1
    door_choice = None
    tribe_choice = None
    while hp > 0:
        print(f"\n Het is dag nummer {day} en je hebt {hp} HP.")
        
        # Controleer of de daglimiet is bereikt, als de limiet is ingeschakeld
        if dag_limiet and day > max_days:
            print(f"\nJe hebt het spel voltooid! Je hebt {max_days} dagen overleefd.")
            break

        # begin spel
        if day == 1:
            choice = input("\nJe kijkt om je heen en hebt al een tentje. Naar wat zoek je? 1. hout of 2. eten?: ")
            if choice == "1":
                print("Je blijft warm en hebt de nacht overleeft.")
                hp += 5  # Bonus voor het verzamelen van hout
            elif choice == "2":
                hp = gather_food(hp)
            else:
                print("Typ 1 of 2 alsjeblieft.")
            
            # dag 1.5
            print("\nDe nacht valt, je hoort vreemde geluiden en voelt de kou binnensluipen.")
            if choice == "1":
                print("Gelukkig heb je een vuurtje gemaakt met het hout en blijf je warm, maar je bent hongerig en verliest conditie -5 HP.")
                hp -= 10
            else:
                print("Na je jacht besluit je om te gaan slapen, maar hoor je vreemde geluiden en heb je geen vuur en slaap je dus niet -10 HP")
                hp -= 10
            if hp <= 0:
                print("Je hebt de nacht niet overleefd door de kou.")
                break

        # dag 2 (Dit elif t/m break is een stuk code die we kunnen repeaten voor de latere dagen, dan kunnen we makkelijk de dagen nu maken. gewoon copy/paste)
        elif day == 2:  # Gebruik elif zodat de code naar dag 2 gaat
            print("Je besluit om het eiland te verkennen, ga je richting het oosten of westen.")
            choice_day2 = input("1. Oost of 2. West?: ")
            
            if choice_day2 == "1":
                water_choice = input("Je ziet een tempel en besluit om erin te gaan en vind een vreemd object, pak je het op of ga je verder de tempel verkennen 1. Oppakken of 2. Tempel Verder Verkennen: ")
                if water_choice == "1":
                    computer_choice(hp)
                    hp -= 15
                elif water_choice == "2":
                    print("je laat het object en verkent de tempel verder en ziet twee deuren, welke kies je links of rechts?")
                    door_choice = input("Kies een deur: 1. links of 2. rechts?: ")
                    if door_choice == "1":
                        print("Je hebt gekozen om de linkerdeur te nemen. Je vindt een kamer vol met materialen om een hulpsignaal te maken")
                    elif door_choice == "2":
                        print("Je hebt gekozen om de rechterdeur te nemen. Je bevindt een kamer vol met slangen en word vergiftigd -100 hp")
                        hp -= 150
                else:
                    print("Typ 1 of 2 alsjeblieft.")
                    
            elif choice_day2 == "2":
                print("Je ontmoet een volk en zien ze jij als bedreiging, probeer je te communiceren of te vechten.")
                tribe_choice = input("1. communiceren 2. vechten: ")
                if tribe_choice == "1":
                    print("Je laat zien dat je in vrede komt en verwelkomen ze jou, ze geven je kamer en overnacht. Je voelt je fris +10 HP")
                    hp += 10
                elif tribe_choice == "2":
                    print("Je probeert te vechten, maar je word doodgeslagen -100 HP")
                    hp -= 150
                else:
                    print("Typ 1 of 2 alsjeblieft.")
                    

        elif day == 3: 
            print("je besluit dat vandaag do or die is en beloof je jezelf dat vandaag je laatste dag is op het eiland en ontsnapt hoe dan ook")
            
            if door_choice == "1":
                print("je begint met het maken van een hulpsignaal en het is gelukt. \nEen paar uur later komt een helikoper je redden en ga je terug naar je normale leven")
            elif tribe_choice == "1":
                    print("je vraagt het volk om hulp en helpen ze jou om een boot te bouwen. \n Het lukt je om weg te gaan van het eiland en hawaii te bereiken en leef je daar de rest van je leven")
            else:
                print("unlocked secret ending")                
            
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
            print("Je komt een beer te gemoet en breekt je wapen tijdens het gevecht. Je bent dood. -100 HP")
            hp -= 100
        elif choice_3 == "2":
            print("Je besluit om met je handen te jagen en vangt een vis. +10 HP")
            hp += 10
        else:
            print("Typ 1 of 2 alsjeblieft.")
    else:
        print("Typ 1 of 2 alsjeblieft.")
    return hp

start_game(dag_limiet=True, max_days=3)