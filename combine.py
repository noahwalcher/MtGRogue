import json
import os
import re
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import fetchAndPopulateDB

def combine(cardOne, cardTwo):
    if os.path.exists('id_counter.txt'):
        with open('id_counter.txt', 'r') as file:
            id = int(file.read().strip())
    else:
            id = 1
    if (cardOne['mainCard'][1] == "normal" and "Planeswalker" not in cardOne['mainCard'][14]):
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            cardImage = normalNormal(cardOne, cardTwo, id)
        elif cardTwo['mainCard'][1] == "saga":
            cardImage = normalSaga(cardOne, cardTwo, id)
        elif cardTwo['mainCard'][1] == "adventure":
            cardImage = normalAdventure(cardOne, cardTwo, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            cardImage = normalPlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")
    elif cardOne['mainCard'][1] == "saga":
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            cardImage = normalSaga(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "saga":
            cardImage = sagaSaga(cardOne, cardTwo, id)
        elif cardTwo['mainCard'][1] == "adventure":
            cardImage = sagaAdventure(cardOne, cardTwo, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            cardImage = sagaPlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")
    elif cardOne['mainCard'][1] == "adventure":
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            cardImage = normalAdventure(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "saga":
            cardImage = sagaAdventure(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "adventure":
            cardImage = adventureAdventure(cardOne, cardTwo, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            cardImage = adventurePlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")
    elif "Planeswalker" in cardOne['mainCard'][14]:
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            cardImage = normalPlaneswalker(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "saga":
            cardImage = sagaPlaneswalker(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "adventure":
            cardImage = adventurePlaneswalker(cardTwo, cardOne, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            cardImage = planeswalkerPlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")

    id += 1
    with open('id_counter.txt', 'w') as file:
            file.write(str(id))

    return [cardImage]

conn = sqlite3.connect('mtg_cards.db')
cursor = conn.cursor()

titleFont = ImageFont.truetype("Fonts/beleren-bold_P1.01.ttf", size=20)
typeFont = ImageFont.truetype("Fonts/beleren-bold_P1.01.ttf", size=16)
bodyFont = ImageFont.truetype("Fonts/mplantin.ttf", size=14)
flipsideTitleFont = ImageFont.truetype("Fonts/mplantin.ttf", size=12)

standardTitleCoord = (32, 28)
offsetTitleCoord = (59, 28)
fuseTitleCoord1 = (49, 23)
fuseTitleCoord2 = (290, 23)
adventureTitleCoord = (32, 331)
offsetPlaneswalkerTitleCoord = (63, 19)
aftermathTitleCoord = (295, 30)

standardTypeCoord = (33, 298)
fullTextTypeCoord = (33, 65)
fuseTypeCoord1 = (48, 210)
fuseTypeCoord2 = (289, 210)
adventureTypeCoord = (33, 355)
aftermathTypeCoord1 = (31, 185)
aftermathTypeCoord2 = (296, 177)
sagaTypeCoord = (33, 445)

standardBodyCoord = (33, 332, 339, 480)
fullTextBodyCoord = (33, 98, 339, 467)
fuseBodyCoord1 = (48, 237, 251, 330)
fuseBodyCoord2 = (289, 237, 492, 330)
adventureBodyCoord1 = (194, 332, 347, 479)
adventureBodyCoord2 = (33, 379, 183, 479)
aftermathBodyCoord1 = (33, 218, 342, 275)
aftermathBodyCoord2 = (303, 260, 473, 342)
saga2ChapterBodyCoord = ((44, 158, 182, 293), (44, 299, 182, 435))
planeswalker3BodyCoord = ((65, 330, 343, 375),(65, 386, 343, 423),(65, 432, 343, 467))
planeswalker3AbilityModifierCoords = ((36, 358), (36, 403), (36, 448))
planeswalkerStartingLoyaltyCoord = (333, 484)

#3rd/4th number are the size of the mana symbols
standardManaCoord = (346, 31, 17, 18)
fuseManaCoord1 = (256, 28, 15, 16)
fuseManaCoord2 = (498, 28, 15, 16)
MDFCManaCoord = (160, 472, 11, 11)
adventureManaCoord = (180, 333, 14, 15)
aftermathManaCoord = (476, 34, 17, 18)
planeswalkerManaCoord = (347, 23, 17, 17)

flipsideTitleCoord = (27, 473)


def draw_text_within_bounding_box(frame, draw, text, fontPath, fontSize, bounding_box):
    font = ImageFont.truetype(fontPath, fontSize)
    x, y, x2, y2 = bounding_box
    lines = text.split('\n')
    space_width = draw.textbbox((0, 0), ' ', font)[2] - draw.textbbox((0, 0), ' ', font)[0]
    pattern = r'(\{.*?\}|[^{}]+)'
    for index, line in enumerate(lines):
        words = line.split()
        wrappedLine = []
        currentLine = ""
        for word in words:
            testLine = f"{currentLine} {word}".strip()
            text_bbox = draw.textbbox((0,0), testLine, font)
            textWidth = text_bbox[2] - text_bbox[0]
            if textWidth <= (x2 - x):
                currentLine = testLine
            else:
                wrappedLine.append(currentLine)
                currentLine = word
        wrappedLine.append(currentLine)
        lines[index:index+1] = wrappedLine
    text_bbox = draw.textbbox((0,0), "\n".join(lines), font)
    textHeight = text_bbox[3] - text_bbox[1]
    if textHeight <= (y2 - y):
        print(f"Printed at {fontSize}")
        current_y = y
        for line in lines:
            getLineHeight = draw.textbbox((0, 0), line, font)
            words = line.split()
            for index, word in enumerate(words):
                if re.search(pattern, word):
                    parsedWord = [match for match in re.findall(pattern, word)]
                    words[index:index+1] = parsedWord                
            current_x = x
            for word in words:
                text_bbox = draw.textbbox((current_x, current_y), word, font)
                textWidth = text_bbox[2] - text_bbox[0]
                if word.startswith("{") and word.endswith("}"):
                    innerSymbol = word[1:-1].lower().replace("/", "")
                    symbol = Image.open(f"ManaSymbols/{innerSymbol}.png").resize((fontSize, fontSize))
                    frame.paste(symbol, (current_x, current_y), symbol)
                    textWidth = fontSize
                    print(f"THIS IS OUR WORD ---> {word}")
                else:        
                    draw.text((current_x, current_y), word, font=font, fill="black")
                current_x += textWidth + space_width
            current_y += getLineHeight[3] -  getLineHeight[1]
        return True
    else:
        if fontSize > 10: #This is the minimum font size that can be adjusted
            print(f"Couldn't fit at {fontSize}. Reducing")
            return draw_text_within_bounding_box(frame, draw, text, fontPath, fontSize - 1, bounding_box)
        else:
            print("Couldn't fit within the bounding box")
            return False
        
def drawManaCost(frame, mana_cost, position):
    # Define the path to mana symbols
    mana_symbol_path = "ManaSymbols/"
    print(f"Here's the mana coord -> {position}")
    
    mana_cost = mana_cost.replace("/", "")
    # Regular expression to find mana symbols
    mana_symbols = re.findall(r'{(.*?)}', mana_cost)
    # Define the size and spacing of mana symbols
    x, y, sizex, sizey = position

    mana_symbol_size = (sizex, sizey)
    spacing = 2

    totalWidth = len(mana_symbols) * (mana_symbol_size[0] + spacing) - spacing
    
    x -= totalWidth
    blackCircle = Image.open("ManaSymbols/black_circle.png").resize(mana_symbol_size)
    for symbol in mana_symbols:
        # Load the mana symbol image
        mana_image_path = f"{mana_symbol_path}{symbol}.png"
        mana_image = Image.open(mana_image_path).resize(mana_symbol_size)

        # Paste the mana symbol image onto the card
        frame.paste(blackCircle, (x-1, y+2), blackCircle)
        frame.paste(mana_image, (x, y), mana_image)

        # Move to the next position
        x += mana_symbol_size[0] + spacing

def getMainType(typeLine):
    if "Planeswalker" in typeLine:
        return "Planeswalker"
    elif "Creature" in typeLine:
        return "Creature"
    elif "Land" in typeLine:
        return "Land"
    elif "Enchantment" in typeLine:
        return "Enchantment"
    elif "Artifact" in typeLine:
        return "Artifact"
    elif "Instant" in typeLine:
        return "Instant"
    elif "Sorcery" in typeLine:
        return "Sorcery"
    else:
        return ""
  
#Pass the face in if card is multifaced
def createCardImage(card, framePath, titleCoord, typeCoord, textCoord, manaCoord, flipsideTitleCoords = None, backCard = None, card2 = None, title2Coord = None, type2Coord = None, text2Coord = None, manaCoord2 = None, databaseCard = None):
    frame = Image.open(framePath)
    draw = ImageDraw.Draw(frame)
    draw.text(titleCoord, card["name"], font=titleFont, fill="black")
    if ("TransformBack" not in framePath):
        drawManaCost(frame, card["mana_cost"], manaCoord)
    draw.text(typeCoord, card["type_line"], font=typeFont, fill="black")
    if (card["power"] and card["toughness"]):
        box = Image.open("ManaSymbols/clpt.png").resize((81, 42))
        frame.paste(box, (274, 466), box)
        draw.text((316, 483), f"{card['power']}/{card['toughness']}", font=titleFont, fill="black", align="center", anchor="mm")
    if ("Saga" in framePath):
        chapters = card["oracle_text"].split("\n")[1:]
        for index, chapter in enumerate(chapters):
            chapter = chapter.split(" — ")[1]
            draw_text_within_bounding_box(frame, draw, chapter, "Fonts/mplantin.ttf", 14, textCoord[index])
    elif ("Planeswalker" in framePath):
        #We don't account for passives or more/less than 3 abilities at the moment
        abilities = card["oracle_text"].split("\n")
        for index, ability in enumerate(abilities):
            loyaltyModifier = ability.split(":")[0]
            draw_text_within_bounding_box(frame, draw, ability, "Fonts/mplantin.ttf", 14, textCoord[index])
            draw.text(planeswalker3AbilityModifierCoords[index], loyaltyModifier, font=typeFont, fill="white", anchor="mm", align="center")
            print(f"Starting loyalty here ----:> {card["loyalty"]}")
            draw.text(planeswalkerStartingLoyaltyCoord, card["loyalty"], font=typeFont, fill="white", anchor="mm", align="center")
    else:
        itFits = draw_text_within_bounding_box(frame, draw, card["oracle_text"], "Fonts/mplantin.ttf", 14, textCoord)
    if flipsideTitleCoords and backCard:
        if "Back" in framePath:
            draw.text(flipsideTitleCoords, getMainType(backCard["type_line"]), font=flipsideTitleFont, fill="black")
            drawManaCost(frame, backCard["mana_cost"], MDFCManaCoord)
        else:
            draw.text(flipsideTitleCoords, getMainType(backCard["type_line"]), font=flipsideTitleFont, fill="white")
            drawManaCost(frame, backCard["mana_cost"], MDFCManaCoord)
    if card2 and title2Coord and type2Coord and text2Coord and manaCoord2:
        if "Aftermath" in framePath:
            rotatedFrame = frame.rotate(90, expand=True)
            draw = ImageDraw.Draw(rotatedFrame)
            draw.text(title2Coord, card2["name"], font=titleFont, fill="black")
            draw.text(type2Coord, card2["type_line"], font=typeFont, fill="black")
            drawManaCost(rotatedFrame, card2["mana_cost"], manaCoord2)
            itFits2 = draw_text_within_bounding_box(frame, draw, card2["oracle_text"], "Fonts/mplantin.ttf", 14, text2Coord)
            frame = rotatedFrame.rotate(-90, expand=True)
        else:
            if ("Adventure" in framePath):
                draw.text(title2Coord, card2["name"], font=typeFont, fill="white")
                draw.text(type2Coord, card2["type_line"], font=typeFont, fill="white")
                drawManaCost(frame, card2["mana_cost"], manaCoord2)
                itFits2 = draw_text_within_bounding_box(frame, draw, card2["oracle_text"], "Fonts/mplantin.ttf", 14, text2Coord)
            else:
                draw.text(title2Coord, card2["name"], font=titleFont, fill="black")
                draw.text(type2Coord, card2["type_line"], font=typeFont, fill="black")
                drawManaCost(frame, card2["mana_cost"], manaCoord2)
                itFits2 = draw_text_within_bounding_box(frame, draw, card2["oracle_text"], "Fonts/mplantin.ttf", 14, text2Coord)
    #extend frame based on prior frame
    if ("Fuse" in framePath or "Aftermath" in framePath or "Adventure" in framePath) and (not itFits or not itFits2):
        print("Didn't fit. Making mdfc")
        cardFront = createCardImage(card, "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card2)
        cardBack = createCardImage(card2, "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card)
        return [cardFront, cardBack]
    elif ("Frames/Standard.png" == framePath) and not itFits:
        return createCardImage(card, "Frames/FullText.png", standardTitleCoord, fullTextTypeCoord, fullTextBodyCoord, standardManaCoord)
    else:
        print("Saving")
        frame.save(f"images/{card["name"]}.png")
        return [frame]

def createSingleFaceCardObject(cardOne, cardTwo, id):
    newName = f"No. {id}"
    newSuperType = ""
    if "Legendary" in cardOne['mainCard'][14] or "Legendary" in cardTwo['mainCard'][14]:
        newSuperType += " Legendary"

    newTypeLine = ""
    if "Artifact" in cardOne['mainCard'][14] or "Artifact" in cardTwo['mainCard'][14]:
        newTypeLine += " Artifact"
    if "Enchantment" in cardOne['mainCard'][14] or "Enchantment" in cardTwo['mainCard'][14]:
        newTypeLine += " Enchantment"
    if "Creature" in cardOne['mainCard'][14] or "Creature" in cardTwo['mainCard'][14]:
        newTypeLine += " Creature"

    newSubType = ""
    if "Equipment" in cardOne['mainCard'][14] or "Equipment" in cardTwo['mainCard'][14]:
        newSubType += " Equipment"
    if "Creature" in cardOne['mainCard'][14] or "Creature" in cardTwo['mainCard'][14]:
        newSubType += " Zombie"

    newFullTypeLine = f"{newSuperType.strip()} {newTypeLine.strip()} — {newSubType.strip()}"
    if "Equipment" in newFullTypeLine and "Creature" in newFullTypeLine:
        if "Equipment" in cardOne['mainCard'][14]:
            cardTwo, cardOne = cardOne, cardTwo
        oracle = cardOne['mainCard'][11]
        equipmentOracle = cardTwo['mainCard'][11]
        equipmentLines = equipmentOracle.split("\n")
        equipCost = ""
        for line in equipmentLines:
            if line.startswith('Equip '):
                equipCost = line.replace("Equip ", "", 1)
        equipmentLinesSansEquip = [s for s in equipmentLines if not s.startswith("Equip ")]
        reducedLinesSansEquip = "\n".join(equipmentLinesSansEquip)
        reconfigureText = f"\nReconfigure {equipCost}\nEquipped Creature has all abilities this card would have as a creature except Reconfigure.\n{reducedLinesSansEquip}"
        oracle += reconfigureText
        return {
            "oracle_id": id,
            "set_type": "Rogue",
            "layout": "Rogue",
            "set_name": "Rogue",
            "name": newName,
            "mana_cost": cardOne['mainCard'][9],
            "cmc": cardOne['mainCard'][4],
            "type_line": f"{newFullTypeLine}",
            "oracle_text": oracle.replace(cardOne['mainCard'][10], newName),
            "power": cardOne['mainCard'][12],
            "toughness": cardOne['mainCard'][13]
        }
    else:
        cmc = cardOne['mainCard'][4] if cardOne['mainCard'][4] > cardTwo['mainCard'][4] else cardTwo['mainCard'][4]
        manaCost = cardOne['mainCard'][9] if cardOne['mainCard'][4] > cardTwo['mainCard'][4] else cardTwo['mainCard'][9]
        oracle = f"{cardOne['mainCard'][11]}\n{cardTwo['mainCard'][11]}"
        power1 = "0"
        power2 = "0"
        toughness1 = "0"
        toughness2 = "0"
        if cardOne['mainCard'][12]:
            power1 = cardOne['mainCard'][12]
        if cardTwo['mainCard'][12]:
            power2 = cardTwo['mainCard'][12]
        if cardOne['mainCard'][13]:
            toughness1 = cardOne['mainCard'][13]
        if cardTwo['mainCard'][13]:
            toughness2 = cardTwo['mainCard'][13]
        power = ""
        toughness = ""

        if power1 is not None and power2 is not None:
            power = int(power1) + int(power2)
        elif power1 is not None:
            power = int(power1)
        elif power2 is not None:
            power = int(power2)

        if toughness1 is not None and toughness2 is not None:
            toughness = int(toughness1) + int(toughness2)
        elif toughness1 is not None:
            toughness = int(toughness1)
        elif toughness2 is not None:
            toughness = int(toughness2)
                
        return {
            "oracle_id": id,
            "set_type": "Rogue",
            "layout": "Rogue",
            "set_name": "Rogue",
            "name": newName,
            "mana_cost": manaCost,
            "cmc": cmc,
            "type_line": f"{newFullTypeLine}",
            "oracle_text": oracle.replace(cardOne['mainCard'][10], newName).replace(cardTwo['mainCard'][10], newName),
            "power": power,
            "toughness": toughness
        }
    
def createTwoFaceCardObject(cardOne, cardTwo, id):
    newName = f"No. {id} - A"
    newNameTwo = f"No. {id} - B"

    power1 = ""
    power2 = ""
    toughness1 = ""
    toughness2 = ""
    loyalty1 = ""
    loyalty2 = ""
    if cardOne['mainCard'][12]:
        power1 = cardOne['mainCard'][12]
    if cardTwo['mainCard'][12]:
        power2 = cardTwo['mainCard'][12]
    if cardOne['mainCard'][13]:
        toughness1 = cardOne['mainCard'][13]
    if cardTwo['mainCard'][13]:
        toughness2 = cardTwo['mainCard'][13]
    if cardOne['mainCard'][8]:
        loyalty1 = cardOne['mainCard'][8]
    if cardTwo['mainCard'][8]:
        loyalty2 = cardTwo['mainCard'][8]
    return {
        "oracle_id": id,
        "set_type": "Rogue",
        "layout": "Rogue",
        "set_name": "Rogue",
        "name": f"No. {id}",
        "mana_cost": "",
        "cmc": "",
        "type_line": f"{cardOne['mainCard'][14]} // {cardTwo['mainCard'][14]}",
        "colors": "",
        "card_faces": [
            {
                "object": "card_face",
                "name": newName,
                "mana_cost": cardOne['mainCard'][9],
                "type_line": cardOne['mainCard'][14],
                "oracle_text": cardOne['mainCard'][11].replace(cardOne['mainCard'][10], newName),
                "power": power1,
                "toughness": toughness1,
                "id": id,
                "loyalty": loyalty1
            },
            {
                "object": "card_face",
                "name": newNameTwo,
                "mana_cost": cardTwo['mainCard'][9],
                "type_line": cardTwo['mainCard'][14],
                "oracle_text": cardTwo['mainCard'][11].replace(cardTwo['mainCard'][10], newNameTwo),
                "power": power2,
                "toughness": toughness2,
                "id": id,
                "loyalty": loyalty2
            }
        ]
    }

def createThreeFaceCardObject(faceOne, faceTwo, cardTwo, id):
    newName = f"No. {id} - A"
    newNameTwo = f"No. {id} - B"
    newNameThree = f"No. {id} - C"

    power1 = ""
    power2 = ""
    power3 = ""
    toughness1 = ""
    toughness2 = ""
    toughness3 = ""
    loyalty1 = ""
    loyalty2 = ""
    loyalty3 = ""
    if faceOne[8]:
        power1 = faceOne[8]
    if faceTwo[8]:
        power2 = faceTwo[8]
    if cardTwo['mainCard'][12]:
        power3 = cardTwo['mainCard'][12]
    if faceOne[9]:
        toughness1 = faceOne[9]
    if faceTwo[9]:
        toughness2 = faceTwo[9]
    if cardTwo['mainCard'][13]:
        toughness3 = cardTwo['mainCard'][13]
    if faceOne[5]:
        loyalty1 = faceOne[5]
    if faceTwo[5]:
        loyalty2 = faceTwo[5]
    if cardTwo['mainCard'][8]:
        loyalty3 = cardTwo['mainCard'][8]

    faceTwoText = faceTwo[11]
    pattern = r'\(Then exile this card\. You may cast the (\w+) later from exile\.\)'
    if re.search(pattern, faceTwo[11]):
        faceTwoText = re.sub(pattern, r"(Then exile this card. You may play a non-adventure card exiled this way.)", faceTwo[11])


    return {
        "oracle_id": id,
        "set_type": "Rogue",
        "layout": "Rogue",
        "set_name": "Rogue",
        "name": f"No. {id}",
        "mana_cost": "",
        "cmc": "",
        "type_line": f"{faceOne[10]} // {faceTwo[10]} // {cardTwo['mainCard'][14]}",
        "colors": "",
        "card_faces": [
            {
                "object": "card_face",
                "name": newName,
                "mana_cost": faceOne[6],
                "type_line": faceOne[10],
                "oracle_text": faceOne[11].replace(faceOne[7], newName),
                "power": power1,
                "toughness": toughness1,
                "id": id,
                "loyalty": loyalty1
            },
            {
                "object": "card_face",
                "name": newNameTwo,
                "mana_cost": faceTwo[6],
                "type_line": faceTwo[10],
                "oracle_text": faceTwoText.replace(faceTwo[7], newNameTwo),
                "power": power2,
                "toughness": toughness2,
                "id": id,
                "loyalty": loyalty2
            },
            {
                "object": "card_face",
                "name": newNameThree,
                "mana_cost": cardTwo['mainCard'][9],
                "type_line": cardTwo['mainCard'][14],
                "oracle_text": cardTwo['mainCard'][11].replace(cardTwo['mainCard'][10], newNameThree),
                "power": power3,
                "toughness": toughness3,
                "id": id,
                "loyalty": loyalty3
            }
        ]
    }

def createFourFaceCardObject(faceOne, faceTwo, faceThree, faceFour, id):
    newName = f"No. {id} - A"
    newNameTwo = f"No. {id} - B"
    newNameThree = f"No. {id} - C"
    newNameFour = f"No. {id} - D"

    power1 = ""
    power2 = ""
    power3 = ""
    power4 = ""
    toughness1 = ""
    toughness2 = ""
    toughness3 = ""
    toughness4 = ""
    if faceOne[8]:
        power1 = faceOne[8]
    if faceTwo[8]:
        power2 = faceTwo[8]
    if faceThree[8]:
        power3 = faceThree[8]
    if faceFour[8]:
        power4 = faceFour[8]
    if faceOne[9]:
        toughness1 = faceOne[9]
    if faceTwo[9]:
        toughness2 = faceTwo[9]
    if faceThree[9]:
        toughness3 = faceThree[9]
    if faceFour[9]:
        toughness4 = faceFour[9]
    faceTwoText = faceTwo[11]
    faceFourText = faceFour[11]
    pattern = r'\(Then exile this card\. You may cast the (\w+) later from exile\.\)'
    if re.search(pattern, faceTwo[11]):
        faceTwoText = re.sub(pattern, r"(Then exile this card. You may play a non-adventure card exiled this way.)", faceTwo[11])
    if re.search(pattern, faceFour[11]):
        faceFourText = re.sub(pattern, r"(Then exile this card. You may play a non-adventure card exiled this way.)", faceFour[11])


    return {
        "oracle_id": id,
        "set_type": "Rogue",
        "layout": "Rogue",
        "set_name": "Rogue",
        "name": f"No. {id}",
        "mana_cost": "",
        "cmc": "",
        "type_line": f"{faceOne[10]} // {faceTwo[10]} // {faceThree[10]} // {faceFour[10]}",
        "colors": "",
        "card_faces": [
            {
                "object": "card_face",
                "name": newName,
                "mana_cost": faceOne[6],
                "type_line": faceOne[10],
                "oracle_text": faceOne[11].replace(faceOne[7], newName),
                "power": power1,
                "toughness": toughness1,
                "id": id
            },
            {
                "object": "card_face",
                "name": newNameTwo,
                "mana_cost": faceTwo[6],
                "type_line": faceTwo[10],
                "oracle_text": faceTwoText.replace(faceTwo[7], newNameTwo),
                "power": power2,
                "toughness": toughness2,
                "id": id
            },
            {
                "object": "card_face",
                "name": newNameThree,
                "mana_cost": faceThree[6],
                "type_line": faceThree[10],
                "oracle_text": faceThree[11].replace(faceThree[7], newNameThree),
                "power": power3,
                "toughness": toughness3,
                "id": id
            },
            {
                "object": "card_face",
                "name": newNameFour,
                "mana_cost": faceFour[6],
                "type_line": faceFour[10],
                "oracle_text": faceFourText.replace(faceFour[7], newNameFour),
                "power": power4,
                "toughness": toughness4,
                "id": id
            },
        ]
    }

def normalNormal(cardOne, cardTwo, id):
    typeLineOne = cardOne['mainCard'][14]
    typeLineTwo = cardTwo['mainCard'][14]
    if ('Instant' in typeLineOne and 'Instant' in typeLineTwo) or ('Sorcery' in typeLineOne and 'Sorcery' in typeLineTwo):
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
        cardImage = createCardImage(card["card_faces"][0], "Frames/Fuse.png", fuseTitleCoord1, fuseTypeCoord1, fuseBodyCoord1, fuseManaCoord1, card2 = card["card_faces"][1], title2Coord=fuseTitleCoord2, type2Coord=fuseTypeCoord2, text2Coord=fuseBodyCoord2, manaCoord2=fuseManaCoord2 )
        fetchAndPopulateDB.insert_card_data(cursor, card)
        conn.commit()
        conn.close()
        return [cardImage]
    elif ('Instant' in typeLineOne and 'Sorcery' in typeLineTwo) or ('Sorcery' in typeLineOne and 'Instant' in typeLineTwo):
        oracle_text_1 = cardOne['mainCard'][11]
        oracle_text_2 = cardTwo['mainCard'][11]
        if oracle_text_1 < oracle_text_2:
            card = createTwoFaceCardObject(cardOne, cardTwo, id)
        else:
            card = createTwoFaceCardObject(cardTwo, cardOne, id)
        cardImage = createCardImage(card["card_faces"][0], "Frames/Aftermath.png", standardTitleCoord, aftermathTypeCoord1, aftermathBodyCoord1, standardManaCoord, card2=card["card_faces"][1], title2Coord=aftermathTitleCoord, type2Coord=aftermathTypeCoord2, text2Coord=aftermathBodyCoord2, manaCoord2=aftermathManaCoord)
        fetchAndPopulateDB.insert_card_data(cursor, card)
        conn.commit()
        conn.close()
        return [cardImage]

    elif 'Instant' in typeLineOne or 'Instant' in typeLineTwo or 'Sorcery' in typeLineOne or 'Sorcery' in typeLineTwo:
        if ('Instant' in typeLineOne or 'Sorcery' in typeLineOne):
            cardOne, cardTwo = cardTwo, cardOne
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
        cardImage = createCardImage(card["card_faces"][0], "Frames/Adventure.png", standardTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, card2=card["card_faces"][1], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
        fetchAndPopulateDB.insert_card_data(cursor, card)
        conn.commit()
        conn.close()
        return [cardImage]
    elif ('Land' in typeLineOne or 'Land' in typeLineTwo) or ("X" in cardOne['mainCard'][9] or "X" in cardTwo['mainCard'][9]) or ("X" in cardOne['mainCard'][12] or "X" in cardOne['mainCard'][13] or "X" in cardTwo['mainCard'][12] or "X" in cardTwo['mainCard'][13]):
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
        cardImage = createCardImage(card["card_faces"][0], "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][1])
        cardImage2 = createCardImage(card["card_faces"][1], "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][0])
        fetchAndPopulateDB.insert_card_data(cursor, card)
        conn.commit()
        conn.close()
        return [cardImage, cardImage2]
    else:
        card = createSingleFaceCardObject(cardOne, cardTwo, id)
        cardImage = createCardImage(card, "Frames/Standard.png", standardTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord)
        fetchAndPopulateDB.insert_card_data(cursor, card)
        conn.commit()
        conn.close()
        return [cardImage]

def normalSaga(cardOne, cardTwo, id):
    typeLineOne = cardOne['mainCard'][14]
    card = createTwoFaceCardObject(cardTwo, cardOne, id)
    sagaLines = cardTwo['mainCard'][11].split('\n')
    if sagaLines[1].startswith("I, II —") and sagaLines[2].startswith("III —") and len(sagaLines) == 3:
        if ('Instant' in typeLineOne or 'Sorcery' in typeLineOne or 'Land' in typeLineOne):
            cardImage = createCardImage(card["card_faces"][0], "Frames/12-3SagaMDFCFront.png", offsetTitleCoord, sagaTypeCoord, saga2ChapterBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][1])
            cardImage2 = createCardImage(card["card_faces"][1], "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][0])
            fetchAndPopulateDB.insert_card_data(cursor, card)
            conn.commit()
            conn.close()
            return [cardImage, cardImage2]
        else:
            cardImage = createCardImage(card["card_faces"][0], "Frames/12-3SagaTransformFront.png", offsetTitleCoord, sagaTypeCoord, saga2ChapterBodyCoord, standardManaCoord, card2=card["card_faces"][1])
            cardImage2 = createCardImage(card["card_faces"][1], "Frames/StandardTransformBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, card2=card["card_faces"][0])
            fetchAndPopulateDB.insert_card_data(cursor, card)
            conn.commit()
            conn.close()
            return [cardImage, cardImage2]

def normalAdventure(cardOne, cardTwo, id):
    card = createThreeFaceCardObject(cardTwo['faces'][0], cardTwo['faces'][1], cardOne, id)
    cardImage = createCardImage(card["card_faces"][0], "Frames/AdventureMDFCFront.png", offsetTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, backCard=card["card_faces"][2] ,flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][1], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
    cardImage2 = createCardImage(card["card_faces"][2], "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][0])
    fetchAndPopulateDB.insert_card_data(cursor, card)
    conn.commit()
    conn.close()
    return [cardImage, cardImage2]

def normalPlaneswalker(cardOne, cardTwo, id):
    card = createTwoFaceCardObject(cardOne, cardTwo, id)
    planeswalkerAbilities = cardTwo['mainCard'][11].split('\n')
    hasPassive = False
    if ":" not in planeswalkerAbilities[0]:
        hasPassive = True
        planeswalkerAbilities = planeswalkerAbilities[1:]
    #Currently only handle planeswalkers with 3 abilities and no passives
    if not hasPassive and len(planeswalkerAbilities) == 3:
        cardImage = createCardImage(card["card_faces"][0], "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][1])
        cardImage2 = createCardImage(card["card_faces"][1], "Frames/3PlaneswalkerMDFCBack.png", offsetPlaneswalkerTitleCoord, standardTypeCoord, planeswalker3BodyCoord, planeswalkerManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][0])
        fetchAndPopulateDB.insert_card_data(cursor, card)
        conn.commit()
        conn.close()
        return [cardImage, cardImage2]

#Don't currently support saga/saga
def sagaSaga(cardOne, cardTwo, id):
    print()

def sagaAdventure(cardOne, cardTwo, id):
    card = createThreeFaceCardObject(cardTwo['faces'][0], cardTwo['faces'][1], cardOne, id)
    cardImage = createCardImage(card["card_faces"][0], "Frames/AdventureMDFCFront.png", offsetTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, backCard=card["card_faces"][2] ,flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][1], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
    cardImage2 = createCardImage(card["card_faces"][2], "Frames/12-3SagaMDFCBack.png", offsetTitleCoord, sagaTypeCoord, saga2ChapterBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][0])
    fetchAndPopulateDB.insert_card_data(cursor, card)
    conn.commit()
    conn.close()
    return [cardImage, cardImage2]

#Only works for specifically formatted planeswalkers/sagas. Needs more logic to handle other cases
def sagaPlaneswalker(cardOne, cardTwo, id):
    card = createTwoFaceCardObject(cardOne, cardTwo, id)
    cardImage = createCardImage(card["card_faces"][0], "Frames/12-3SagaTransformFront.png", offsetTitleCoord, sagaTypeCoord, saga2ChapterBodyCoord, standardManaCoord, card2=card["card_faces"][1])
    cardImage2 = createCardImage(card["card_faces"][1], "Frames/3PlaneswalkerTransformBack.png", offsetPlaneswalkerTitleCoord, standardTypeCoord, planeswalker3BodyCoord, planeswalkerManaCoord, backCard=card["card_faces"][0])
    fetchAndPopulateDB.insert_card_data(cursor, card)
    conn.commit()
    conn.close()
    return [cardImage, cardImage2]

def adventureAdventure(cardOne, cardTwo, id):
    card = createFourFaceCardObject(cardOne['faces'][0], cardOne['faces'][1], cardTwo['faces'][0], cardTwo['faces'][1], id)
    cardImage = createCardImage(card["card_faces"][0], "Frames/AdventureMDFCFront.png", offsetTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, backCard=card["card_faces"][2] ,flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][1], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
    cardImage2 = createCardImage(card["card_faces"][2], "Frames/AdventureMDFCBack.png", offsetTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, backCard=card["card_faces"][0] ,flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][3], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
    fetchAndPopulateDB.insert_card_data(cursor, card)
    conn.commit()
    conn.close()
    return [cardImage, cardImage2]

def adventurePlaneswalker(cardOne, cardTwo, id):
    card = createThreeFaceCardObject(cardOne['faces'][0], cardOne['faces'][1], cardTwo, id)
    cardImage = createCardImage(card["card_faces"][0], "Frames/AdventureMDFCFront.png", offsetTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, backCard=card["card_faces"][2] ,flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][1], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
    cardImage2 = createCardImage(card["card_faces"][2], "Frames/3PlaneswalkerMDFCBack.png", offsetPlaneswalkerTitleCoord, standardTypeCoord, planeswalker3BodyCoord, planeswalkerManaCoord, flipsideTitleCoords=flipsideTitleCoord, backCard=card["card_faces"][0])
    fetchAndPopulateDB.insert_card_data(cursor, card)
    conn.commit()
    conn.close()
    return [cardImage, cardImage2]

#Don't currently have 2 planeswalkers in the list
def planeswalkerPlaneswalker(cardOne, cardTwo, id):
    print()
