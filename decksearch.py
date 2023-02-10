from lor_deckcodes import LoRDeck, CardCodeAndCount
import json
from typing import List
import pathlib
from dataclasses import dataclass

# loading the sets
MAIN_DATA_PATH = pathlib.Path(r"B:\eigene dateien\desktop\bard bot\lor_decks")


deck = LoRDeck.from_deckcode('CUDQCAQAAIAQKAAMAEDACEQBAYCAQAIGA4CAEAIADUWQIBQACEMBWHIDAEBAAAIBAYAAWAIGBQNACAIBAASQ')
card = deck.cards[1]



def load_all_sets(MAIN_DATA_PATH):
    set1_path = MAIN_DATA_PATH / "set1-lite-en_us\en_us\data\set1-en_us.json"
    set2_path = MAIN_DATA_PATH / "set2-lite-en_us\en_us\data\set2-en_us.json"
    set3_path = MAIN_DATA_PATH / "set3-lite-en_us\en_us\data\set3-en_us.json"
    set4_path = MAIN_DATA_PATH / "set4-lite-en_us\en_us\data\set4-en_us.json"
    set5_path = MAIN_DATA_PATH / "set5-lite-en_us\en_us\data\set5-en_us.json"
    set6_path = MAIN_DATA_PATH / "set6-lite-en_us\en_us\data\set6-en_us.json"
    set7_path = MAIN_DATA_PATH / "set6cde-lite-en_us\en_us\data\set6cde-en_us.json"
    all_sets = []
# storing sets from the json
    for i in range(0, 7):
        all_sets_path = [set1_path, set2_path, set3_path, set4_path, set5_path,
        set6_path, set7_path]
        with open(all_sets_path[i], "r", encoding='utf8') as f:
            all_sets.append(json.load(f))

    return all_sets

#
# search function that searches for the dictionary of a single inserted card code(01FR036)
# 
# @returns: dictionary of the given card code
#
def get_card_dictionary_of_card_code(card, all_sets):
    if card.set == 6:
        for card_dictionary in all_sets[5]:
            if card_dictionary.get("cardCode") == card.card_code:               
                return card_dictionary
        for card_dictionary in all_sets[6]:
            if card_dictionary.get("cardCode") == card.card_code:               
                return card_dictionary

    for card_dictionary in all_sets[card.set-1]:
        if card_dictionary.get("cardCode") == card.card_code:   
            return card_dictionary

    raise RuntimeError(f"Cannot find {card} in the given sets.")


def get_card_dictionary_of_card_CODE(card_code, all_sets):
    for card_set in all_sets:
        for card_dictionary in card_set:
            if  card_dictionary["cardCode"] == card_code:
                return card_dictionary
    
    raise RuntimeError(f"Cannot find {card_code} in the given sets.")

#
# sorts a decklist for its card costs 
#
# @returns: a list of tuples with the sorted cards dictionarys and their respective number of copies
#
def sort_for_cost(deck, all_sets):    
    card_list = [(get_card_dictionary_of_card_code(card, all_sets), card.count) for card in deck.cards]
    sorted_card_list = sorted(card_list, key=lambda x:x[0]["cost"])
    return sorted_card_list

#
# get functions that search for the respective card type and puts them into a
# list [number of copies + x, card name]
#
# @returns: list with type of cards
#
def get_champions(deck):
    champion_list = []
    for card in deck:
        if card[0]["supertype"] == "Champion":
            champion_list.append(str(card[1]) + "x " + card[0]["name"])
    return champion_list



def get_units(deck):
    unit_list = []
    for card in deck:
        if card[0]["supertype"] != "Champion" and card[0]["type"] == "Unit":
            unit_list.append(str(card[1]) + "x " + card[0]["name"])
    return unit_list

def get_other(deck):
    other_list = []
    for card in deck:
        if card[0]["type"] == "Equipment" or  card[0]["type"] == "Landmark":
            other_list.append(str(card[1]) + "x " + card[0]["name"])
    return other_list

def get_spells(deck):
    spells_list = []
    for card in deck:
        if card[0]["type"] == "Spell":
            spells_list.append(str(card[1]) + "x " + card[0]["name"])
    return spells_list

#
# read in list of cards
#
# @returns: string of inserted list
#
def card_list_to_string(card_list):
    word = ""
    for card in card_list:
        word += card + "\n"
    return word

#
# search function that inserts a cards name and
# searches for the card image in it's respective dictionary
#
# @returns: the url of a cards respective card Image
#
def get_dictionary_of_card_name(card_name, all_sets):
    card_name = card_name.lower()  
    for card_set in all_sets:
        for card_dictionary in card_set:
            if card_dictionary["name"].lower() == card_name:
                return card_dictionary
    raise RuntimeError(f"Cannot find {card_name} in all_sets")




