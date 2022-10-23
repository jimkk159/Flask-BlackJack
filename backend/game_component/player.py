import uuid
from flask import Blueprint
from flask_login import UserMixin

player_blueprint = Blueprint('player', __name__)


class Hand:

    def __init__(self):
        self.id = uuid.uuid1()
        self.cards = []
        self.is_hit = True
        self.is_ace_split = False
        self.is_finish = False
        self._5_card_charlie = False
        self.result = ""

    def get_cards(self):
        return self.cards

    def get_cards_num(self):
        return len(self.cards)

    def get_is_hit(self):
        return self.is_hit

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

    def set_is_hit(self, is_hit: bool):
        self.is_hit = is_hit

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

    # GET
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

    def get_able_double(self):
        return len(self.hands) == 1 and len(self.hands[0].get_cards()) == 2

    def get_able_fold(self):
        return len(self.hands) == 1 and len(self.hands[0].get_cards()) == 2

    # find hand
    def get_hand_by_id(self, id_):
        for hand in self.get_hands():
            if str(hand.id) == id_:
                return hand

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

    def add_total_stake(self, stake: int):
        self.total_stake += stake

    def set_fold(self, fold: bool):
        self.fold = fold

    def set_double(self, double: bool):
        self.double = double

    def set_insurance(self, insurance: bool):
        self.insurance = insurance

    def append_empty_hand(self):
        self.hands.append(Hand())

    def pay_stake(self):

        if self.get_is_pay():
            self.add_money(-self.basic_stake)
            return True
        return False


class Table:

    def __init__(self):
        self.id = uuid.uuid1()
        self.player_num = 0
        self.in_ = []

    # GET
    # Get All Players Hands
    def get_all_hands(self):

        all_hands = []
        for player in self.in_:
            all_hands.append(player.get_hands())
        return all_hands

    # Get All Players inside table
    def get_players(self):
        return self.in_

    def get_is_player_id(self, id_):
        for player in self.in_:
            if player.id == id_:
                return True
        return False

    def get_player_by_id(self, id_):
        for player in self.in_:
            if player.id == id_:
                return player

    # SET
    # Set stake
    def set_stake(self):
        for player in self.in_:
            basic_stake = player.get_basic_stake()
            player.set_total_stake(basic_stake)

    # Refresh
    def refresh(self):
        self.in_ = []
        self.player_num = 0

    # Append
    def append_by_id(self, id_=None, name="Unknown", money=0):
        player = Player(id_=id_, name=name, money=money)
        self.in_.append(player)
        self.player_num = len(self.in_)

    # Create Players
    def create(self, player_num):
        self.in_ = []
        self.player_num = player_num
        for _ in range(player_num):
            player = Player()
            self.in_.append(player)

    def create_by_id(self, ids: list):
        self.in_ = []
        self.player_num = len(ids)
        for id_ in ids:
            player = Player(id_)
            self.in_.append(player)

    # Reset All Player
    def reset_players(self):

        self.set_stake()
        self.reset_double()
        self.reset_fold()
        self.reset_insurance()
        self.reset_hands()

    # Pay Stake
    def pay_stake(self):

        result = self.is_pay_stake()
        for num in range(len(result)):
            if result[num]:
                player = self.in_[num]
                basic_stake = player.get_basic_stake()
                self.in_[num].add_money(-basic_stake)
        return result  # Have paid

    # Able to Pay Stake
    def is_pay_stake(self):

        result = []
        for player in self.in_:
            if player.money > player.basic_stake:
                result.append(True)
            else:
                result.append(False)
        return result

    # Reset Double
    def reset_double(self):

        for player in self.in_:
            player.double = False

    # Reset Fold
    def reset_fold(self):

        for player in self.in_:
            player.fold = False

    # Reset Insurance
    def reset_insurance(self):

        for player in self.in_:
            player.insurance = False

    # Reset Cards in hand
    def reset_hands(self):

        # Reset Player
        for player in self.in_:
            player.hands = [Hand()]
