import uuid
from math import floor
from app.game_component.player import Player, Hand
from app.game_component.card import Deck


class Table:

    def __init__(self, id_=None, table_name=None, deck_num=None, max_player=None, min_bet=None, bj_ratio=None,
                 is_insurance=True, is_insurance_over_10=False, is_double=True):
        self.id = id_ if id_ else uuid.uuid1()
        self.name = table_name

        self.player_num = 0
        self.in_ = []

        # Table Status
        self.game_start = False
        self.owner = None

        # Table Rule
        self.deck_num = deck_num if deck_num else 4
        self.max_player = max_player if max_player else 4
        self.min_bet = min_bet if min_bet else 5
        self.bj_ratio = bj_ratio if bj_ratio else 1.5
        self.is_insurance = is_insurance
        self.is_insurance_over_10 = is_insurance_over_10
        self.is_double = is_double

        # Setting Deck
        self.deck = Deck(self.deck_num)
        self.deck.shuffle()
        self.set_blackjack_value()

        # Setting Banker
        self.banker = []


    # GET
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_player_num(self):
        return self.player_num

    def get_players(self):
        return self.in_

    def get_game_start(self):
        return self.game_start

    def get_deck_num(self):
        return self.deck_num

    def get_max_player(self):
        return self.max_player


    def get_min_bet(self):
        return self.min_bet

    def get_blackjack_ratio(self):
        return self.bj_ratio

    def get_is_insurance(self):
        return self.is_insurance

    def get_is_insurance_over_10(self):
        return self.is_insurance_over_10

    def get_is_double(self):
        return self.is_double

    def get_deck(self):
        return self.deck.get_deck()

    def get_banker_cards(self):
        return self.banker

    # Check Table Full
    def get_is_full(self):
        if len(self.get_players()) >= self.max_player:
            return True
        return False

    # Check Owner
    def get_is_owner(self, player):
        if str(self.get_players()[0].get_id()) == player.get_id():
            return True
        return False

    def get_is_owner_by_id(self, id_):
        if str(self.in_[0].id) == id_:
            return True
        return False

    # Check Card Enough
    def get_cards_enough(self):

        if len(self.get_deck()) <= self.deck_num * 52 / 2:
            return True
        return False

    # Player
    def get_player_by_id(self, id_):
        for player in self.in_:
            if str(player.id) == id_:
                return player

    def get_player_by_hand_id(self, id_):
        for player in self.in_:
            for hand in player.get_hands():
                if str(hand.get_id()) == id_:
                    return player

    def get_is_player_id(self, id_):
        for player in self.in_:
            if player.id == id_:
                return True
        return False

    def get_player_option(self, player, hand):
        result = []
        if self.get_player_can_double(player):
            result.append("double")
        if self.get_hand_can_split(player, hand):
            result.append("split")
        result += ["hit", "stand"]
        return result

    # Hand
    def get_hand_by_id(self, id_):
        for player in self.in_:
            for hand in player.get_hands():
                if str(hand.get_id()) == id_:
                    return hand

    # SET
    def set_game_start(self, game_start):
        self.game_start = game_start

    def set_owner(self):

        self.owner = self.in_[0]

    def set_deck_num(self, number):
        self.deck_num = number

    def set_max_player(self, number):
        self.max_player = number

    def set_min_bet(self, min_bet):
        self.min_bet = min_bet

    def set_is_insurance(self, is_insurance):
        self.is_insurance = is_insurance

    def set_is_insurance_over_10(self, is_insurance_over_10):
        self.is_insurance_over_10 = is_insurance_over_10

    def set_is_double(self, is_double):
        self.is_double = is_double

    def set_blackjack_ratio(self, blackjack_ratio):
        self.bj_ratio = blackjack_ratio

    def set_blackjack_value(self):
        poker_value_dict = {"K": 10, "Q": 10, "J": 10, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5,
                            "4": 4, "3": 3, "2": 2, "A": 11}

        for card in self.get_deck():
            symbol = card.get_symbol()
            card.set_value(poker_value_dict[symbol])

    # Deal Card
    def deal(self, cards_in_hand: list, faced=True):
        card_ = self.get_deck().pop()
        card_.faced = faced
        cards_in_hand.append(card_)

    def deal_to_all(self):

        # To each player
        for player in self.get_players():
            self.deal(player.get_hands()[0].get_cards())

        # To banker
        self.deal(self.banker)

    def deal_initial(self):

        self.deal_to_all()
        self.hole_banker_card()
        self.deal_to_all()

    def deal_to_banker(self):
        while self.get_hand_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)

    # Banker
    def reveal_banker_card(self):
        self.banker[0].set_faced(True)

    def hole_banker_card(self):
        self.banker[0].set_faced(False)

    def banker_bust_process(self):

        for player in self.get_players():
            for hand in player.get_hands():
                hand_result = hand.get_result()
                if hand_result == "" or hand_result == "stand":
                    hand.set_result("win")

    def compare_cards(self):

        banker_point = self.get_hand_sum_switch_ace(self.banker)
        for player in self.get_players():
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

    # Stake
    def set_stake(self):
        for player in self.in_:
            basic_stake = player.get_basic_stake()
            player.set_total_stake(basic_stake)

    def all_pay_stake(self):
        result = []
        for player in self.get_players():
            result.append(self.player_pay_stake(player))
        return result

    def player_pay_stake(self, player):
        return player.pay_stake()

    # Exchange the money
    def give_hand_money(self, hand, player):

        if hand.get_result() == "win":

            if hand.get_is_charlie() or player.get_double():

                player.add_money(4 * player.get_basic_stake())

            else:

                player.add_money(2 * player.get_basic_stake())

        if hand.get_result() == "blackjack":

            if player.get_double():
                player.add_money(2 * (1 + self.bj_ratio) * player.get_basic_stake())

            elif hand.get_is_charlie():
                player.money.add_money(floor((1 + 3 * self.bj_ratio) * player.get_basic_stake()))

            else:
                player.add_money(floor((1 + self.bj_ratio) * player.get_basic_stake()))

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

        if self.get_is_banker_blackjack() and player.get_insurance:
            player.add_money(2 * floor(player.get_basic_stake() / 2))

    # Append Player
    def append_by_id(self, id_=None, player_name="Unknown", money=0):
        player = Player(id_=id_, name=player_name, money=money)
        self.in_.append(player)
        self.player_num = len(self.in_)

    # Reset
    def reset(self):

        if self.get_cards_enough():
            self.deck.reset_deck()

        # Reset Player
        self.reset_players()

        # Reset Banker Cards
        self.banker = []

    def reset_players(self):

        self.set_stake()
        self.reset_double()
        self.reset_fold()
        self.reset_insurance()
        self.reset_hands()
        self.reset_show_insurance()
        self.reset_show_blackjack()

    def refresh(self):
        self.in_ = []
        self.player_num = 0

    def reset_hands(self):

        # Reset Player
        for player in self.in_:
            player.set_hands(Hand())

    def reset_double(self):

        for player in self.in_:
            player.set_double(False)

    def reset_fold(self):

        for player in self.in_:
            player.set_fold(False)

    def reset_insurance(self):

        for player in self.in_:
            player.set_insurance(False)

    def reset_show_insurance(self):

        for player in self.in_:
            player.set_show_insurance(False)

    def reset_show_blackjack(self):

        for player in self.in_:
            player.set_show_blackjack(False)

    # Insurance
    def get_judge_insurance(self):

        if self.banker[1].get_symbol() == "A" or (
                self.is_insurance_over_10 and self.banker[1].get_symbol() in ["A", "K", "Q", "J", "10"]):
            return True
        return False

    def set_player_insurance(self, player, insurance: bool):

        player.set_insurance(insurance)

    def player_has_insurance(self, player):

        player.set_insurance(True)

    def reset_player_insurance(self, player):

        player.set_insurance(False)

    def ask_player_insurance(self, player, choice):

        player.set_insurance(False)
        if choice and player.get_money() >= floor(player.get_basic_stake() / 2):
            player.add_money(-floor(player.get_basic_stake() / 2))
            player.set_insurance(True)

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

    # Double Down
    def get_able_double(self, player):
        return player.get_able_double()

    def get_player_can_double(self, player):
        if len(player.get_hands()[0].get_cards()) == 2 and \
                player.get_money() >= player.get_basic_stake() and \
                self.is_double and player.get_hands_num() == 1:
            return True
        return False

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

    # Split
    def get_able_split(self, hand):
        return hand.get_able_split()

    def get_hand_can_split(self, player, hand):
        if len(hand.get_cards()) == 2 and \
                hand.get_cards()[0].get_symbol() == hand.get_cards()[1].get_symbol() \
                and player.get_money() >= player.get_basic_stake():
            return True
        return False

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

    # Stand
    def set_hand_stand(self, hand):
        hand.set_result("stand")

    def stand_process(self, hand):
        hand.set_able_hit(False)
        hand.set_is_finish(True)
        self.set_hand_stand(hand)

    # Surrender
    def get_able_fold(self, player):
        return player.get_able_fold()

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

    # Wager
    def get_player_stake(self, player):
        return player.get_total_stake()

    # 5 Card charlie
    def get_hand_is_charlie(self, hand):
        return hand.get_is_charlie()

    # Bust
    def get_is_hand_bust(self, cards_in_hand):

        if self.get_hand_sum_switch_ace(cards_in_hand) > 21:
            return True
        return False

    # Blackjack
    def get_is_blackjack(self, cards_in_hand):
        if len(cards_in_hand) == 2 and self.get_hand_sum(cards_in_hand) == 21:
            return True
        return False

    def get_is_banker_bust(self):

        if self.get_is_hand_bust(self.banker):
            return True
        return False

    def set_hand_blackjack(self, hand):
        hand.set_result("blackjack")

    def blackjack_process(self, player):

        if self.get_is_player_blackjack(player):
            self.check_player_blackjack(player)
            return True
        return False

    def check_blackjack(self):

        return all(map(self.check_player_blackjack, self.get_players()))

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

    # Push
    def set_hand_push(self, hand):
        hand.set_result("push")

    # Lose
    def set_hand_lose(self, hand):
        hand.set_result("lose")

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

    # Check End
    def get_is_hand_end(self, hand):

        if hand:
            return True if (hand.get_result() != "" and hand.get_result() != "stand") else False
        return False

    def get_is_player_end(self, player):

        hands = player.get_hands()
        if hands:
            return all([(True if hand.get_result() != "" else False) for hand in hands])
        return False

    # Check Finish
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





