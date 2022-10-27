import uuid
from app.game_component.table import Table


class Blackjack:

    def __init__(self, id_=None):

        self.id = id_ if id_ else uuid.uuid1()

        # Setting Table
        self.max_table = 6
        self.tables = []

    # Table Maintain
    def create_table(self, table_name=None, deck_num=None, max_player=None, min_bet=None, bj_ratio=None,
                     is_insurance=True, is_insurance_over_10=False, is_double=True):

        if not table_name:
            return

        if table_name == "":
            return

        if len(self.tables) == self.max_table:
            return

        if self.get_table_by_name(table_name):
            return

        self.tables.append(
            Table(table_name=table_name, deck_num=deck_num, max_player=max_player, min_bet=min_bet, bj_ratio=bj_ratio,
                  is_insurance=is_insurance, is_insurance_over_10=is_insurance_over_10, is_double=is_double))

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

    # GET
    def get_table_by_id(self, table_id):
        for table in self.tables:
            if str(table.get_id()) == table_id:
                return table

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

    def get_is_table_exit(self, table):
        if self.get_table_by_name(table):
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
