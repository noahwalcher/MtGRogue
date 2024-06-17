import random

def getRandomTriggers():
    return random.sample(triggers, k=3)

def getRandomEffects():
    return random.sample(effects, k=3)

def getRandomCompanion():
    return random.sample(companions, k=3)

def getRandomCreatureUpgrades():
    return random.sample(creatureUpgrades, k=3)

def getRandomArtifactEnchantmentUpgrades():
    return random.sample(artifactEnchantmentUpgrades, k=3)

def getRandomSpellUpgrades():
    return random.sample(spellUpgrades, k=3)

def getRandomLandUpgrades():
    return random.sample(landUpgrades, k=3)

triggers = [
    "Whenever an artifact enters the battlefield under your control",
    "Whenever you discard a card",
    "Whenever one or more cards leave your graveyard",
    "Whenever a zombie enters the battlefield under your control",
    "Whenever you sacrifice a creature",
    "Whenever you gain life",
    "Whenever you lose life",
    "At the beginning of your upkeep, if you have no cards in hand",
    "Whenever you cast your second spell each turn",
    "At the beginning of your upkeep, if you have delirium"
]

effects = [
    "gain 1 life",
    "lose 1 life",
    "surveil 1",
    "amass 1",
    "discard a card, then draw a card",
    "add 1 to your mana pool",
    "gain 1 gold",
    "increase the number needed to roll a rare card by 1",
    "target creature gets +1/+1 until end of turn",
    "deal 1 damage to any target",
    "target card in your hand gains delve until end of turn"
]

companions = [
    "Companion — You have discarded a card this turn",
    "Companion — You control an artifact",
    "Companion — You control a zombie",
    "Companion — Delirium",
    "Companion — Hellbent",
    "Companion — You have sacrificed a creature this turn",
    "Companion — You have gained life this turn",
    "Companion — You have lost life this turn",
    "Companion — A card has left your graveyard this turn",
]

creatureUpgrades = [
    "This creature gets +1/+0.",
    "This creature gets +0/+1.",
    "This creature costs {1} less to cast.",
    "Trample",
    "Vigilance",
    "Lifelink",
    "Unearth equal to mana cost",
    "Dredge 1",
    "Cycling {1}",
    "Delve",
    "Whenever you lose life put a +1/+1 counter on this creature.",
    "Amass 1",
    "When this creature enters the battlefield, create a food token.",
    "When this creature dies, create a treasure token.",
    "Haste",
    "Menace",
    "Fabricate 1",
    "Extort",
    "Whenever this creature deals combat damage to an opponent, gain 1 gold.",
    "Flash",
    "Exploit (When this creature enters the battlefield, you may sacrifice a creature.)",
    "{T}: Add {1}",
    "Changeling (This card is every creature type.)",
    "Deathtouch",
    "First strike",
    "Double strike",
    "Flying",
    "Hexproof"
]

artifactEnchantmentUpgrades = [
    "Dredge 1",
    "Delve",
    "Cycling {1}",
    "This card costs {1} less to cast",
    "Creatures your opponents control enter the battlefield tapped.",
    "Delirium — At the beginning of your upkeep mill a card",
    "{T}: Add {1}",
    "Extort",
    "Zombies get +1/+0.",
    "{3}, Sacrifice this card: Return target card from your graveyard to your hand.",
    "Whenever you cast your second spell in a turn, gain 1 life.",
    "Play with the top card of your library revealed.",
    "You have no maximum hand size.",
    "{3}, Sacrifice this card: Search your library for a basic land and put it onto the battlefield.",
    "{2}, Sacrifice a creature: This card deals 1 damage to any target.",
    "When this card enters the battlefield, untap target permanent.",
    "At the beginning of your upkeep choose one: each player gains 1 life or each player loses 1 life.",
    "Sacrifice this card: Draw a card.",
    "Indestructible",
    "Whenever one or more cards leave your graveyard, gain 1 gold.",
    "When this card enters the battlefield, Surveil 1.",
    "{T}, Pay 1 life: Put target card from your graveyard on the bottom of your library.",
    "When this card leaves the battlefield, draw a card."
]

landUpgrades = [
    "{T}, Exert this land: Add {2}",
    "Cycling {1}",
    "Dredge 1",
    "You may cast this card for {1}.",
    "{3}, {T}: Amass 1",
    "{2}: Return this card from your graveyard to the battlefield under your control.",
    "When this land enters the battlefield, untap it.",
    "Pay 1 life, Sacrifice a creature, {T}: Create a treasure token.",
    "{T}, Sacrifice this land: Search your library for a basic land card and put it onto the battlefield.",
    "Delirium — {T}, Sacrifice this land: Return target card from your graveyard to your hand.",
    "When this land enters the battlefield, it deals 1 damage to any target.",
    "{2}, {T}, Sacrifice this land: Draw a card.",
    "This land enters the battlefield tapped. When it does, surveil 1.",
    "{4}: This land becomes a 1/1 Zombie creature with deathtouch until end of turn. It's still a land.",
    "Play with the top card of your library revealed.",
    "Channel — {2}, Discard this card: Gain 2 gold.",
    "You may reveal this card from your opening hand. If you do, mill 4."
]

spellUpgrades = [
    "Flashback equal to mana cost",
    "Dredge 1",
    "Delve",
    "This card costs {1} less to cast.",
    "Amass 1",
    "Surveil 1",
    "Create a treasure token.",
    "Create a blood token.",
    "Create a food token.",
    "Investigate.",
    "Draw a card, then discard a card.",
    "Lose 2 life. Return target card from your graveyard to your hand.",
    "You may reveal this card from your opening hand. If you do, gain 3 gold.",
    "Put a +1/+1 counter on target creature.",
    "Put a -1/-1 counter on target creature.",
    "Scry 2.",
    "Discard a card, then draw a card",
    "Cycling {1}",
    "Target creature gets +1/-1 until end of turn.",
    "Tap target creature.",
    "Gain 1 life.",
    "Lose 1 life.",
    "Deal 1 damage to any target.",
    "You may exchange 1 item for a random item.",
    "Overload {5} (You may cast this spell for its overload cost. If you do, change “target” in its text to “each.”)"
]