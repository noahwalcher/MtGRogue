import random

def getRandomTriggers():
    return random.sample(triggers, k=3)

def getRandomEffects():
    return random.sample(effects, k=3)

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