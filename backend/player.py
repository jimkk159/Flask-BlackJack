from flask import Blueprint

player_blueprint = Blueprint('player', __name__)

class Hand:

    def __init__(self):
        # self.id = id_
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

class Player:

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

    def __init__(self, player_num):
        self.player_num = player_num
        self.in_ = self.create(self.player_num)
        self.out = []

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

    # Get All Players outside table
    def get_players_out(self):
        return self.out

    # SET
    # Set stake
    def set_stake(self):

        for player in self.in_:
            basic_stake = player.get_basic_stake()
            player.set_total_stake(basic_stake)

    # Create Player
    def create(self, player_num):
        in_game = []
        for id_ in range(player_num):
            player = Player(id_=id_)
            in_game.append(player)
        return in_game

    # Reset Player
    def reset_all(self):

        self.enter()
        self.set_stake()
        result = self.pay_stake()
        self.reset_double()
        self.reset_fold()
        self.reset_insurance()
        self.reset_hands()
        return result

    # Enter table
    def enter(self):

        while self.out:
            self.in_.append(self.out.pop())
        self.in_.sort(key=lambda x: x.id)

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

    # People who win or lose
    def eliminate(self):

        out_game = []
        for player in self.in_:
            if not any(map(lambda x: x.result == "", player.get_hands())):
                out_game.append(player.id)

        while out_game:
            out_player_id = out_game.pop()
            pick_id = 0
            for num in range(len(self.in_)):
                if self.in_[num].id == out_player_id:
                    pick_id = num
                    break
            out_game_player = self.in_.pop(pick_id)
            self.out.append(out_game_player)

    # Print Players Cards
    def print_all_cards(self):

        for player in self.in_:
            player.get_print_cards()

    # Print Players Moneys
    def print_all_money(self):

        for player in self.in_:
            player.get_print_money()

    # Print Players Status
    def print_all_status(self, choice="in"):

        array = self.in_ if choice == "in" else self.out
        for player in array:
            player.get_print_status()

    # Print Players Result
    def print_all_result(self):

        for player in self.out:
            player.get_print_result()
