import random 

def start_game():
    print("je belandt op een eiland, het laatste wat je je kan herinneren is dat je in een cruiseship zat en van het leven zat te genieten")
    hp = 100
    day = 1
    while hp > 0:
        print(f"\n het is dag nummer {day} en je hebt {hp} HP")
        choice = input("\n je kijkt om je heen en hebt al een tentje. naar wat zoek je 1.hout of 2.eten?: ")
        if choice == "1":
            print("je hebt hout gevonden en rust de rest van de dag")
        elif choice == "2":
            hp = gather_food(hp)
        else:
            print("Typ 1 of 2 alsjeblieft")

        if hp <= 0:
            print("hp is op")
            ask = input("opnieuw proberen? ")
            if ask.lower() == "ja":
                start_game()
            else:
                print("bedankt voor het spelen")
                break
            
    day+= 1
                





def gather_food(hp):
    choice_2 = input("\n je gaat op zoek naar eten, wat ga je doen 1.bessen of 2.jagen: ")
    if choice_2 == "1":
       print(f"je vindt bessen, maar ze zijn giftig -10 hp")
       hp -= 10
    elif choice_2 == "2":
       choice_3 = input("maak je 1. een wapen of 2.jaag je met handen: ")
       if choice_3 =="1":
           print("je maakt een wapen en zoekt gelijk naar prooi \n je komt een beer te gemoet en breekt je wapen tijdens het gevecht en gaat dood -100")
           hp -= 100
       elif choice_3 == "2":
           print("je besluit om met je handen te jagen en vangt een vis")
    return hp
           
start_game()