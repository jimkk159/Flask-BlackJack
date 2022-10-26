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

        # Setting Banker
        self.banker = []

        # Setting Table
        self.max_table = 6
        self.tables = []

    # GET
    def get_deck(self):
        return self.deck

    def get_deck_cards(self):
        return self.get_deck().deck

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

    def get_banker_cards(self):
        return self.banker

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
    def set_table_deck_num(self, table=None, deck_num=4):

        if not table:
            return
        table.set_deck_num(deck_num)

    def set_table_name_deck_num(self, table_name=None, deck_num=4):

        if table_name:
            return
        table = self.get_table_by_name(table_name)
        if table:
            return
        table.set_deck_num(deck_num)

    def set_table_max(self, table=None, max_player_num=4):

        if not table:
            return
        table.set_max_player(max_player_num)

    def set_table_name_max(self, table_name=None, max_player_num=4):

        if not table_name:
            return
        table = self.get_table_by_name(table_name)
        if not table:
            return
        table.set_max_player(max_player_num)

    def set_table_min_bet(self, table=None, min_bet=5):

        if not table:
            return
        table.set_min_bet(min_bet)

    def set_table_name_min_bet(self, table_name=None, min_bet=5):

        if not table_name:
            return
        table = self.get_table_by_name(table_name)
        if not table:
            return
        table.set_min_bet(min_bet)

    def set_table_blackjack_ratio(self, table=None, bj_ratio=1.5):

        if not table:
            return
        table.set_blackjack_ratio(bj_ratio)

    def set_table_name_blackjack_ratio(self, table_name=None, bj_ratio=1.5):

        if not table_name:
            return
        table = self.get_table_by_name(table_name)
        if not table:
            return
        table.set_blackjack_ratio(bj_ratio)

    def set_table_is_insurance(self, table=None, is_insurance=True):

        if not table:
            return
        table.set_is_insurance(is_insurance)

    def set_table_name_is_insurance(self, table_name=None, is_insurance=True):

        if not table_name:
            return
        table = self.get_table_by_name(table_name)
        if not table:
            return
        table.set_is_insurance(is_insurance)

    def set_table_insurance_over_10(self, table=None, is_insurance_over_10=False):

        if not table:
            return
        table.set_is_insurance_over_10(is_insurance_over_10)

    def set_table_name_insurance_over_10(self, table_name=None, is_insurance_over_10=False):

        if not table_name:
            return
        table = self.get_table_by_name(table_name)
        if not table:
            return
        table.set_is_insurance_over_10(is_insurance_over_10)

    def set_table_is_double(self, table=None, is_double=True):

        if not table:
            return
        table.set_is_double(is_double)

    def set_table_name_is_double(self, table_name=None, is_double=True):

        if not table_name:
            return
        table = self.get_table_by_name(table_name)
        if not table:
            return
        table.set_is_double(is_double)

    #
    def set_is_insurance(self, is_insurance):
        self.is_insurance = is_insurance

    def set_insurance_over_10(self, is_insurance_over_10):
        self.is_insurance_over_10 = is_insurance_over_10

    def set_is_double(self, is_double):
        self.is_double = is_double

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

    # Set Hand Blackjack
    def set_hand_blackjack(self, hand):
        hand.set_result("blackjack")

    def blackjack_process(self, player):

        if self.get_is_player_blackjack(player):
            self.check_player_blackjack(player)
            return True
        return False

    # Set Hand Push
    def set_hand_push(self, hand):
        hand.set_result("push")

    # Set Hand Lose
    def set_hand_lose(self, hand):
        hand.set_result("lose")

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

    def check_blackjack(self, table_name):

        return all(map(self.check_player_blackjack, self.get_table_name_players(table_name)))

    def check_player_blackjack(self, player):

        hand = player.get_hands()[0]
        banker_blackjack = self.get_is_banker_blackjack()
        player_blackjack = self.get_is_player_blackjack(player)
        if banker_blackjack and player_blackjack:
            hand.set_result("push")
            hand.set_able_hit(False)
            hand.set_is_finish(True)
            self.set_hand_push(hand)
            return True

        if banker_blackjack:
            hand.set_result("lose")
            hand.set_able_hit(False)
            hand.set_is_finish(True)
            self.set_hand_lose(hand)
            return True

        if player_blackjack:
            hand.set_result("blackjack")
            hand.set_able_hit(False)
            hand.set_is_finish(True)
            self.set_hand_blackjack(hand)
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

    def get_is_players_finish(self, table_name):

        players = self.get_table_name_players(table_name)
        if players:
            return all(map(self.get_is_player_finish, players))
        return False

    def get_cards_enough(self):

        if len(self.get_deck_cards()) <= self.deck_num * 52 / 2:
            return True
        return False

    def get_player_by_id(self, id_):
        for table in self.tables:
            for player in table.get_players():
                if str(player.get_id()) == id_:
                    return player

    def get_hand_by_id(self, id_):
        for table in self.tables:
            for player in table.get_players():
                for hand in player.get_hands():
                    if str(hand.get_id()) == id_:
                        return hand

    def get_player_by_hand_id(self, id_):
        for table in self.tables:
            for player in table.get_players():
                for hand in player.get_hands():
                    if str(hand.get_id()) == id_:
                        return player

    # Game Setting
    def reset(self, table):

        if self.get_cards_enough():
            self.deck.reset_deck()

        # Reset Player
        table.reset_players()

        # Reset Banker Cards
        self.banker = []

    def pay_all_stake(self, table_name):
        result = []
        for player in self.get_table_name_players(table_name):
            result.append(self.pay_player_stake(player))
        return result

    def pay_player_stake(self, player):
        return player.pay_stake()

    def set_players_by_ids(self, table, ids: list[int]):
        table.create_by_id(ids)

    # Table Maintain
    def create_table(self, table_name=None):

        if not table_name:
            return

        if table_name == "":
            return

        if len(self.tables) == self.max_table:
            return

        if self.get_table_by_name(table_name):
            return

        self.tables.append(Table(name=table_name))

    def enter_table(self, table_name=None, player_id=None, player_name="Unknown", money=0):

        if not table_name:
            return

        if table_name == "":
            return

        table = self.get_table_by_name(table_name)
        if not table:
            return
        if table.get_is_player_id(player_id):
            return

        table.append_by_id(id_=player_id, player_name=player_name, money=money)

    def delete_table(self, table_name=None):

        if not table_name:
            return

        if table_name == "":
            return

        if not self.get_table_by_name(table_name):
            return

        table_num = None
        for num in range(len(self.tables)):
            # Find Table
            if self.tables[num].get_name() == table_name:
                table_num = num
                break

        # Table delete
        if table_num is not None:
            self.tables.pop(table_num)

    def leave_table(self, player, table):

        player_num = None
        players = table.get_players()
        for num in range(len(players)):
            # Find Player
            if str(players[num].get_id()) == str(player.get_id()):
                player_num = num
                break

        # Player leave table
        if player_num is not None:
            table.get_players().pop(player_num)

    def get_table_by_id(self, table_id):
        for table in self.tables:
            if str(table.get_id()) == table_id:
                return table

    def get_table_cards(self, table):
        return table.get_all_hands()

    def get_cards_by_table_id(self, table_id):
        for table in self.tables:
            if str(table.get_id()) == table_id:
                return table.get_all_hands()

    def get_tables(self):
        return self.tables

    def get_table_by_name(self, table_name):
        for table in self.tables:
            if table.get_name() == str(table_name):
                return table

    def get_table_name_players(self, table_name):
        return self.get_table_by_name(table_name).get_players()

    def get_table_players_num(self, table):
        return table.get_player_num()

    def get_table_name_players_num(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_player_num()

    def get_table_players(self, table):
        return table.get_players()

    def get_table_player_by_id(self, table, id_):
        for player in table.get_players():
            if str(player.get_id()) == id_:
                return player

    def get_is_table_name_empty(self, table_name):
        table = self.get_table_by_name(table_name)
        if not table:
            return True
        if self.get_is_table_empty(table) == 0:
            return True
        return False

    def get_is_table_empty(self, table):
        if len(table.get_players()) == 0:
            return True
        return False

    def get_table_has_player(self, table, input_player):
        for player in table.get_players():
            if str(input_player.get_id()) == str(player.get_id()):
                return True
        return False

    def get_player_table(self, input_player):
        for table in self.get_tables():
            for player in table.get_players():
                if str(input_player.get_id()) == str(player.get_id()):
                    return table

    def get_table_deck_num(self, table):
        return table.get_deck_num()

    def get_table_name_deck_num(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_deck_num()

    def get_table_max(self, table):
        return table.get_max_player()

    def get_table_name_max(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_max_player()

    def get_table_min_bet(self, table):
        return table.get_min_bet()

    def get_table_name_min_bet(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_min_bet()

    def get_table_blackjack_ratio(self, table):
        return table.get_blackjack_ratio()

    def get_table_name_blackjack_ratio(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_blackjack_ratio()

    def get_table_is_insurance(self, table):
        return table.get_is_insurance()

    def get_table_name_is_insurance(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_is_insurance()

    def get_table_insurance_over_10(self, table):
        return table.get_is_insurance_over_10()

    def get_table_name_is_insurance_over_10(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_is_insurance_over_10()

    def get_table_is_double(self, table):
        return table.get_is_double()

    def get_table_name_is_double(self, table_name):
        table = self.get_table_by_name(table_name)
        return table.get_is_double()

    # Deal Card
    def deal(self, cards_in_hand: list, faced=True):
        card_ = self.get_deck_cards().pop()
        card_.faced = faced
        cards_in_hand.append(card_)

    def deal_to_all(self, table):

        # To each player
        for player in table.get_players():
            self.deal(player.get_hands()[0].get_cards())

        # To banker
        self.deal(self.banker)

    def deal_initial(self, table):

        self.deal_to_all(table)
        self.hole_banker_card()
        self.deal_to_all(table)

    # Ask Insurance
    def ask_insurance(self, table, choice):

        # ToDo only for player 1
        # for num in range(self.player_num):
        self.ask_player_insurance(table.get_players()[0], choice)

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

    def banker_bust_process(self, table_name=None):

        if not table_name:
            return
        if table_name == "":
            return
        table = self.get_table_by_name(str(table_name))
        if not table:
            return

        for player in table.get_players():
            for hand in player.get_hands():
                hand_result = hand.get_result()
                if hand_result == "" or hand_result == "stand":
                    hand.set_result("win")

    # Compare the card score in hand
    def compare_cards(self, table_name=None):

        if not table_name:
            return
        if table_name == "":
            return
        table = self.get_table_by_name(str(table_name))
        if not table:
            return

        banker_point = self.get_hand_sum_switch_ace(self.banker)
        for player in table.get_players():
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
