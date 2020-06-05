import re
import reprlib


WORD_PATTERN = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = WORD_PATTERN.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return f'Sentence {reprlib.repr(self.text)}'
