import sqlite3
import os
from pathlib import Path
import requests
import shutil
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
from fuzzywuzzy import process


def connect_db(db_name='mtg_cards.db'):
    return sqlite3.connect(db_name)

def fetch_card_by_id(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM cards
        WHERE oracle_id = ?
    ''', (id,))
    
    card = cursor.fetchone()
    if card:
        card_keys = [description[0] for description in cursor.description]
        card_dict = dict(zip(card_keys, card))

        card_id = card_dict['oracle_id']
        card_faces = fetch_card_faces(card_id)
        return {'mainCard': card, 'faces': card_faces}
    else:
        print(f"No card found with the id '{id}'")

def fetch_card_by_name(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM cards
        WHERE LOWER(name) = LOWER(?)
    ''', (name,))
    
    card = cursor.fetchone()
    if card:
        card_keys = [description[0] for description in cursor.description]
        card_dict = dict(zip(card_keys, card))

        card_id = card_dict['oracle_id']
        card_faces = fetch_card_faces(card_id)
        return {'mainCard': card, 'faces': card_faces}
    else:
        cursor.execute('''
            SELECT * FROM card_faces
            WHERE LOWER(name) = LOWER(?)
        ''', (name,))
        
        card_face = cursor.fetchone()
        if card_face:
            card_face_keys = [description[0] for description in cursor.description]
            card_face_dict = dict(zip(card_face_keys, card_face))
                        
            card_id = card_face_dict['id']
            return fetch_card_by_id(card_id)
        else:
            print(f"Card and card face not found for name: {name}")

def fetch_card_faces(card_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM card_faces
        WHERE id = ?
    ''', (card_id,))
    
    card_faces = cursor.fetchall()
    # if card_faces:
    #     card_faces_keys = [description[0] for description in cursor.description]
    # else:
    #     print("No faces found for this card.")
    return card_faces


def download_card_images(card_names):
    conn = connect_db()
    cursor = conn.cursor()

    # Create directory if it doesn't exist
    image_folder = 'images'
    Path(image_folder).mkdir(parents=True, exist_ok=True)

    success = True  # Initialize a flag to track the success status

    for name in card_names:
        result = fetch_card_by_name(name)
        if result:
            main_card = result['mainCard']
            faces = result['faces']

            if main_card:
                try:
                    image_uri = main_card[2]
                    oracle_id = main_card[0]

                    image_name = f"{oracle_id}.jpg"
                    image_path = os.path.join(image_folder, image_name)

                    # Check if image already exists
                    if os.path.exists(image_path):
                        continue

                    if image_uri:
                        # Download image
                        response = requests.get(image_uri, stream=True, timeout=10)  # Timeout set to 10 seconds
                        response.raise_for_status()  # Raise HTTPError for bad responses

                        with open(image_path, 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        print(f"Downloaded image for '{name}' to '{image_path}'")
                    else:
                        print(f"No image URI found for '{name}'. Checking for faces...")

                        for index, face in enumerate(faces):
                            response = requests.get(face[4], stream=True, timeout=10)
                            response.raise_for_status()

                            image_name = f"{oracle_id}FACE{index + 1}.jpg"
                            image_path = os.path.join(image_folder, image_name)

                            if os.path.exists(image_path):
                                continue

                            with open(image_path, 'wb') as out_file:
                                shutil.copyfileobj(response.raw, out_file)
                            print(f"Downloaded image for face of '{name}' to '{image_path}'")

                except requests.exceptions.RequestException as e:
                    print(f"Failed to download image for '{name}': {str(e)}")
                    success = False  # Set the flag to False if any image download fails

        else:
            print(f"Card '{name}' not found in the database.")
            success = False  # Set the flag to False if the card is not found

    conn.close()
    return success  # Return the success status

with open('mtg_rogue.txt', 'r') as file:
    custom_words = [line.strip().lower() for line in file]

def main():
    image = Image.open("testOCR.jpg")
    gray_image = ImageOps.grayscale(image)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2)
    custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-û " --user-words C:\\Users\\noahw\\devl\\MtGRogueMachine\\mtg_rogue.txt'

    # Apply thresholding
    binary_image = enhanced_image.point(lambda x: 0 if x < 140 else 255, '1')
    text = pytesseract.image_to_string(binary_image, config=custom_config).strip().lower()

    best_match, score = process.extractOne(text, custom_words)
    print(f"best match -> {best_match.replace('ã»', 'û')}")
    print(f"score here -> {score}")

     
    print(f"Our text here!!--> {text}")
    return
    file_path = 'mtg_rogue.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        card_names = [line.strip() for line in file.readlines()]

    # download_card_images(card_names)
    choice = input("fetch or combine")
    if "fetch" in choice:
        card = input("Card Name")
        print(f"card name here -> {card}")
        print(fetch_card_by_id(card))
    elif "combine" in choice:
        card_name = input("Enter the name of the card: ")
        cardOne = fetch_card_by_name(card_name)
        card_name = input("Enter the name of the 2nd card: ")
        cardTwo = fetch_card_by_name(card_name)

        combine.combine(cardOne, cardTwo)

if __name__ == '__main__':
    main()
