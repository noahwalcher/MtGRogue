def dispatch(cardOne, cardTwo):
    assignFramingType(cardOne)
    assignFramingType(cardTwo)

    print()


def assignFramingType(card):
    mainCard = card['mainCard']
    if mainCard[3]: #Check if double faced
        print("Double Faced")
        if ("Sorin" in mainCard[10]):
            card['frameType'] = "M"
        elif ("Voldaren" in mainCard[10]):
            card['frameType'] = "F"
        elif ("Profane" in mainCard[10]):
            card['frameType'] = "N"
        else:
            print(f'Couldnt find a match for {card}')
    else:
        print("Not Double Faced")
        if ("Equipment" in mainCard[14]):
            card['frameType'] = "B"
        elif ("Land" in mainCard[14]):
            card['frameType'] = "K"
        elif ("Saga" in mainCard[14]):
            card['frameType'] = "I"
        elif ("Adventure" in mainCard[14] and "Enchantment" in mainCard[14]):
            card['frameType'] = "H"
        elif ("Enchantment" in mainCard[14]):
            card['frameType'] = "G"
        elif ("Adventure" in mainCard[14] and "Creature" in mainCard[14]):
            card['frameType'] = "E"
        elif ("Artifact" in mainCard[14]):
            card['frameType'] = "A"
        elif ("Planeswalker" in mainCard[14]):
            card['frameType'] = "L"
        elif ("Creature" in mainCard[14]):
            card['frameType'] = "D"
        elif ("Sorcery" in mainCard[14]):
            card['frameType'] = "C"
        elif ("Instant" in mainCard[14]):
            card['frameType'] = "J"
        else:
            print(f'Couldnt find a match for {card}')
