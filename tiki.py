import random

def giving_cards(playerno):

    data = ['Nani Nui Eepo',
            'Kapu Lokahi Nani',
            'Wikiwiki Akami Eepo',
            'Wikiwiki Hookipa Akami',
            'Hookipa Nui Wikiwiki',
            'Wikiwiki Kapu Akami',
            'Hookipa Lokahi Nani',
            'Hookipa Lokahi Huhu',
            'Lokahi Wikiwiki Kapu',
            'Eepo Huhu Akami',
            'Eepo Nani Akami',
            'Akami Huhu Kapu',
            'Akami Huhu Hookipa',
            'Nani Hookipa Nui',
            'Huhu Nui Eepo',
            'Lokahi Wikiwiki Hookipa',
            'Kapu Lokahi Huhu',
            'Nui Eepo Wikiwiki',
            'Huhu Kapu Nui',
            'Huhu Hookipa Nui',
            'Akami Nani Kapu',
            'Akami Nani Hookipa',
            'Kapu Nui Wikiwiki',
            'Lokahi Eepo Nani',
            'Lokahi Eepo Huhu',
            'Eepo Wikiwiki Lokahi',
            'Nani Kapu Nui']
    empty = []
    for j in range(int(playerno)):
        code = random.randint(0, 27-(j+1))
        info_in_code = data.pop(code)
        empty.append(info_in_code)
    return empty


class Position():
    def __init__(self):
        self.position = []
        self.card_database = ['1up', '1up', '2up', '3up', 'topple', 'toast', 'toast']
        self.tiki_database = ['Wikiwiki', 'Huhu', 'Nani', 'Hookipa', 'Kapu', 'Eepo', 'Lokahi', 'Akami', 'Nui']
        self.counter = 0
        self.all_cards_finished = 0
        self.scoreboard = {}
        self.sc_data = {}
    def reset(self):
        self.position = []
        self.card_database = ['1up', '1up', '2up', '3up', 'topple', 'toast', 'toast']
        self.tiki_database = ['Wikiwiki', 'Huhu', 'Nani', 'Hookipa', 'Kapu', 'Eepo', 'Lokahi', 'Akami', 'Nui']
        self.counter = 0
        self.all_cards_finished = 0
        self.scoreboard = {}
        self.sc_data = {}
    def add_counter(self):
        self.counter += 1
    def reset_counter(self):
        self.counter = 0
    def set_position(self):
        tiki1 = ['Wikiwiki', 'Huhu', 'Nani']
        tiki2 = ['Hookipa', 'Kapu', 'Eepo']
        tiki3 = ['Lokahi', 'Akami', 'Nui']
        random.shuffle(tiki1)
        random.shuffle(tiki2)
        random.shuffle(tiki3)
        number = random.randint(1, 6)
        if number == 1:
            start = tiki1 + tiki2 + tiki3
        elif number == 2:
            start = tiki1 + tiki3 + tiki2
        elif number == 3:
            start = tiki2 + tiki1 + tiki3
        elif number == 4:
            start = tiki2 + tiki3 + tiki1
        elif number == 5:
            start = tiki3 + tiki1 + tiki2
        elif number == 6:
            start = tiki3 + tiki2 + tiki1
        return start
    def move_except_toast(self, tiki, card, position):
        if card == "1up":
            if position[0] == tiki:
                return False
            else:
                tiki_index = position.index(tiki)
                tiki = position.pop(tiki_index)
                position.insert(tiki_index-1, tiki)
                self.position = position
                return self.position
        elif card == "2up":
            if position[0] == tiki or position[1] == tiki:
                return False
            else:
                tiki_index = position.index(tiki)
                tiki = position.pop(tiki_index)
                position.insert(tiki_index-2, tiki)
                self.position = position
                return self.position
        elif card == "3up":
            if position[0] == tiki or position[1] == tiki or position[2] == tiki:
                return False
            else:
                tiki_index = position.index(tiki)
                tiki = position.pop(tiki_index)
                position.insert(tiki_index - 3, tiki)
                self.position = position
                return self.position
        elif card == "topple":
            if position[-1] == tiki:
                return False
            else:
                tiki_index = position.index(tiki)
                tiki = position.pop(tiki_index)
                position.append(tiki)
                self.position = position
                return self.position
        else:
            return False
    def move_toast(self, position):
        del position[-1]
        self.position = position
        return self.position
class Player():
    def __init__(self):
        self.name = ""
        self.sc = []
        self.points = 0
        self.cards_to_use = ['1up', '1up', '2up', '3up', 'topple', 'toast', 'toast']
        self.myturn = False
        self.already_chose_card = False
        self.current_card = " "
        self.empty = False
    def reset(self):
        self.name = ""
        self.sc = []
        self.points = 0
        self.cards_to_use = ['1up', '1up', '2up', '3up', 'topple', 'toast', 'toast']
        self.myturn = False
        self.already_chose_card = False
        self.current_card = " "
        self.empty = False
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
    def set_sc(self, secret_card):
        secret_card = secret_card.split(" ")
        for element in secret_card:
            self.sc.append(element)
    def switch_myturn(self, state):
        self.myturn = state
    def get_turn(self):
        return self.myturn
    def set_already_chose_card(self, value):
        self.already_chose_card = value
    def get_already_chose_card(self):
        return self.already_chose_card
    def set_current_card(self, card):
        self.current_card = card
    def get_current_card(self):
        return self.current_card
    def remove_card(self, card, card_list):
        card_list.remove(card)
        self.cards_to_use = card_list
        return self.cards_to_use
    def calculating_points(self, position):
        if self.sc[0] == position[0]:
            self.points += 3
        if self.sc[1] == position[0] or self.sc[1] == position[1]:
            self.points += 2
        if self.sc[2] == position[0] or self.sc[2] == position[1] or self.sc[2] == position[2]:
            self.points += 1
        return self.points
        

    
