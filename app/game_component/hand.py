import uuid


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
