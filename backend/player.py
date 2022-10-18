from flask import Blueprint
from flask_login import UserMixin

player_blueprint = Blueprint('player', __name__)


class Hand:

    def __init__(self, id_):
        self.id = id_
        self.cards = []
        self.is_ace_split = False
        self._5_card_charlie = False
        self.result = ""

    def get_cards(self):
        return self.cards

    def get_is_ace_split(self):
        return self.is_ace_split

    def get_is_charlie(self):
        return self._5_card_charlie

    def get_result(self):
        return self.result

    def set_is_ace_split(self, is_ace_split: bool):
        self.is_ace_split = is_ace_split

    def set_result(self, result):
        self.result = result

    def set_charlie(self, charlie):
        self._5_card_charlie = charlie


class Player():

    def __init__(self, id_, money=100, init_stake=5):
        self.id = id_
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

    def get_money(self):
        return self.money

    def get_basic_stake(self):
        return self.basic_stake

    def get_total_stake(self):
        return self.total_stake

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

    def get_print_cards(self):
        print(f"Player {self.id}:")
        for hand in self.hands:
            for card in hand.cards:
                print(f"{card.get_symbol()} {card.get_suit()} ", end="")
            print(" | ", end="")
        print()

    def get_print_money(self):
        print(f"Player {self.id} has {self.money}")

    def get_print_result(self):
        print(f"Player {self.id} result is", end="")
        for hand in self.hands:
            print(f" {hand.get_result()}", end="")
        print()

    def get_print_status(self):
        print(f"Player {self.id} has:")
        print(f"money: {self.money} ")
        print(f"stake: {self.basic_stake} ")
        print(f"cards: ", end="")
        for hand in self.hands:
            for card in hand.cards:
                print(f"{card.get_symbol()} {card.get_suit()} ", end="")
            print(" | ", end="")
        print()

    # GET
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


class Players:

    def __init__(self):
        self.player_num = None
        self.in_ = None

    # GET
    # Get All Players Hands
    def get_all_hands(self):

        all_hands = []
        for player in self.in_:
            all_hands.append(player.get_hands())
        return all_hands

    # Get All Players inside table
    def get_players_in(self):
        return self.in_

    # SET
    # Set stake
    def set_stake(self):
        for player in self.in_:
            basic_stake = player.get_basic_stake()
            player.set_total_stake(basic_stake)

    # Create Players
    def create(self, player_num):
        self.in_ = []
        self.player_num = player_num
        for id_ in range(player_num):
            player = Player(id_=id_)
            self.in_.append(player)

    def create_by_id(self, ids: list):
        self.in_ = []
        self.player_num = len(ids)
        for id_ in ids:
            player = Player(id_=id_)
            self.in_.append(player)

    # Reset All Player
    def reset_all(self):

        self.set_stake()
        result = self.pay_stake()
        self.reset_double()
        self.reset_fold()
        self.reset_insurance()
        self.reset_hands()
        return result

    # Reset Player
    def reset_player(self, player):

        self.set_stake()
        self.reset_double()
        self.reset_fold()
        self.reset_insurance()
        self.reset_hands()
        return self.pay_player_stake(player)

    # Pay Stake
    def pay_stake(self):

        result = self.is_pay_stake()
        for num in range(len(result)):
            if result[num]:
                player = self.in_[num]
                basic_stake = player.get_basic_stake()
                self.in_[num].add_money(-basic_stake)
        return result  # Have paid

    def pay_player_stake(self, player):

        result = self.is_player_pay_stake(player)
        if result:
            basic_stake = player.get_basic_stake()
            player.add_money(-basic_stake)
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

    def is_player_pay_stake(self, player):

        if player.money > player.basic_stake:
            return True
        else:
            return False

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
            player.hands = [Hand(0)]
