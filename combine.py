import json
import os
from PIL import Image, ImageDraw, ImageFont

def combine(cardOne, cardTwo):
    print("In combine method")

    if os.path.exists('id_counter.txt'):
        with open('id_counter.txt', 'r') as file:
            id = int(file.read().strip())
    else:
            id = 1

    print(f"Counter number: {id}")

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
flipsideTitleFont = ImageFont.truetype("Fonts/mplantin.ttf", size=11)

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
        
#Pass the face in if card is multifaced
#TODO add cmc to card
def createCardImage(card, framePath, titleCoord, typeCoord, textCoord, flipsideTitleCoords = None, card2 = None, title2Coord = None, type2Coord = None, text2Coord = None):
    frame = Image.open(framePath)
    draw = ImageDraw.Draw(frame)
    draw.text(titleCoord, card["name"], font=titleFont, fill="black")
    draw.text(typeCoord, card["type_line"], font=typeFont, fill="black")
    itFits = draw_text_within_bounding_box(draw, card["oracle_text"], "Fonts/mplantin.ttf", 14, textCoord)
    print(f"flipside title coord -> {flipsideTitleCoord}")
    print(f"card 2 -> {card2}")
    if flipsideTitleCoord and card2:
        print('Made it into the if for flipside')
        #TODO also need to add in cmc on flipside panel
        if "Back" in framePath:
            draw.text(flipsideTitleCoord, card2["name"], font=flipsideTitleFont, fill="black")
        else:
            draw.text(flipsideTitleCoord, card2["name"], font=flipsideTitleFont, fill="white")

    if card2 and title2Coord and type2Coord and text2Coord:
        draw.text(title2Coord, card2["name"], font=titleFont, fill="black")
        draw.text(type2Coord, card2["type_line"], font=typeFont, fill="black")
        itFits2 = draw_text_within_bounding_box(draw, card2["oracle_text"], "Fonts/mplantin.ttf", 14, text2Coord)
    #extend frame based on prior frame
    if "Fuse" in framePath and (itFits or not itFits2):
        print("Was fuse but making mdfc")
        createCardImage(card, "Frames/StandardMDFCFront.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card2)
        createCardImage(card2, "Frames/StandardMDFCBack.png", offsetTitleCoord, standardTypeCoord, standardBodyCoord, flipsideTitleCoords=flipsideTitleCoord, card2=card)
    elif ():#TODO handle all cases where card needs extended body room
        print()
    else:
        print("Saving")
        frame.save(f"test/{card["name"]}.png")
        #TODO Lastly save the image

def createTwoFaceCardObject(cardOne, cardTwo, id):
    return {
        "oracle_id": id,
        "name": f"Experiment {id}",
        "layout": "fuse",
        "mana_cost": "",
        "cmc": "",
        "type_line": f"{cardOne['mainCard'][14]} // {cardTwo['mainCard'][14]}",
        "colors": "",
        "card_faces": [
            {
                "object": "card_face",
                "name": f"Experiment {id} - A",
                "mana_cost": cardOne['mainCard'][9],
                "type_line": cardOne['mainCard'][14],
                "oracle_text": cardOne['mainCard'][11]
            },
            {
                "object": "card_face",
                "name": f"Experiment {id} - B",
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
        #def createCardImage(card, framePath, titleCoord, typeCoord, textCoord, flipsideTitleCoord = None, card2 = None, title2Coord = None, type2Coord = None, text2Coord = None):
        createCardImage(card["card_faces"][0], "Frames/Fuse.png", fuseTitleCoord1, fuseTypeCoord1, fuseBodyCoord1, card2 = card["card_faces"][1], title2Coord=fuseTitleCoord2, type2Coord=fuseTypeCoord2, text2Coord=fuseBodyCoord2 )
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
