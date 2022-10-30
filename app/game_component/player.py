import uuid
from flask import Blueprint

player_blueprint = Blueprint('player', __name__)


class Hand:

    def __init__(self):
        self.id = uuid.uuid1()
        self.cards = []
        self.is_able_hit = True
        self.is_ace_split = False
        self.is_finish = False
        self._5_card_charlie = False
        self.result = ""

    def get_id(self):
        return self.id

    def get_cards(self):
        return self.cards

    def get_cards_num(self):
        return len(self.cards)

    def get_able_hit(self):
        return self.is_able_hit

    def get_is_ace_split(self):
        return self.is_ace_split

    def get_is_ace_pair(self):
        if len(self.cards) == 2 and self.cards[0].get_symbol() == 'A' and self.cards[1].get_symbol() == 'A':
            return True
        return False

    def get_is_charlie(self):
        return self._5_card_charlie

    def get_result(self):
        return self.result

    def get_is_finish(self):
        return self.is_finish

    def get_is_end(self):
        result = self.get_result()
        return True if (result != "" and result != "stand") else False

    def get_able_split(self):
        return len(self.cards) == 2 and self.cards[0].get_symbol() == self.cards[1].get_symbol()

    def get_x(self):
        return self.get_cards()[0].get_x()

    def set_able_hit(self, is_hit: bool):
        self.is_able_hit = is_hit

    def set_is_ace_split(self, is_ace_split: bool):
        self.is_ace_split = is_ace_split

    def set_charlie(self, charlie):
        self._5_card_charlie = charlie

    def set_is_finish(self, is_finish: bool):
        self.is_finish = is_finish

    def set_result(self, result):
        self.result = result


class Player:

    def __init__(self, id_=None, name="Unknown", money=100, init_stake=5):
        self.id = id_ if id_ else uuid.uuid1()
        self.name = name
        self.money = money
        self.basic_stake = init_stake
        self.total_stake = init_stake
        self.hands = []
        self.fold = False
        self.double = False
        self.insurance = False
        self.already_pay = False

        # Show
        self.show_insurance = True
        self.show_blackjack = True

    # GET
    def get_x(self):
        first_hand = self.get_hands()[0]
        if not first_hand:
            return
        first_card = first_hand.get_cards()[0]
        if not first_card:
            return
        return first_card.get_x()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_money(self):
        return self.money

    def get_basic_stake(self):
        return self.basic_stake

    def get_total_stake(self):
        return self.total_stake

    def get_hand(self, num):
        if len(self.hands) > num:
            return self.hands[num]

    def get_hands(self):
        return self.hands

    def get_hands_num(self):
        return len(self.hands)

    def get_fold(self):
        return self.fold

    def get_double(self):
        return self.double

    def get_insurance(self):
        return self.insurance

    def get_show_insurance(self):
        return self.show_insurance

    def get_show_blackjack(self):
        return self.show_blackjack

    def get_pay_yet(self):
        return self.already_pay

    def get_able_double(self):
        return len(self.hands) == 1 and len(self.hands[0].get_cards()) == 2 and not self.get_is_finish()

    def get_able_fold(self):
        return len(self.hands) == 1 and len(self.hands[0].get_cards()) == 2 and not self.get_is_finish()

    def get_is_hand_finish(self, hand):
        return hand.get_is_finish()

    def get_is_finish(self):
        return all(map(self.get_is_hand_finish, self.get_hands()))

    # find hand
    def get_hand_by_id(self, id_):
        for hand in self.get_hands():
            if str(hand.get_id()) == id_:
                return hand

    def get_current_hand(self):
        for hand in self.get_hands():
            if not hand.get_is_finish():
                return hand

    def get_current_hand_x(self):
        for hand in self.get_hands():
            if not hand.get_is_finish():
                return hand.get_cards()[0].get_x()

    def get_is_pay(self):

        if self.money > self.basic_stake:
            return True
        else:
            return False

    # SET
    def set_money(self, money: int):
        self.money = money

    def add_money(self, stake: int):
        self.money += stake

    def set_basic_stake(self, stake: int):
        self.basic_stake = stake

    def set_total_stake(self, stake: int):
        self.total_stake = stake

    def set_hands(self, hands):
        self.hands = [hands]

    def add_total_stake(self, stake: int):
        self.total_stake += stake

    def set_fold(self, fold: bool):
        self.fold = fold

    def set_double(self, double: bool):
        self.double = double

    def set_insurance(self, insurance: bool):
        self.insurance = insurance

    def set_show_insurance(self, show_insurance: bool):
        self.show_insurance = show_insurance

    def set_show_blackjack(self, show_blackjack: bool):
        self.show_blackjack = show_blackjack

    def set_pay_yet(self, pay_yet: bool):
        self.already_pay = pay_yet

    def append_empty_hand(self):
        self.hands.append(Hand())

    def pay_stake(self):

        if self.get_is_pay():
            self.add_money(-self.basic_stake)
            return True
        return False

