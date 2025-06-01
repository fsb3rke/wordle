"""
    AUTHOR: werlora
    DATE:   5/31/25
"""


from textual.app import App, ComposeResult
from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual.message import Message
from rich.panel import Panel
from rich.text import Text
from random import choice

FILE_NAME = "Allfivecharwords.txt"

def get_word_list(fname: str) -> list[str]:
    with open(fname, "r", encoding="utf-8") as f:
        return [line.strip().upper() for line in f if len(line.strip()) == 5]

class GuessSubmitted(Message):
    def __init__(self, guess: str) -> None:
        self.guess = guess.upper()
        super().__init__()

class WordleGame:
    def __init__(self, word_list: list[str]) -> None:
        self.word_list = word_list
        self.reset()

    def reset(self):
        self.word = choice(self.word_list).upper()
        self.guessed = []

    def is_valid_guess(self, word: str) -> bool:
        word = word.upper()
        return word in self.word_list and len(word) == 5 and word not in self.guessed

    def submit_guess(self, word: str) -> bool:
        word = word.upper()
        if self.is_valid_guess(word):
            self.guessed.append(word)
            return True
        return False

    def is_correct(self, word: str) -> bool:
        return word.upper() == self.word

    def get_colored_guess(self, word: str) -> Text:
        result = Text()
        target = list(self.word)
        used = [False] * 5

        for i, c in enumerate(word):
            if c == target[i]:
                result.append(c, style="bold white on green")
                used[i] = True
            else:
                result.append(c, style="bold white")

        for i, c in enumerate(word):
            if result[i] != "_":
                continue
            if c in target:
                idx = target.index(c)
                if not used[idx]:
                    result[i] = Text(c, style="bold black on yellow")
                    used[idx] = True
                else:
                    result[i] = Text(c, style="bold white on grey23")
            else:
                result[i] = Text(c, style="bold white on grey23")
        return result

class WordleView(Static):
    def __init__(self, game: WordleGame):
        super().__init__()
        self.game = game

    def render(self) -> Panel:
        lines = []
        for guess in self.game.guessed:
            lines.append(self.game.get_colored_guess(guess))
        for _ in range(5 - len(lines)):
            lines.append(Text("     ", style="dim"))

        return Panel(Text("\n").join(lines), title="WORDLE")

class WordleApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.word_list = get_word_list(FILE_NAME)
        self.game = WordleGame(self.word_list)

    def compose(self) -> ComposeResult:
        yield Vertical(
            WordleView(self.game),
            Input(placeholder="Guess a 5-letter word...", id="word-input")
        )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        guess = event.value.strip().upper()
        input_widget = self.query_one("#word-input", Input)

        if not self.game.is_valid_guess(guess):
            input_widget.placeholder = "Invalid guess. Try again!"
            input_widget.value = ""
            return

        self.game.submit_guess(guess)
        self.query_one(WordleView).refresh()
        input_widget.value = ""

        if self.game.is_correct(guess):
            input_widget.placeholder = "Correct! Press Q to quit."
            input_widget.disabled = True
        elif len(self.game.guessed) >= 5:
            input_widget.placeholder = f"Out of tries! Word was {self.game.word}"
            input_widget.disabled = True

if __name__ == "__main__":
    WordleApp().run()
