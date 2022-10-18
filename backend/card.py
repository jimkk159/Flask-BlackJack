import uuid
import random
from flask import Blueprint

suits = ["spade", "heart", "diamond", "club"]
poker_symbol = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
poker_value_dict = {"K": 13, "Q": 12, "J": 11, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5,
                    "4": 4, "3": 3, "2": 2, "A": 1}

card_blueprint = Blueprint('card', __name__)


class Card:

    def __init__(self, symbol, suit, faced=True):
        # self.id = id_
        self.symbol = symbol
        self.suit = suit
        self.value = poker_value_dict[symbol]
        self.faced = faced

    # GET
    def get_symbol(self):
        return self.symbol

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def get_faced(self):
        return self.faced

    # SET
    def set_value(self, value):
        self.value = value

    def set_faced(self, faced):
        self.faced = faced


class Deck:

    def __init__(self, deck_num):
        self.deck_num = deck_num
        self.deck = self.get_multi_new_deck(self.deck_num)

    # GET
    def get_cards_num(self):
        return len(self.deck)

    def get_deck_num(self):
        return self.deck_num

    def get_deck(self):
        return self.deck

    def get_new_deck(self):
        return [Card(symbol, suit) for symbol in poker_symbol for suit in suits]

    def get_multi_new_deck(self, deck_num):
        deck = []
        for _ in range(deck_num):
            deck += self.get_new_deck()
        return deck

    def get_print_deck(self):

        count = 0
        for card in self.deck:

            print(card.suit, card.symbol, " ", end="")
            count += 1
            if count == 4:
                print()
                count = 0

    # Set
    def shuffle(self):
        random.shuffle(self.deck)

    def reset_deck(self):
        self.deck = self.get_multi_new_deck(self.deck_num)
        self.shuffle()
