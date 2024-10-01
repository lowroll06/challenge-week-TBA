def start_game(day_limit_enabled=False, max_days=2):
    print("Je belandt op een eiland, het laatste wat je je kan herinneren is dat je op een cruiseship zat en van het leven aan het genieten was.")
    hp = 100
    day = 1  # De dag begint op 1
    
    while hp > 0:
        print(f"\nHet is dag {day} en je hebt {hp} HP.")
        
        # Controleer of de daglimiet is bereikt, als de limiet is ingeschakeld
        if day_limit_enabled and day > max_days:
            print(f"\nJe hebt het spel voltooid! Je hebt {max_days} dagen overleefd.")
            break

        # Dag 1 keuze
        if day == 1:
            choice = input("\nJe kijkt om je heen en hebt al een tentje. Naar wat zoek je? 1. hout of 2. eten?: ")
            if choice == "1":
                print("Je hebt hout gevonden en rust de rest van de dag.")
                hp += 5  # Bonus voor het verzamelen van hout
            elif choice == "2":
                hp = gather_food(hp)
            else:
                print("Typ 1 of 2 alsjeblieft.")
            
            # Nacht na dag 1
            print("\nDe nacht valt, je hoort vreemde geluiden en voelt de kou binnensluipen.")
            if choice == "1":
                print("Gelukkig heb je een vuurtje gemaakt met het hout en blijf je warm.")
            else:
                print("Zonder hout heb je het koud. Je slaapt slecht en verliest 5 HP door de kou.")
                hp -= 5
            
            if hp <= 0:
                print("Je hebt de nacht niet overleefd door de kou.")
                break

        # Dag 2 keuze
        elif day == 2:  # Gebruik elif zodat de code naar dag 2 gaat
            print("\nHet is tijd om actie te ondernemen. Je hebt de nacht overleefd, maar je moet meer doen om te blijven leven.")
            choice_day2 = input("Wat ga je doen? 1. Water zoeken of 2. Een betere schuilplaats bouwen?: ")
            
            if choice_day2 == "1":
                print("Je gaat op zoek naar water.")
                water_choice = input("Je vindt een rivier. Drink je het water direct? 1. Ja of 2. Nee, eerst koken: ")
                if water_choice == "1":
                    print("Je drinkt het water direct en krijgt een maaginfectie. -15 HP")
                    hp -= 15
                elif water_choice == "2":
                    print("Je kookt het water en drinkt het veilig op. +10 HP")
                    hp += 10
                else:
                    print("Typ 1 of 2 alsjeblieft.")
                    
            elif choice_day2 == "2":
                print("Je besluit een stevigere schuilplaats te bouwen.")
                shelter_choice = input("Je hebt een idee. Bouw je 1. een hut van hout of 2. een hut van bladeren en takken?: ")
                if shelter_choice == "1":
                    print("Je bouwt een stevige hut van hout en voelt je veilig. +10 HP")
                    hp += 10
                elif shelter_choice == "2":
                    print("Je bouwt een hut van bladeren en takken, maar deze biedt weinig bescherming tegen de elementen. -5 HP")
                    hp -= 5
                else:
                    print("Typ 1 of 2 alsjeblieft.")
            
            if hp <= 0:
                print("Je hebt het niet overleefd.")
                break

        # Verhoog de dag
        day += 1

    # Vraag na het verliezen of de speler opnieuw wil beginnen
    if hp <= 0:
        print("Je HP is op. Je hebt het niet overleefd.")
        ask = input("Wil je opnieuw proberen? (ja/nee): ")
        if ask.lower() == "ja":
            start_game(day_limit_enabled, max_days)
        else:
            print("Bedankt voor het spelen!")
            
def gather_food(hp):
    choice_2 = input("\nJe gaat op zoek naar eten. Wat ga je doen? 1. Bessen verzamelen of 2. Jagen?: ")
    if choice_2 == "1":
        print("Je vindt bessen, maar ze zijn giftig. -10 HP")
        hp -= 10
    elif choice_2 == "2":
        choice_3 = input("Maak je 1. een wapen of 2. jaag je met je handen?: ")
        if choice_3 == "1":
            print("Je maakt een wapen en zoekt naar prooi.\nJe komt een beer tegen en breekt je wapen tijdens het gevecht. Je gaat dood. -100 HP")
            hp -= 100
        elif choice_3 == "2":
            print("Je besluit om met je handen te jagen en vangt een vis. +10 HP")
            hp += 10
        else:
            print("Typ 1 of 2 alsjeblieft.")
    else:
        print("Typ 1 of 2 alsjeblieft.")
    
    return hp

# Voorbeeld: Speel met een daglimiet van 3 dagen
start_game(day_limit_enabled=True, max_days=2)

# Als je de daglimiet uit wilt schakelen, gebruik je:
# start_game(day_limit_enabled=False)
