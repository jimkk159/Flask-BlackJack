from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

TABLE_WIDTH = 81
CARD_WIDTH = 5

INIT_CARD_X_SPACE = 2.0
INIT_CARD_Y_SPACE = 15.0
INIT_HAND_X_SPACE = 12.0
INIT_HAND_Y_SPACE = 0.0
INIT_PLAYER_X_SPACE = 30.0
INIT_PLAYER_Y_SPACE = 0.0

# Check Blackjack
def check_blackjack(table_, player):
    if table_.get_is_banker_blackjack():
        table_.reveal_banker_card()

    if table_.check_player_blackjack(player):
        return True
    return False

# Set Card Location
def set_cards_location(table_):
    set_banker_location(table_.get_banker_cards())

    if table_.get_player_num() == 1:
        set_table_players_location(init_x=TABLE_WIDTH / 2 - CARD_WIDTH / 2,
                                   table_=table_)

    elif table_.get_player_num() == 2:
        set_table_players_location(init_x=TABLE_WIDTH / 4 - 2 * CARD_WIDTH, player_x_space=43 - CARD_WIDTH,
                                   table_=table_)

    elif table_.get_player_num() == 3:
        set_table_players_location(init_x=TABLE_WIDTH / 5 - 2 * CARD_WIDTH,
                                   player_x_space=30 - CARD_WIDTH,
                                   hand_x_space=INIT_HAND_X_SPACE - 2,
                                   table_=table_)

    elif table_.get_player_num() == 4:
        set_table_players_location(init_x=TABLE_WIDTH / 6 - 2 * CARD_WIDTH,
                                   player_x_space=25 - CARD_WIDTH,
                                   hand_x_space=INIT_HAND_X_SPACE - 2,
                                   table_=table_)


def set_banker_location(cards):
    if len(cards) > 0:
        cards[0].set_x(34)

    for num in range(len(cards)):
        if num > 1:
            cards[num].set_x(40 + 2 * num)


def set_table_players_location(init_x=0.0, init_y=0.0, card_x_space=None, card_y_space=None, hand_x_space=None,
                               hand_y_space=None, player_x_space=30.0, player_y_space=0.0, table_=None):
    if table_:
        players = table_.get_players()
        for num in range(len(players)):
            set_player_location(init_x=init_x + (num * player_x_space if player_x_space else num * INIT_PLAYER_X_SPACE),
                                init_y=init_y + (num * player_y_space if player_y_space else num * INIT_PLAYER_Y_SPACE),
                                card_x_space=card_x_space,
                                card_y_space=card_y_space,
                                hand_x_space=hand_x_space,
                                hand_y_space=hand_y_space,
                                player=players[num])


def set_player_location(init_x=0.0, init_y=0.0, card_x_space=None, card_y_space=None, hand_x_space=None,
                        hand_y_space=None, player=None):
    if player:
        hands = player.get_hands()
        for num in range(len(hands)):
            set_hand_location(init_x=init_x + (num * hand_x_space if hand_x_space else num * INIT_HAND_X_SPACE),
                              init_y=init_y + (num * hand_y_space if hand_y_space else num * INIT_HAND_Y_SPACE),
                              card_x_space=card_x_space,
                              card_y_space=card_y_space,
                              hand=hands[num])


def set_hand_location(init_x=0.0, init_y=0.0, card_x_space=None, card_y_space=None, hand=None):
    if hand:
        cards = hand.get_cards()
        for num in range(len(cards)):
            set_card_location(x=init_x + (num * card_x_space if card_x_space else num * INIT_CARD_X_SPACE),
                              y=init_y + (num * card_y_space if card_y_space else num * INIT_CARD_Y_SPACE),
                              card=cards[num])


def set_card_location(x=0.0, y=0.0, card=None):
    card.set_x(x)
    card.set_y(y)
