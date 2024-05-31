import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

def combine(cardOne, cardTwo):
    print("In combine method")

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

standardTitleCoord = ()
offsetTitleCoord = (59, 28)
fuseTitleCoord1 = (49, 23)
fuseTitleCoord2 = (290, 23)
adventureTitleCoord = ()
planeswalkerTitleCoord = ()
aftermathTitleCoord = ()

standardTypeCoord = (33, 298)
fuseTypeCoord1 = (48, 210)
fuseTypeCoord2 = (289, 210)
adventureTypeCoord = ()
aftermathTypeCoord = ()

standardBodyCoord = (33, 332, 339, 469)
fuseBodyCoord1 = (48, 237, 251, 330)
fuseBodyCoord2 = (289, 237, 492, 330)
adventureBodyCoord = ()
planeswalkerBodyCoord = ()
aftermathBodyCoord = ()

#3rd/4th number are the size of the mana symbols
standardManaCoord = (346, 31, 17, 18)
fuseManaCoord1 = (256, 28, 15, 16)
fuseManaCoord2 = (498, 28, 15, 16)
MDFCManaCoord = (160, 472, 11, 11)
adventureManaCoord = ()
aftermathManaCoord = ()

flipsideTitleCoord = (27, 473)


def draw_text_within_bounding_box(draw, text, fontPath, fontSize, bounding_box):
    font = ImageFont.truetype(fontPath, fontSize)
    x, y, x2, y2 = bounding_box
    lines = text.split('\n')
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
        draw.text((x, y), "\n".join(lines), font=font, fill="black")
        return True
    else:
        if fontSize > 10: #This is the minimum font size that can be adjusted
            return draw_text_within_bounding_box(draw, text, fontPath, fontSize - 1, bounding_box)
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

    # Save or show the modified card image
    frame.save("modified_card.png")

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
    itFits = draw_text_within_bounding_box(draw, card["oracle_text"], "Fonts/mplantin.ttf", 14, textCoord)
    if flipsideTitleCoords and card2:
        if "Back" in framePath:
            draw.text(flipsideTitleCoords, getMainType(card2["type_line"]), font=flipsideTitleFont, fill="black")
            drawManaCost(frame, card2["mana_cost"], MDFCManaCoord)
        else:
            draw.text(flipsideTitleCoords, getMainType(card2["type_line"]), font=flipsideTitleFont, fill="white")
            drawManaCost(frame, card2["mana_cost"], MDFCManaCoord)

    if card2 and title2Coord and type2Coord and text2Coord and manaCoord2:
        draw.text(title2Coord, card2["name"], font=titleFont, fill="black")
        draw.text(type2Coord, card2["type_line"], font=typeFont, fill="black")
        drawManaCost(frame, card2["mana_cost"], manaCoord2)
        itFits2 = draw_text_within_bounding_box(draw, card2["oracle_text"], "Fonts/mplantin.ttf", 14, text2Coord)
    #extend frame based on prior frame
    if "Fuse" in framePath and (not itFits or not itFits2):
        print("Was fuse but making mdfc")
        createCardImage(card, "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card2)
        createCardImage(card2, "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, standardManaCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card)
    elif ():#TODO handle all cases where card needs extended body room
        print()
    else:
        print("Saving")
        frame.save(f"test/{card["name"]}.png")

def createTwoFaceCardObject(cardOne, cardTwo, id):
    return {
        "oracle_id": id,
        "name": f"No. {id}",
        "layout": "fuse",
        "mana_cost": "",
        "cmc": "",
        "type_line": f"{cardOne['mainCard'][14]} // {cardTwo['mainCard'][14]}",
        "colors": "",
        "card_faces": [
            {
                "object": "card_face",
                "name": f"No. {id} - A",
                "mana_cost": cardOne['mainCard'][9],
                "type_line": cardOne['mainCard'][14],
                "oracle_text": cardOne['mainCard'][11]
            },
            {
                "object": "card_face",
                "name": f"No. {id} - B",
                "mana_cost": cardTwo['mainCard'][9],
                "type_line": cardTwo['mainCard'][14],
                "oracle_text": cardTwo['mainCard'][11]
            }
        ]
    }

def normalNormal(cardOne, cardTwo, id):
    typeLineOne = cardOne['mainCard'][14]
    typeLineTwo = cardTwo['mainCard'][14]
    if ('Instant' in typeLineOne and 'Instant' in typeLineTwo) or ('Sorcery' in typeLineOne and 'Sorcery' in typeLineTwo):
        card = createTwoFaceCardObject(cardOne, cardTwo, id)
#def createCardImage(card, framePath, titleCoord, typeCoord, textCoord, manaCoord, flipsideTitleCoords = None, card2 = None, title2Coord = None, type2Coord = None, text2Coord = None, manaCoord2 = None):
        createCardImage(card["card_faces"][0], "Frames/Fuse.png", fuseTitleCoord1, fuseTypeCoord1, fuseBodyCoord1, fuseManaCoord1, card2 = card["card_faces"][1], title2Coord=fuseTitleCoord2, type2Coord=fuseTypeCoord2, text2Coord=fuseBodyCoord2, manaCoord2=fuseManaCoord2 )
    elif ('Instant' in typeLineOne and 'Sorcery' in typeLineTwo) or ('Sorcery' in typeLineOne and 'Instant' in typeLineTwo):
        print('aftermath')
    else:
        print('Two Permanents')


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
