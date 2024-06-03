import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

def combine(cardOne, cardTwo):
    if os.path.exists('id_counter.txt'):
        with open('id_counter.txt', 'r') as file:
            id = int(file.read().strip())
    else:
            id = 1
    if (cardOne['mainCard'][1] == "normal" and "Planeswalker" not in cardOne['mainCard'][14]):
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            normalNormal(cardOne, cardTwo, id)
        elif cardTwo['mainCard'][1] == "saga":
            normalSaga(cardOne, cardTwo, id)
        elif cardTwo['mainCard'][1] == "adventure":
            normalAdventure(cardOne, cardTwo, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            normalPlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")
    elif cardOne['mainCard'][1] == "saga":
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            normalSaga(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "saga":
            sagaSaga(cardOne, cardTwo, id)
        elif cardTwo['mainCard'][1] == "adventure":
            sagaAdventure(cardOne, cardTwo, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            sagaPlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")
    elif cardOne['mainCard'][1] == "adventure":
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            normalAdventure(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "saga":
            sagaAdventure(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "adventure":
            adventureAdventure(cardOne, cardTwo, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            adventurePlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")
    elif "Planeswalker" in cardOne['mainCard'][14]:
        if (cardTwo['mainCard'][1] == "normal" and "Planeswalker" not in cardTwo['mainCard'][14]):
            normalPlaneswalker(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "saga":
            sagaPlaneswalker(cardTwo, cardOne, id)
        elif cardTwo['mainCard'][1] == "adventure":
            adventurePlaneswalker(cardTwo, cardOne, id)
        elif "Planeswalker" in cardTwo['mainCard'][14]:
            planeswalkerPlaneswalker(cardOne, cardTwo, id)
        else:
            print("Not sure what to do with these cards")

    id += 1
    with open('id_counter.txt', 'w') as file:
            file.write(str(id))

titleFont = ImageFont.truetype("Fonts/beleren-bold_P1.01.ttf", size=20)
typeFont = ImageFont.truetype("Fonts/beleren-bold_P1.01.ttf", size=16)
bodyFont = ImageFont.truetype("Fonts/mplantin.ttf", size=14)
flipsideTitleFont = ImageFont.truetype("Fonts/mplantin.ttf", size=12)

standardTitleCoord = (32, 28)
offsetTitleCoord = (59, 28)
fuseTitleCoord1 = (49, 23)
fuseTitleCoord2 = (290, 23)
adventureTitleCoord = (32, 331)
planeswalkerTitleCoord = ()
aftermathTitleCoord = (295, 30)

standardTypeCoord = (33, 298)
fullTextTypeCoord = (33, 65)
fuseTypeCoord1 = (48, 210)
fuseTypeCoord2 = (289, 210)
adventureTypeCoord = (33, 355)
aftermathTypeCoord1 = (31, 185)
aftermathTypeCoord2 = (296, 177)

standardBodyCoord = (33, 332, 339, 480)
fullTextBodyCoord = (33, 98, 339, 467)
fuseBodyCoord1 = (48, 237, 251, 330)
fuseBodyCoord2 = (289, 237, 492, 330)
adventureBodyCoord1 = (194, 332, 347, 479)
adventureBodyCoord2 = (33, 379, 183, 479)
planeswalkerBodyCoord = ()
aftermathBodyCoord1 = (33, 218, 342, 275)
aftermathBodyCoord2 = (303, 260, 473, 342)

#3rd/4th number are the size of the mana symbols
standardManaCoord = (346, 31, 17, 18)
fuseManaCoord1 = (256, 28, 15, 16)
fuseManaCoord2 = (498, 28, 15, 16)
MDFCManaCoord = (160, 472, 11, 11)
adventureManaCoord = (180, 333, 14, 15)
aftermathManaCoord = (476, 34, 17, 18)

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

        #draw.text((x, y), "\n".join(lines), font=font, fill="black")
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
def createCardImage(card, framePath, titleCoord, typeCoord, textCoord, manaCoord, flipsideTitleCoords = None, card2 = None, title2Coord = None, type2Coord = None, text2Coord = None, manaCoord2 = None):
    frame = Image.open(framePath)
    draw = ImageDraw.Draw(frame)
    draw.text(titleCoord, card["name"], font=titleFont, fill="black")
    drawManaCost(frame, card["mana_cost"], manaCoord)
    draw.text(typeCoord, card["type_line"], font=typeFont, fill="black")
    if (card["power"] and card["toughness"]):
        box = Image.open("ManaSymbols/clpt.png").resize((81, 42))
        frame.paste(box, (274, 466), box)
        draw.text((316, 483), f"{card['power']}/{card['toughness']}", font=titleFont, fill="black", align="center", anchor="mm")
    itFits = draw_text_within_bounding_box(frame, draw, card["oracle_text"], "Fonts/mplantin.ttf", 14, textCoord)
    if flipsideTitleCoords and card2:
        if "Back" in framePath:
            draw.text(flipsideTitleCoords, getMainType(card2["type_line"]), font=flipsideTitleFont, fill="black")
            drawManaCost(frame, card2["mana_cost"], MDFCManaCoord)
        else:
            draw.text(flipsideTitleCoords, getMainType(card2["type_line"]), font=flipsideTitleFont, fill="white")
            drawManaCost(frame, card2["mana_cost"], MDFCManaCoord)
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
        createCardImage(card, "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card2)
        createCardImage(card2, "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card)
    elif ("Frames/Standard.png" == framePath) and not itFits:
        createCardImage(card, "Frames/FullText.png", standardTitleCoord, fullTextTypeCoord, fullTextBodyCoord, standardManaCoord)
    elif ():#TODO handle all cases where card needs extended body room
        #Might be able to combine a lot of these. Need to see once we get further
        print()
    else:
        print("Saving")
        #TODO Add card object to database
        frame.save(f"test/{card["name"]}.png")

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
            "name": newName,
            "mana_cost": manaCost,
            "cmc": cmc,
            "type_line": f"{newFullTypeLine}",
            "oracle_text": oracle.replace(cardOne['mainCard'][10], newName),
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
    if cardOne['mainCard'][12]:
        power1 = cardOne['mainCard'][12]
    if cardTwo['mainCard'][12]:
        power2 = cardTwo['mainCard'][12]
    if cardOne['mainCard'][13]:
        toughness1 = cardOne['mainCard'][13]
    if cardTwo['mainCard'][13]:
        toughness2 = cardTwo['mainCard'][13]
    return {
        "oracle_id": id,
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
                "toughness": toughness1
            },
            {
                "object": "card_face",
                "name": newNameTwo,
                "mana_cost": cardTwo['mainCard'][9],
                "type_line": cardTwo['mainCard'][14],
                "oracle_text": cardTwo['mainCard'][11].replace(cardTwo['mainCard'][10], newNameTwo),
                "power": power2,
                "toughness": toughness2
            }
        ]
    }

def normalNormal(cardOne, cardTwo, id):
    typeLineOne = cardOne['mainCard'][14]
    typeLineTwo = cardTwo['mainCard'][14]
    if ('Instant' in typeLineOne and 'Instant' in typeLineTwo) or ('Sorcery' in typeLineOne and 'Sorcery' in typeLineTwo):
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
        createCardImage(card["card_faces"][0], "Frames/Fuse.png", fuseTitleCoord1, fuseTypeCoord1, fuseBodyCoord1, fuseManaCoord1, card2 = card["card_faces"][1], title2Coord=fuseTitleCoord2, type2Coord=fuseTypeCoord2, text2Coord=fuseBodyCoord2, manaCoord2=fuseManaCoord2 )
    elif ('Instant' in typeLineOne and 'Sorcery' in typeLineTwo) or ('Sorcery' in typeLineOne and 'Instant' in typeLineTwo):
        oracle_text_1 = cardOne['mainCard'][11]
        oracle_text_2 = cardTwo['mainCard'][11]
        if oracle_text_1 < oracle_text_2:
            card = createTwoFaceCardObject(cardOne, cardTwo, id)
        else:
            card = createTwoFaceCardObject(cardTwo, cardOne, id)
        createCardImage(card["card_faces"][0], "Frames/Aftermath.png", standardTitleCoord, aftermathTypeCoord1, aftermathBodyCoord1, standardManaCoord, card2=card["card_faces"][1], title2Coord=aftermathTitleCoord, type2Coord=aftermathTypeCoord2, text2Coord=aftermathBodyCoord2, manaCoord2=aftermathManaCoord)
    elif 'Instant' in typeLineOne or 'Instant' in typeLineTwo or 'Sorcery' in typeLineOne or 'Sorcery' in typeLineTwo:
        if ('Instant' in typeLineOne or 'Sorcery' in typeLineOne):
            cardOne, cardTwo = cardTwo, cardOne
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
        createCardImage(card["card_faces"][0], "Frames/Adventure.png", standardTitleCoord, standardTypeCoord, adventureBodyCoord1, standardManaCoord, card2=card["card_faces"][1], title2Coord=adventureTitleCoord, type2Coord=adventureTypeCoord, text2Coord=adventureBodyCoord2, manaCoord2=adventureManaCoord)
    elif ('Land' in typeLineOne or 'Land' in typeLineTwo) or ("X" in cardOne['mainCard'][9] or "X" in cardTwo['mainCard'][9]) or ("X" in cardOne['mainCard'][12] or "X" in cardOne['mainCard'][13] or "X" in cardTwo['mainCard'][12] or "X" in cardTwo['mainCard'][13]):
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
        createCardImage(card["card_faces"][0], "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][1])
        createCardImage(card["card_faces"][1], "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card["card_faces"][0])
    else:
        card = createSingleFaceCardObject(cardOne, cardTwo, id)
        createCardImage(card, "Frames/Standard.png", standardTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord)


def normalSaga(cardOne, cardTwo, id):
    print()

def normalAdventure(cardOne, cardTwo, id):
    print()

def normalPlaneswalker(cardOne, cardTwo, id):
    print()

def sagaSaga(cardOne, cardTwo, id):
    print()

def sagaAdventure(cardOne, cardTwo, id):
    print()

def sagaPlaneswalker(cardOne, cardTwo, id):
    print()

def adventureAdventure(cardOne, cardTwo, id):
    print()

def adventurePlaneswalker(cardOne, cardTwo, id):
    print()

def planeswalkerPlaneswalker(cardOne, cardTwo, id):
    print()
