import sqlite3
import json
import requests

def fetch_scryfall_data():
    scryfall_bulk_data_url = 'https://api.scryfall.com/bulk-data'
    response = requests.get(scryfall_bulk_data_url)
    bulk_data = response.json()

    # Find the Oracle Cards data object
    oracle_cards_data = next(item for item in bulk_data['data'] if item['type'] == 'oracle_cards')
    oracle_cards_url = oracle_cards_data['download_uri']

    # Download the Oracle Cards data
    response = requests.get(oracle_cards_url)
    cards_data = response.json()

    # Save cards_data to a JSON file
    filename = 'scryfall_oracle_cards.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=4)

    return cards_data

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        oracle_id TEXT PRIMARY KEY,
        layout TEXT,
        image_uri TEXT,
        has_multiple_faces BOOLEAN,
        cmc REAL,
        color_identity TEXT,
        colors TEXT,
        defense TEXT,
        loyalty TEXT,
        mana_cost TEXT,
        name TEXT,
        oracle_text TEXT,
        power TEXT,
        toughness TEXT,
        type_line TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS card_faces (
        id TEXT,
        cmc REAL,
        colors TEXT,
        defense TEXT,
        image_uri TEXT,
        loyalty TEXT,
        mana_cost TEXT,
        name TEXT PRIMARY KEY,
        power TEXT,
        toughness TEXT,
        type_line TEXT,
        oracle_text TEXT,
        FOREIGN KEY(id) REFERENCES cards(id)
    )
    ''')
    #CMC doesn't seem to exist on any card_faces

def insert_card_data(cursor, card):
    if '//' in card['name']:

        parts = card['name'].replace(' ', '').split('//')
        if len(parts) == 2 and parts[0] == parts[1]:
            return
        
    if (card['set_type'] == "funny" or 
        card['set_type'] == "alchemy" or 
        card['set_type'] == "memorabilia" or 
        card['set_type'] == "token" or 
        card['type_line'] == "Scheme" or 
        card['type_line'] == "Vanguard" or 
        card['layout'] == "planar" or 
        card['set_type'] == "minigame" or 
        card['set_name'] == "Sega Dreamcast Cards" or 
        card['set_name'] == "Astral Cards"):
        return

    card_values = (
        card['oracle_id'], card.get('layout', ''), card.get('image_uris', {}).get('large', ''), 'card_faces' in card, card.get('cmc', None),
        ','.join(card.get('color_identity', [])), ','.join(card.get('colors', [])), card.get('defense', ''), card.get('loyalty', ''), card.get('mana_cost', ''),
        card['name'], card.get('oracle_text', ''), card.get('power', ''), card.get('toughness', ''), card['type_line']
    )

    cursor.execute('''
    INSERT OR IGNORE INTO cards (
        oracle_id, layout, image_uri, has_multiple_faces, cmc, color_identity, colors, defense, 
        loyalty, mana_cost, name, oracle_text, power, toughness, type_line
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', card_values)

    if 'card_faces' in card:
            for card_face in card['card_faces']:
                insert_card_face_data(cursor, card['oracle_id'], card_face)

def insert_card_face_data(cursor, card_id, card_face):
    cursor.execute('''
    INSERT OR IGNORE INTO card_faces (
        id, cmc, colors, defense, image_uri, loyalty, mana_cost, name, power, toughness, type_line, oracle_text
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        card_id, card_face.get('cmc', ''), ','.join(card_face.get('colors', [])), card_face.get('defense', ''), card_face.get('image_uris', {}).get('large', ''), card_face.get('loyalty', ''), 
        card_face['mana_cost'], card_face['name'], card_face.get('power', ''), card_face.get('toughness', ''), card_face.get('type_line', ''), card_face.get('oracle_text', '')
    ))

def main():
    # Fetch Scryfall data
    cards_data = fetch_scryfall_data()

    # Connect to SQLite database
    conn = sqlite3.connect('mtg_cards.db')
    cursor = conn.cursor()

    # Create tables
    create_tables(cursor)

    # Insert data into tables
    for card in cards_data:
        insert_card_data(cursor, card)
        

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
