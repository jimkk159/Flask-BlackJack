import uuid
import random
from flask import Blueprint

suits = ["spade", "heart", "diamond", "club"]
poker_symbol = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
poker_value = {"K": 13, "Q": 12, "J": 11, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5,
               "4": 4, "3": 3, "2": 2, "A": 1}
poker_value_to_img = {"K": "King", "Q": "Queen", "J": "Jack", "10": "10", "9": "9", "8": "8", "7": "7",
                      "6": "6", "5": "5", "4": "4", "3": "3", "2": "2", "A": "Ace"}
card_blueprint = Blueprint('card', __name__)


class Card:

    def __init__(self, symbol, suit, value=None, faced=True):
        self.id = uuid.uuid1()
        self.suit = suit
        self.symbol = symbol
        self.value = value if value else poker_value[symbol]
        self.faced = faced
        self.img = self.get_card_img(self.suit, self.symbol)
        self.x = 0
        self.y = 0

    # GET
    def get_symbol(self):
        return self.symbol

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def get_faced(self):
        return self.faced

    def get_img(self):
        return self.img

    def get_card_img(self, suit, symbol):
        if suit and symbol:
            return f"{poker_value_to_img[symbol]}_of_{suit}s.svg"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    # SET
    def set_value(self, value):
        self.value = value

    def set_faced(self, faced):
        self.faced = faced

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class Deck:

    def __init__(self, deck_num):
        self.id = uuid.uuid1()
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
