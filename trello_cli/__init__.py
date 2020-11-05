import os
from dotenv import load_dotenv

from trello import TrelloClient

load_dotenv()

client = TrelloClient(
    api_key=os.environ['TRELLO_API_KEY'],
    api_secret=os.environ['TRELLO_API_SECRET'],
    token=os.environ['TRELLO_TOKEN']
)


class TrelloManager:
    ENTER_KEY = 'ENTER'
    BACK_KEY = 'b'
    TOP_KEY = 't'
    EXIT_KEY = 'q'

    ERROR_CODE = 'ERROR'

    @classmethod
    def input_check(cls, input_key):
        if input_key == '':
            val = cls.ENTER_KEY
        elif input_key == cls.BACK_KEY:
            val = cls.BACK_KEY
        else:
            try:
                val = int(input_key)
            except ValueError:
                val = cls.ERROR_CODE

        return val

    @classmethod
    def print_common_command(cls, add_commands=[]):
        print('')
        print('------------')
        for command in add_commands:
            print(command)
        print('[{back}] Back'.format(back=TrelloManager.BACK_KEY))
        print('[{top}] TOP'.format(top=TrelloManager.TOP_KEY))
        print('[{exit}] Exit'.format(exit=TrelloManager.EXIT_KEY))

    @classmethod
    def print_next_message(cls):
        print('')
        print('What you gonna after this?')

    def __init__(self):
        self.boards = None
        self.select_board = None
        self.select_list = None
        self.select_dist_list = None
        self.labels = None
        self.select_card_action = None

    @classmethod
    def print_header(cls, msg):
        print('')
        print(msg)

    @classmethod
    def print_success_mgs(cls, msg):
        print('')
        print(msg)
        print('')

    def prompt(self):
        val = ' > '
        if self.select_board:
            val = self.select_board.name + ' > '
        if self.select_list:
            val += self.select_list.name + ' > '

        return val

    def error_func(self, func, input_key):
        print('入力された文字が不正です。[{key}] '.format(key=input_key))
        func()

    def exec_input_common_key(self, input_val, back_func=None):
        if input_val == TrelloManager.BACK_KEY:
            if back_func is None:
                self.print_select_board_prompt()
            else:
                back_func()

        elif input_val == TrelloManager.TOP_KEY:
            self.print_select_board_prompt()

        elif input_val == TrelloManager.EXIT_KEY:
            exit()

    def print_select_board_prompt(self):
        TrelloManager.print_header('# select board number.')
        for i, board in enumerate(self.boards):
            print('[{index}] {name}'.format(name=board.name, index=i))
        self.print_common_command()

        input_key = input('Enter board number :')
        self.exec_input_common_key(input_key)

        input_val = TrelloManager.input_check(input_key)

        if input_val in [TrelloManager.ERROR_CODE, TrelloManager.ENTER_KEY]:
            self.error_func(self.print_select_board_prompt, input_key)

        else:
            if len(self.boards) < input_val:
                self.error_func(self.print_select_board_prompt, input_key)

            else:
                self.select_board = self.boards[input_val]
                self.labels = self.select_board.get_labels()
                self.print_select_list_prompt()

    def print_select_list_prompt(self, dist=False):
        TrelloManager.print_header('# select list number.')
        for i, list in enumerate(self.select_board.list_lists()):
            print(
                '[{index}] {name}'.format(
                    name=list.name,
                    index=i))
        TrelloManager.print_common_command()

        input_key = input(
            '{prompt} Enter list number :'.format(
                prompt=self.prompt()))
        input_val = TrelloManager.input_check(input_key)
        self.exec_input_common_key(input_key)

        if input_val in [TrelloManager.ERROR_CODE, TrelloManager.ENTER_KEY]:
            self.error_func(self.print_select_list_prompt, input_key)

        else:
            if len(self.select_board.list_lists()) < input_val:
                self.error_func(self.print_select_list_prompt, input_key)

            else:
                select_list = self.select_board.list_lists()[input_val]
                if dist:
                    self.select_dist_list = select_list
                else:
                    self.select_list = select_list
                    self.print_select_card_prompt()

    def print_select_card_prompt(self):
        TrelloManager.print_header('# select card number or command')
        for i, card in enumerate(self.select_list.list_cards()):
            print('[{index}] {name}'.format(name=card.name, index=i))
        TrelloManager.print_common_command([
            '[{enter}] Create new card'.format(enter=TrelloManager.ENTER_KEY),
        ])

        input_key = input('{prompt} Enter card number :'.format(
            prompt=self.prompt()))
        input_val = TrelloManager.input_check(input_key)
        self.exec_input_common_key(input_key, self.print_select_list_prompt)

        if input_val == TrelloManager.ERROR_CODE:
            self.error_func(self.print_select_card_prompt, input_key)

        elif input_val == TrelloManager.ENTER_KEY:
            self.print_create_card_prompt()

        else:
            if len(self.select_list.list_cards()) < input_val:
                self.error_func(self.print_select_card_prompt, input_key)

            else:
                select_card = self.select_list.list_cards()[input_val]
                self.print_select_card_action_prompt()

                if self.select_card_action == 0:
                    self.print_card_move_prompt(select_card)

                elif self.select_card_action == 1:
                    self.print_card_remove_prompt(select_card)

    def print_create_card_prompt(self):
        TrelloManager.print_header('# craate card')
        card_name = input('{prompt} Input New card name :'.format(
            prompt=self.prompt()))
        if card_name == '':
            self.error_func(self.print_select_card_prompt, card_name)
        else:
            card = self.select_list.add_card(card_name)
            self.print_select_label_prompt(card)

    def print_select_label_prompt(self, card):
        TrelloManager.print_header('# select label number')
        for i, label in enumerate(self.labels):
            print('[{index}] {name}'.format(name=label.name, index=i))
        print('[{enter}] Skip'.format(enter=TrelloManager.ENTER_KEY))

        input_key = input('{prompt} Enter label number :'.format(
            prompt=self.prompt()))
        input_val = TrelloManager.input_check(input_key)

        if input_val == TrelloManager.ERROR_CODE:
            self.error_func(self.print_select_card_prompt, input_key)

        elif input_val == TrelloManager.ENTER_KEY:
            self.print_success_mgs('Card created success.')
            self.print_select_card_prompt()

        else:
            select_label = self.labels[input_val]
            card = client.get_card(card.id)
            card.add_label(select_label)

            self.print_success_mgs('Card created success.')
            self.print_select_card_prompt()

    def print_select_card_action_prompt(self):
        TrelloManager.print_header('# select action number')
        print('[0] Move card')
        print('[1] Remove card')

        input_key = input('{prompt} Enter action number :'.format(
            prompt=self.prompt()))
        input_val = TrelloManager.input_check(input_key)
        self.exec_input_common_key(input_key, self.print_select_list_prompt)

        if input_val == TrelloManager.ERROR_CODE:
            self.error_func(self.print_select_card_action_prompt, input_key)

        elif input_val == TrelloManager.ENTER_KEY:
            self.error_func(self.print_select_card_action_prompt, input_key)

        else:
            self.select_card_action = input_val

    def print_card_move_prompt(self, select_card):
        self.print_select_list_prompt(dist=True)
        select_card.change_list(self.select_dist_list.id)

        self.print_success_mgs('Card moved success.')
        self.print_select_card_prompt()

    def print_card_remove_prompt(self, select_card):
        select_card.delete()
        self.print_success_mgs('Card removed success.')
        TrelloManager.print_next_message()
        self.print_select_card_prompt()


def main() -> None:
    tm = TrelloManager()
    tm.boards = client.list_boards()

    tm.print_select_board_prompt()
