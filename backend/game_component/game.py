import uuid
from math import floor
from backend.game_component.player import Hand, Table
from backend.game_component.card import Deck


class Blackjack:

    def __init__(self, id_=None):

        self.id = id_ if id_ else uuid.uuid1()
        self.game_end = False

        # Setting Rule
        self.is_insurance = True
        self.is_insurance_over_10 = False
        self.is_double = True
        self.blackjack_ratio = 1.5

        # Setting Deck
        self.deck_num = 4
        self.deck = Deck(self.deck_num)
        self.deck.shuffle()
        self.set_blackjack_value(self.deck)

        # Setting Player
        self.players_num = 1
        self.tables = [Table()]

        # Setting Banker
        self.banker = []
        self.min_bet = 5

    # GET
    def get_deck(self):
        return self.deck

    def get_deck_num(self):
        return self.deck_num

    def get_deck_cards(self):
        return self.get_deck().deck

    def get_players_num(self):
        return self.players_num

    def get_min_bet(self):
        return self.min_bet

    def get_is_insurance(self):
        return self.is_insurance

    def get_insurance_over_10(self):
        return self.is_insurance_over_10

    def get_player_can_double(self, player):
        if len(player.get_hands()[0].get_cards()) == 2 and \
                player.get_money() >= player.get_basic_stake() and \
                self.is_double and player.get_hands_num() == 1:
            return True
        return False

    def get_hand_can_split(self, player, hand):
        if len(hand.get_cards()) == 2 and \
                hand.get_cards()[0].get_symbol() == hand.get_cards()[1].get_symbol() \
                and player.get_money() >= player.get_basic_stake():
            return True
        return False

    def get_judge_insurance(self):

        if self.banker[1].get_symbol() == "A" or (
                self.is_insurance_over_10 and self.banker[1].get_symbol() in ["A", "K", "Q", "J", "10"]):
            return True
        return False

    def get_is_double(self):
        return self.is_double

    def get_able_double(self, player):
        return player.get_able_double()

    def get_able_split(self, hand):
        return hand.get_able_split()

    def get_able_fold(self, player):
        return player.get_able_fold()

    def get_blackjack_ratio(self):
        return self.blackjack_ratio

    def get_banker_cards(self):
        return self.banker

    def get_table_cards(self, table):
        for table in self.tables:
            table.get_id()
        return self.tables.get_all_hands()

    def get_table(self):
        return self.tables

    def get_players(self):
        return self.tables.get_players()

    def get_player_option(self, player, hand):
        result = []
        if self.get_player_can_double(player):
            result.append("double")
        if self.get_hand_can_split(player, hand):
            result.append("split")
        result += ["hit", "stand"]
        return result

    def get_player_stake(self, player):
        return player.get_total_stake()

    def get_hand_is_charlie(self, hand):
        return hand.get_is_charlie()

    # Check Bust
    def get_is_hand_bust(self, cards_in_hand):

        if self.get_hand_sum_switch_ace(cards_in_hand) > 21:
            return True
        return False

    def get_player_insurance(self, player):
        return player.get_insurance()

    # Check Sum
    def get_hand_sum(self, cards_in_hand):

        total = 0
        for card_ in cards_in_hand:
            total += card_.get_value()
        return total

    def switch_ace_value(self, cards_in_hand):

        for card_ in cards_in_hand:
            if card_.get_symbol() == "A" and card_.get_value() == 11:
                card_.set_value(1)
                return True
        return False

    def get_hand_sum_switch_ace(self, cards_in_hand):

        while self.get_hand_sum(cards_in_hand) > 21:
            if not self.switch_ace_value(cards_in_hand):
                break

        return self.get_hand_sum(cards_in_hand)

    def get_is_blackjack(self, cards_in_hand):
        if len(cards_in_hand) == 2 and self.get_hand_sum(cards_in_hand) == 21:
            return True
        return False

    def get_is_banker_bust(self):

        if self.get_is_hand_bust(self.banker):
            return True
        return False

    # SET
    def set_deck_num(self, deck_num):
        self.deck_num = deck_num

    def set_player_num(self, player_num):
        self.players_num = player_num

    def set_min_bet(self, min_bet):
        self.min_bet = min_bet

    def set_is_insurance(self, is_insurance):
        self.is_insurance = is_insurance

    def set_insurance_over_10(self, is_insurance_over_10):
        self.is_insurance_over_10 = is_insurance_over_10

    def set_is_double(self, is_double):
        self.is_double = is_double

    def set_blackjack_ratio(self, blackjack_ratio):
        self.blackjack_ratio = blackjack_ratio

    def set_player_insurance(self, player, insurance: bool):

        player.set_insurance(insurance)

    # Set Hand Stand
    def set_hand_stand(self, hand):
        hand.set_result("stand")

    def stand_process(self, hand):
        hand.set_able_hit(False)
        hand.set_is_finish(True)
        self.set_hand_stand(hand)

    # Set Player Fold
    def set_hand_fold(self, hand):
        hand.set_result("fold")

    def fold_process(self, player):
        if player.get_able_fold():
            player.set_fold(True)
            hand = player.get_hands()[0]
            hand.set_is_finish(True)
            self.set_hand_fold(hand)
            return True
        return False

    # Set card value
    def set_blackjack_value(self, deck):
        poker_value_dict = {"K": 10, "Q": 10, "J": 10, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5,
                            "4": 4, "3": 3, "2": 2, "A": 11}

        for card in deck.get_deck():
            symbol = card.get_symbol()
            card.set_value(poker_value_dict[symbol])

    def player_has_insurance(self, player):

        player.set_insurance(True)

    def reset_player_insurance(self, player):

        player.set_insurance(False)

    def check_blackjack(self):

        return all(map(self.check_player_blackjack, self.get_players()))

    def check_player_blackjack(self, player):

        hand = player.get_hands()[0]
        banker_blackjack = self.get_is_banker_blackjack()
        player_blackjack = self.get_is_player_blackjack(player)
        if banker_blackjack and player_blackjack:
            hand.set_result("push")
            return True

        if banker_blackjack:
            hand.set_result("lose")
            return True

        if player_blackjack:
            hand.set_result("blackjack")
            return True
        return False

    def get_is_banker_blackjack(self):
        if self.get_is_blackjack(self.banker):
            return True
        return False

    def get_is_player_blackjack(self, player):
        hand = player.get_hands()[0]
        if self.get_is_blackjack(hand.get_cards()):
            return True
        return False

    # Check Player End
    def get_is_hand_end(self, hand):

        if hand:
            return True if (hand.get_result() != "" and hand.get_result() != "stand") else False
        return False

    def get_is_player_end(self, player):

        hands = player.get_hands()
        if hands:
            return all([(True if hand.get_result() != "" else False) for hand in hands])
        return False

    def get_is_player_finish(self, player):

        hands = player.get_hands()
        if hands:
            return all([(True if (hand.get_result() != "" or hand.get_is_finish()) else False) for hand in hands])
        return False

    def get_is_players_finish(self):

        players = self.get_players()
        if players:
            return all(map(self.get_is_player_finish, players))
        return False

    def get_cards_enough(self):

        if len(self.get_deck_cards()) <= self.deck_num * 52 / 2:
            return True
        return False

    def get_player_by_id(self, id_):
        for player in self.get_players():
            if str(player.get_id()) == id_:
                return player

    def get_hand_by_id(self, id_):
        for player in self.get_players():
            for hand in player.get_hands():
                if str(hand.get_id()) == id_:
                    return hand

    def get_player_by_hand_id(self, id_):
        for player in self.get_players():
            for hand in player.get_hands():
                if str(hand.get_id()) == id_:
                    return player

    # Game Setting
    def reset(self):

        if self.get_cards_enough():
            self.deck.reset_deck()

        # Reset Player
        self.tables.reset_players()

        # Reset Banker Cards
        self.banker = []

    def pay_all_stake(self):
        result = []
        for player in self.get_players():
            result.append(self.pay_player_stake(player))
        return result

    def pay_player_stake(self, player):
        return player.pay_stake()

    def set_players(self):
        self.tables.create(self.players_num)

    def set_players_by_ids(self, ids: list[int]):
        self.tables.create_by_id(ids)

    def enter_table(self, id_=None, name="Unknown", money=0):
        if not self.tables.get_is_player_id(id_):
            self.tables.append_by_id(id_=id_, name=name, money=money)

    # Deal Card
    def deal(self, cards_in_hand: list, faced=True):
        card_ = self.get_deck_cards().pop()
        card_.faced = faced
        cards_in_hand.append(card_)

    def deal_to_all(self):

        # To each player
        for player in self.tables.get_players():
            self.deal(player.get_hands()[0].get_cards())

        # To banker
        self.deal(self.banker)

    def deal_initial(self):

        self.deal_to_all()
        self.hole_banker_card()
        self.deal_to_all()

    # Ask Insurance
    def ask_insurance(self, choice):

        # ToDo only for player 1
        # for num in range(self.player_num):
        self.ask_player_insurance(self.tables.get_players()[0], choice)

    def ask_player_insurance(self, player, choice):

        player.set_insurance(False)
        if choice and player.get_money() >= floor(player.get_basic_stake() / 2):
            player.add_money(-floor(player.get_basic_stake() / 2))
            player.set_insurance(True)

    # Double Down
    def double_down(self, player):

        player.set_double(True)
        player.add_money(-player.get_basic_stake())
        player.set_total_stake(2 * player.get_basic_stake())
        self.deal(player.get_hands()[0].get_cards())

    def double_down_process(self, player):
        self.double_down(player)
        hand = player.get_hands()[0]
        hand.set_able_hit(False)
        hand.set_is_finish(True)
        if self.get_is_hand_bust(hand.get_cards()):
            hand.set_result("bust")
            return True
        return False

    # Hit
    def hit(self, hand):
        self.deal(hand.get_cards())
        if len(hand.cards) >= 5:
            hand.set_charlie(True)

    def hit_process(self, hand):
        if hand.get_able_hit() and not hand.get_is_finish():
            self.hit(hand)
        if hand.get_is_ace_split():
            hand.set_able_hit(False)
            if not hand.get_able_split():
                hand.set_is_finish(True)
        if self.get_is_hand_bust(hand.get_cards()):
            hand.set_able_hit(False)
            hand.set_is_finish(True)
            hand.set_result("bust")

    # Split
    def split(self, hands, hand):

        is_ace_pair = hand.get_is_ace_pair()
        # Separate the card
        split_card = hand.get_cards().pop()
        hand.set_able_hit(True)

        # Create New Hand
        split_hand = Hand()
        split_hand.get_cards().append(split_card)
        if is_ace_pair:
            hand.set_is_ace_split(True)
            split_hand.set_is_ace_split(True)

        # Assign the hand to player
        hands.append(split_hand)

    def split_process(self, player, hand):

        player.add_money(-player.get_basic_stake())
        player.add_total_stake(player.get_basic_stake())
        self.split(player.get_hands(), hand)

    # It's banker time
    def reveal_banker_card(self):
        self.banker[0].set_faced(True)

    def hole_banker_card(self):
        self.banker[0].set_faced(False)

    def deal_to_banker(self):

        while self.get_hand_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)

    def banker_bust_process(self):

        for player in self.tables.get_players():
            for hand in player.get_hands():
                hand_result = hand.get_result()
                if hand_result == "" or hand_result == "stand":
                    hand.set_result("win")

    # Compare the card score in hand
    def compare_cards(self):

        banker_point = self.get_hand_sum_switch_ace(self.banker)
        for player in self.tables.get_players():
            for hand in player.get_hands():
                hand_result = hand.get_result()
                if hand_result == "" or hand_result == "stand":

                    if hand.get_is_charlie():
                        hand.set_result("win")
                    else:
                        player_point = self.get_hand_sum_switch_ace(hand.get_cards())
                        if player_point > banker_point:
                            hand.set_result("win")
                        elif player_point < banker_point:
                            hand.set_result("lose")
                        else:
                            hand.set_result("push")

    # Exchange the money
    def give_hand_money(self, hand, player):

        if hand.get_result() == "win":

            if hand.get_is_charlie() or player.get_double():

                player.add_money(4 * player.get_basic_stake())

            else:

                player.add_money(2 * player.get_basic_stake())

        if hand.get_result() == "blackjack":

            if player.get_double():
                player.add_money(2 * (1 + self.blackjack_ratio) * player.get_basic_stake())

            elif hand.get_is_charlie():
                player.money.add_money(floor((1 + 3 * self.blackjack_ratio) * player.get_basic_stake()))

            else:
                player.add_money(floor((1 + self.blackjack_ratio) * player.get_basic_stake()))

        if hand.get_result() == "push":
            if player.get_double():
                player.add_money(2 * player.get_basic_stake())
            else:
                player.add_money(player.get_basic_stake())

    def give_money(self, player):

        for hand in player.get_hands():
            self.give_hand_money(hand, player)

        if player.get_fold():
            player.add_money(floor(player.get_basic_stake() / 2))

        if self.get_is_banker_blackjack() and self.get_player_insurance(player):
            player.add_money(2 * floor(player.get_basic_stake() / 2))
