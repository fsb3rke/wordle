"""
    AUTHOR: werlora
    DATE:   5/31/25
"""

"""
    THIS IS SPLITTED FOR TODO SECTION

    TODO: (0) write a better version of "upper" function 'cuz there's no way to upper i->İ it's rewrites like i->I.
    TODO: (1) colored text for hints. GREEN means true position of char. YELLOW means wrong position but word contains in the char which is given. NON-COLORED means wrong char, it's not in the word.
    TODO: (debug) if line marked with this todo, it means it'll be removed when it's finished.
"""

from random import choice


FILE_NAME: str = "Allfivecharwords.txt"

"""
Fetchs word data for create a list.
"""
def get_word_list(fname: str) -> list:
    return open(fname, 'r').read().splitlines()

class Wordle:
    def __init__(self, fname: str) -> None:
        self.fname: str = fname
        self.__word_list: list = get_word_list(self.fname)
        self.__guessed_words: list = []
        self.__wordle_word: str = ""

    """
    Resets all of guessed words and selected wordle word.
    """
    def reset(self) -> None:
        self.__guessed_words = []
        self.__wordle_word = ""

    """
    Sets a wordle word.
    """
    def set_wordle_word(self) -> None:
        self.__wordle_word = choice(self.__word_list)
        print(self.__wordle_word) # TOOD: (debug)

    """
    Checks if word equals wordle word.
    """
    def check_if_word_equals_wordle_word(self, word: str) -> bool:
        return self.__wordle_word == word.upper() # TODO: (0)

    def guess(self, word: str) -> bool:
        statement: bool =   word.upper() in self.__word_list and len(word) == 5 and word.upper() not  in self.__guessed_words # TODO: (0)
        if statement:
            self.__guessed_words.append(word.upper()) # TODO: (0)

        return statement

    def get_guessed_words_with_table(self) -> str:
        table_rows: list = []
        for i in range(len(self.__guessed_words)):
            temp_row: list = []
            for j in range(len(self.__guessed_words[i])):
                temp_row.append(f"|{self.__guessed_words[i][j]}|") # TODO: (1)

            table_rows.append(temp_row)

        # This is for empty rows
        for j in range(5-len(table_rows)):
            temp_s_row: list = []
            for a in range(5):
                temp_s_row.append("| |")

            table_rows.append(temp_s_row)

        table: str = ""
        for i in range(len(table_rows)):
            table += " ".join(table_rows[i]) + ("\n" if (i+1) < len(table_rows) else "")
            
        return table

game: Wordle = Wordle(FILE_NAME)
game.set_wordle_word()

i: int = 0
while i != 5:
    print(game.get_guessed_words_with_table())
    print()

    word: str = str(input("Guess word: "))
    if not game.guess(word):
        i -= 1
    
    if game.check_if_word_equals_wordle_word(word):
        print("BROO YOU FOND IT!!")
        break

    i += 1

print(game.get_guessed_words_with_table())
